---
Title: Merge Strategies
description: Describes the process of historization used depending on the nature of source data
weight: 20
categories: []
aliases:
---

# Purpose

Open Data Fabric [by design]({{<relref "spec#nature-of-data">}}) stores all data in the append-only event log format, always preserving the entire history. Unfortunately, a lot of data in the world is not stored or exposed this way. Some organizations may share their data in the form of periodic database dumps, while some choose to provide it as a log of changes between current and the previous export.

When ingesting data from external sources, {{<term "Root datasets" "root-dataset">}} can choose between different {{<schema "merge strategies" "MergeStrategy">}} that define how to combine the newly-ingested data with the existing one.

# Types

## `Ledger`
{{<schema "Ledger" "MergeStrategy::Ledger">}} strategy should be used for data sources containing append-only event streams. New data exports can have new rows added, but once data already made it into one export it should never change or disappear. A user-specified primary key is used to identify which events were already seen, not to duplicate them.

<!-- TODO: Describe what happens if historical records were modified by the publisher --->

### Example <!-- omit in toc -->

Imagine a data publisher that exposes dataset with **historical** populations of major cities around the world, for example:

```csv
Year,Country,City,Population
2019,CA,Vancouver,2581000
2019,US,Seattle,3433000
```

This dataset is temporal (has a `year` column), so it's a good sign that we're dealing with a `ledger` data.

{{<warning>}}
Having a time column doesn't always mean that the dataset is a ledger - to be a true ledger all previous records should be immutable and never change.
{{</warning>}}

So we use the following root dataset manifest to ingest it:

```yaml
kind: DatasetSnapshot
version: 1
content:
  name: cities-population
  kind: Root
  metadata:
    - kind: SetPollingSource
      ...
      merge:
        kind: Ledger
        primaryKey:
          - year
          - country
          - city
    - kind: SetVocab
      eventTimeColumn: year
```

Notice that we specify `ledger` merge strategy with composite primary key `(year, country, city)`, meaning that we expect only one record per city per year. We also set `eventTimeColumn` to use `year` as the source of event times.

The resulting dataset when ingested will look like this:

|  op   | system_time | event_time | country |   city    | population |
| :---: | :---------: | :--------: | :-----: | :-------: | :--------: |
|  +A   |     s1      |    2019    |   CA    | Vancouver |  2581000   |
|  +A   |     s1      |    2019    |   US    |  Seattle  |  3433000   |

`+A` in `op` column identifies the {{<term "Operation Type">}} and in this case all we have is `Append` operations.

Now let's say after a census in Vancouver our source data changes to:

```csv
Country,City,Population
2019,CA,Vancouver,2581000
2019,US,Seattle,3433000
2020,CA,Vancouver,2606000
```

So far this is a valid ledger data - history is preserved and changes are append-only.

Pulling the dataset will now result in the following history:

|   op   | system_time | event_time | country |     city      | population  |
| :----: | :---------: | :--------: | :-----: | :-----------: | :---------: |
|   +A   |     s1      |    2019    |   CA    |   Vancouver   |   2581000   |
|   +A   |     s1      |    2019    |   US    |    Seattle    |   3433000   |
| **+A** |   **s1**    |  **2020**  | **CA**  | **Vancouver** | **2606000** |

Note that the old events from 2019 were recognized as ones we already seen and were not added again.

## `Snapshot`
{{<schema "Snapshot" "MergeStrategy::Snapshot">}} strategy can be used for data exports that are taken periodically and contain only the latest state snapshot of the observed entity or system. Over time such exports can have new rows added, and old rows either removed or modified.

It's important to understand that publishers that use such formats **routinely lose information**. When a record in the database is updated, or one DB dump is replaced with another we not only lose the history of previous values, but you also lose the context of why those changes happened. This is a really bad default!

The `snapshot` strategy transforms such data sources into a history of changes by performing the [change data capture](https://en.wikipedia.org/wiki/Change_data_capture). It relies on a user-specified primary key to correlate the rows between the two snapshots.

A new event is added into the output stream whenever:

- A row with a certain primary key appears for the first time
- A row with a certain key disappears from the snapshot
- A row data associated with a certain key has changed

In case of removal or changes in data this strategy will issue explicit **retraction** (`-R`) and **correction** (`-C` / `+C`) events.

The Snapshot strategy also requires special treatment in regards to the event time. Since snapshot-style data exports represent the state of some system at a certain time - it is important to know what that time was. This time is usually captured in some form of metadata (e.g. in the name of the file, in the URL, or the HTTP caching headers. It should be possible to extract and propagate this time into a data column.

<!-- TODO: Describe event time sources --->

### Example <!-- omit in toc -->

Imagine a data publisher that exposes dataset with **current** populations of major cities around the world, for example:

```csv
Country,City,Population
CA,Vancouver,2581000
US,Seattle,3433000
```

This dataset is non-temporal (doesn't have any date/time columns), so it's a clear sign we're dealing with a `snapshot` data.

So we use the following root dataset manifest to ingest it:

```yaml
kind: DatasetSnapshot
version: 1
content:
  name: cities-population
  kind: Root
  metadata:
    - kind: SetPollingSource
      fetch:
        kind: Url
        url: https://...
        eventTime:
          kind: FromMetadata
      ...
      merge:
        kind: Snapshot
        primaryKey:
        - country
        - city
```

Notice that we specify `snapshot` merge strategy with composite primary key `(country, city)`. We also specify the `eventTime` of kind `FromMetadata`, instructing the ingest to use time from the caching headers as the event time of new records.

The resulting dataset when ingested will look like this:

|  op   | system_time | event_time | country |   city    | population |
| :---: | :---------: | :--------: | :-----: | :-------: | :--------: |
|  +A   |     s1      |     e1     |   CA    | Vancouver |  2581000   |
|  +A   |     s1      |     e1     |   US    |  Seattle  |  3433000   |

Notice that since it's the first time we ingested data both records have `op == '+A'` values, i.e. "append" operation.

Now let's say after a census in Vancouver our source data changes to:

```csv
Country,City,Population
CA,Vancouver,2606000
US,Seattle,3433000
```

Pulling the dataset will now result in the following history:

|   op   | system_time | event_time | country |     city      | population  |
| :----: | :---------: | :--------: | :-----: | :-----------: | :---------: |
|   +A   |     s1      |     e1     |   CA    |   Vancouver   |   2581000   |
|   +A   |     s1      |     e1     |   US    |    Seattle    |   3433000   |
| **-C** |   **s2**    |   **e1**   | **CA**  | **Vancouver** | **2581000** |
| **+C** |   **s2**    |   **e2**   | **CA**  | **Vancouver** | **2606000** |

The two added rows represent the `'-C' correct-from` event that carries the old value that was changed, and `'+C' correct-to` event that carries the new value that was observed. Similarly the `'-R' retract` event can be issued for a record that disappeared in the source data.

This model is extremely powerful, as it not only provides us the full history of how data was evolving over time, but allows all downstream computations to **automatically react to corrections and retractions**.


## `Append`
Under {{<schema "Append" "MergeStrategy::Append">}} strategy all observed input data will be appended to the Dataset in its original form, without any modifications.

This strategy is rarely used in datasets that poll data from a remote source, but can be useful for datasets that get data pushed into them (e.g. from an IoT device).
