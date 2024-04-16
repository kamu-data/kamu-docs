---
Title: Leaderboard
description:
weight: 0
categories: []
aliases: []
---

**Topics covered:**
- Top-N aggregation
- Retractions / corrections
- Push ingest

## Summary
Suppose we have a game where players compete in matches against one another and get assigned an overall match score. In this example we will see:
- How to create a dataset that represents a leaderboard of top-scoring players in the game using "Top-N" class of queries
- How such dataset tracks the entire history of changes
- And how "Top-N" queries manifest into a mechanism called retractions and corrections.


## Steps

### Getting Started
To follow this example checkout `kamu-cli` repository and navigate into [examples/leaderboard](https://github.com/kamu-data/kamu-cli/tree/master/examples/leaderboard) sub-directory.

Create a temporary kamu {{<term "workspace">}} in that folder using:

```sh
kamu init
```

You can either follow the example steps below or fast-track through it by running:

```sh
./init.sh
```

### Scores Dataset
We start with the `player_scores` dataset that will ingest the scores of all players who played a match. It will have a very simple schema:
- `match_time TIMESTAMP`
- `match_id BIGINT`
- `player_id STRING`
- `score BIGINT`

Our game will be sending scores data directly to the {{<term "node">}} hosting this dataset, so we will use {{<schema "AddPushSource">}} metadata event to describe the format that data will come in.

We'll use {{<schema "NdJson" "ReadStep::NdJson">}}:

```yaml
kind: DatasetSnapshot
version: 1
content:
  name: player-scores
  kind: Root
  metadata:
    - kind: AddPushSource
      sourceName: default
      read:
        kind: NdJson
        schema:
          - "match_time TIMESTAMP"
          - "match_id BIGINT"
          - "player_id STRING"
          - "score BIGINT"
      merge:
        kind: Ledger
        primaryKey:
          - match_id
          - player_id
    - kind: SetVocab
      eventTimeColumn: match_time
```

Create the dataset now:
```sh
kamu add player-scores.yaml
```

To get data in we will ingest it from a file, but note that it could similarly be any other ["push" protocol]({{<ref "push-source">}}) like REST, MQTT, Kafka...

Let's add the first match scores in:
```sh
kamu ingest player-scores ./data/1.ndjson
```

You can see the new data via:
```sh
kamu tail player-scores
```

```
┌────────┬────┬─────┬──────────┬───────────┬───────┐
│ offset │ op │ ... │ match_id │ player_id │ score │
├────────┼────┼─────┼──────────┼───────────┼───────┤
│      0 │ +A │ ... │        1 │     Alice │   100 │
│      1 │ +A │ ... │        1 │       Bob │    80 │
└────────┴────┴─────┴──────────┴───────────┴───────┘
```

### Leaderboard Dataset
Having all the historical scores we could already build a leaderboard using batch computations as simple as:

```sh
kamu sql
```

```sql
select
  *
from (
  select
    row_number() over (order by score desc) as place,
    match_time,
    match_id,
    player_id,
    score
  from "player-scores";
) where place <= 2
```

But there are **many benefits** to expressing it as a streaming pipeline, which we will discuss shortly.

For now let's create a streaming leaderboard dataset. Luckily the query is almost identical to the batch variant:

```yaml
kind: DatasetSnapshot
version: 1
content:
  name: leaderboard
  kind: Derivative
  metadata:
    - kind: SetTransform
      inputs:
        - datasetRef: player-scores
          alias: player_scores
      transform:
        kind: Sql
        engine: risingwave
        queries:
          - alias: leaderboard
            # Note we are using explicit `crate materialized view` statement below
            # because RW does not currently support Top-N queries directly on sinks.
            #
            # Note `partition by 1` is currently required by RW engine
            # See: https://docs.risingwave.com/docs/current/window-functions/#syntax
            query: |
              create materialized view leaderboard as
              select
                *
              from (
                select
                  row_number() over (partition by 1 order by score desc) as place,
                  match_time,
                  match_id,
                  player_id,
                  score
                from player_scores
              )
              where place <= 2
          - query: |
              select * from leaderboard
    - kind: SetVocab
      eventTimeColumn: match_time
```

Create this dataset:

```sh
kamu add player-scores.yaml
```

Let's process all data that is already in `player-scores` and see the results:

```sh
kamu pull leaderboard
kamu tail leaderboard
```

```
┌────────┬────┬─────┬───────┬──────────┬───────────┬───────┐
│ offset │ op │ ... │ place │ match_id │ player_id │ score │
├────────┼────┼─────┼───────┼──────────┼───────────┼───────┤
│      0 │ +A │ ... │     1 │        1 │     Alice │   100 │
│      1 │ +A │ ... │     2 │        1 │       Bob │    80 │
└────────┴────┴─────┴───────┴──────────┴───────────┴───────┘
```

### Introducing Retractions
Suppose we played another match with scores like these:
```
Alice: 70
Charlie: 90
```

Let's see what happens to the `leaderboard` dataset:

```sh
kamu ingest player-scores ./data/2.ndjson
kamu pull leaderboard
kamu tail leaderboard
```

Pay attention to the `op` column:
```
┌────────┬────┬─────┬───────┬──────────┬───────────┬───────┐
│ offset │ op │ ... │ place │ match_id │ player_id │ score │
├────────┼────┼─────┼───────┼──────────┼───────────┼───────┤
│      0 │ +A │ ... │     1 │        1 │     Alice │   100 │
│      1 │ +A │ ... │     2 │        1 │       Bob │    80 │
│      2 │ -R │ ... │     2 │        1 │       Bob │    80 │
│      3 │ +A │ ... │     2 │        2 │   Charlie │    90 │
└────────┴────┴─────┴───────┴──────────┴───────────┴───────┘
```

Now this is very interesting:
- We still see the history of Alice and Bob being ranked 1 and 2 initially
- Then we see a "retraction" (`-R`) record that says "Bob is no longer ranked 2nd"
- And an "append" (`+A`) record that says "Charlie is now ranked 2nd"

If we repeat this again with scores:
```
Bob: 60
Charlie: 110
```

As usual:
```sh
kamu ingest player-scores ./data/3.ndjson
kamu pull leaderboard
kamu tail leaderboard
```

As Alice was displaced by Charlie from the 1st place we see (starting from row `offset: 4`) how both records are retracted and replaced by new values:
```
┌────────┬────┬─────┬───────┬──────────┬───────────┬───────┐
│ offset │ op │ ... │ place │ match_id │ player_id │ score │
├────────┼────┼─────┼───────┼──────────┼───────────┼───────┤
│      0 │ +A │ ... │     1 │        1 │     Alice │   100 │
│      1 │ +A │ ... │     2 │        1 │       Bob │    80 │
│      2 │ -R │ ... │     2 │        1 │       Bob │    80 │
│      3 │ +A │ ... │     2 │        2 │   Charlie │    90 │
│      4 │ -R │ ... │     1 │        1 │     Alice │   100 │
│      5 │ -R │ ... │     2 │        2 │   Charlie │    90 │
│      6 │ +A │ ... │     1 │        3 │   Charlie │   110 │
│      7 │ +A │ ... │     2 │        1 │     Alice │   100 │
└────────┴────┴─────┴───────┴──────────┴───────────┴───────┘
```

You are witnessing the {{<term "retractions and corrections mechanism" "retractions-and-corrections">}} of ODF datasets!

## So, why not Batch?
So what do we gain from having a changelog stream with retractions? Why not run a batch query every once in a while to get the current leaderboard?

The answer is: ***automation and infinite composability***.

As your game evolves, you might want to start rewarding people at top spots with prizes. You may also want to reset the leaderboard each month to make people prove themselves again. All this logic can be expressed as additional steps in the streaming data pipeline.

If you write services that batch-query data at specific points in time and distribute rewards imagine what happens:
- if some player is caught cheating and has to be **retroactively** stripped of its match scores (input retraction)
- if score ingestion pipeline goes down for a day and people who did in fact get top scores end up not accounted for during the reward distribution (backfill)
- if your game is very high-stakes and your have to prove during an audit how the rewards were issued (provenance).

These situations that we call "abnormal" are actually very frequent and in batch world require **highly error-prone manual intervention**.

In the world of ODF streaming - late data, backfills, and input retractions are just normal occurrences. ODF pipeline know how to react to these events and can **automatically reconcile their state** without human intervention, and maintaining a **verifiable provenance**.

---

If you haven't already - make sure to check out the [Stock Market Trading example]({{<ref "stock-trading">}}) that introduces the **{{<term "watermark">}}** - another really important mechanism related to streams.