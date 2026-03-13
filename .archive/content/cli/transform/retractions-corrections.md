---
Title: Retractions & Corrections
description:
weight: 50
underConstruction: false
categories: []
aliases:
---

## Motivation
Errors in source data are inevitable and require a mechanism for correcting them post factum. Unlike databases, where one could issue `DELETE` or `UPDATE` queries, our core data model is an [immutable append-only stream]({{<relref "spec#nature-of-data">}}), and thus requires a different mechanism to issue **retractions and corrections** for past events.

In cases when stream processing operations encounter late data (beyond the current {{<term "watermark">}}), or retractions and corrections in the input, they may also need to issue corrections or retractions for previously produced results that were influenced by these events.

We consider the correction / retraction model that works across all stages of data pipelines essential to making processing **maximally autonomous**. In turn, only by making data processing autonomous can collaborative data pipelines be **sustainable at global scale**.

## Scenario
Consider a video game that writes events to a `match_scores` dataset as players complete the matches:

| match_time | match_id | player_name | score |
| ---------: | -------: | ----------: | ----: |
|         t1 |        1 |       Alice |   100 |
|         t1 |        1 |         Bob |    80 |
|         t2 |        2 |       Alice |    70 |
|         t2 |        2 |     Charlie |    90 |
|         t3 |        3 |         Bob |    60 |
|         t3 |        3 |     Charlie |   110 |

Let's say we want to create a dataset that continuously tracks the **top two** (for simplicity) highest-scoring players - a **leader board**.

This is the case of [Top-N query](https://nightlies.apache.org/flink/flink-docs-release-1.18/docs/dev/table/sql/queries/topn/) and [Window Top-N](https://nightlies.apache.org/flink/flink-docs-release-1.18/docs/dev/table/sql/queries/window-topn/), which can be written in Apache Flink SQL as:

```sql
select
  *
from (
  select
    ROW_NUMBER() OVER (ORDER BY score desc) AS place,
    match_time,
    player_name,
    score,
  from match_scores
) where place <= 2
```

## Representing changes in streams
There are several ways to represent how this query behaves when applied to the above input stream.

### Retract Stream
The most generic way is a "retract stream" that only uses append `+A` and retract `-R` operations (note the new `op` column):

|   op | place | match_time | player_name | score |
| ---: | ----: | ---------: | ----------: | ----: |
|   +A |     1 |         t1 |       Alice |   100 |
|   +A |     2 |         t1 |         Bob |    80 |
|   -R |     2 |         t1 |         Bob |    80 |
|   +A |     2 |         t2 |     Charlie |    90 |
|   -R |     1 |         t1 |       Alice |   100 |
|   -R |     2 |         t2 |     Charlie |    90 |
|   +A |     1 |         t3 |     Charlie |   110 |
|   +A |     2 |         t3 |       Alice |   100 |

In this model the updated state of the leader board is compared with the previous state after each new event, and necessary records first get retracted before being replaced with appends.

### Upsert Stream
Using the knowledge that the `place` column plays the role of a unique key of the resulting state we could also represent the above as an "upsert stream" using only upsert `+A` and retract `-R` operations:

|   op | place | match_time | player_name | score |
| ---: | ----: | ---------: | ----------: | ----: |
|   +A |     1 |         t1 |       Alice |   100 |
|   +A |     2 |         t1 |         Bob |    80 |
|   +A |     2 |         t2 |     Charlie |    90 |
|   +A |     1 |         t3 |     Charlie |   110 |
|   +A |     2 |         t3 |       Alice |   100 |

This additional knowledge allows us to significantly compact the stream. 

Although the retract operation does not appear in our example, it is needed for completeness, e.g. imagine if the source stream retracted the result of the first match right after `t1` - this would require us to empty the leader board with retractions too.

### Changelog Stream (single event)
Some systems produce "changelog streams" containing append `+A`, retract `-R`, and correct `+C` operations with update carrying both the new values and the old values of the record being changed:

|   op | place | match_time | player_name | score | match_time_old | old_player_name | old_score |
| ---: | ----: | ---------: | ----------: | ----: | -------------: | --------------: | --------: |
|   +A |     1 |         t1 |       Alice |   100 |                |                 |           |
|   +A |     2 |         t1 |         Bob |    80 |                |                 |           |
|   +C |     2 |         t2 |     Charlie |    90 |             t1 |             Bob |        80 |
|   +C |     1 |         t3 |     Charlie |   110 |             t1 |           Alice |       100 |
|   +C |     2 |         t1 |       Alice |   100 |             t2 |         Charlie |        90 |

This format is also used by CDC systems like [Debezium](https://debezium.io/) and as an internal data representation in [Arroyo](https://github.com/ArroyoSystems/arroyo).

This format is the most "informative" one, as it differentiates retractions from corrections, and provides access to both the new and the previous state within one event. The drawback is that it significantly impacts the schema to essentially allow carrying two events (old and new) in one record.

### Changelog Stream (two events)
The Apache Flink's "changelog streams" variant is using append `+A`, retract `-R`, correct-from `-C`, and correct-to `+C` operations. Here, the "correct-from" events carry the previous values of the record about to be updated and "correct-to" events carry the new values, with the restriction that these events must **always appear side by side** and in order.

|   op | place | match_time | player_name | score |
| ---: | ----: | ---------: | ----------: | ----: |
|   +A |     1 |         t1 |       Alice |   100 |
|   +A |     2 |         t1 |         Bob |    80 |
|   -C |     2 |         t1 |         Bob |    80 |
|   +C |     2 |         t2 |     Charlie |    90 |
|   -C |     1 |         t1 |       Alice |   100 |
|   +C |     1 |         t3 |     Charlie |   110 |
|   -C |     2 |         t2 |     Charlie |    90 |
|   +C |     2 |         t1 |       Alice |   100 |

By splitting the update operation in two events this format does not require extending the schema with multiple columns.

Due to the restriction that correct from/to events appear side by side, this format can be easily converted into single-event changelog stream form upon reading.


## ODF Model
ODF uses the [two-event changelog stream](#changelog-stream-two-events) as its base model.

Just like in our example above a special `op` column carries the {{<term "operation type">}} of each record.

Retractions and corrections are supported on {{<term "root dataset">}} level via [merge strategies]({{<relref "merge-strategies">}}).

We are currently working to integrate their support into all processing engines for seamless propagation across {{<term "derivative datasets" "derivative-dataset">}}.
