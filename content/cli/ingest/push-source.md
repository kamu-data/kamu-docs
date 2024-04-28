---
Title: Push Sources
weight: 30
categories: []
aliases:
---

Push sources are used in cases when some external actor actively sends data into a dataset.

Push sources are suitable for:
- IoT devices that periodically send data
- Business processes that report events directly into ODF dataset
- For ingesting data from streaming data APIs and event queues like [Apache Kafka](https://kafka.apache.org/).


## Source Metadata
Push sources are added via {{<schema "AddPushSource">}} metadata event:

```yaml
kind: DatasetSnapshot
version: 1
content:
  name: gps
  kind: Root
  metadata:
    - kind: AddPushSource
      sourceName: default
      read:
        kind: NdJson
        schema:
          - t TIMESTAMP
          - long DOUBLE
          - lat DOUBLE
      merge:
        kind: Append
    - kind: SetVocab
      eventTimeColumn: t
```

Note that push sources are **named**:

```yaml
sourceName: default
```

This allows you to declare **multiple push sources per dataset**, which may be useful for situations where several devices from different manufacturers produce slightly different data, but you want them to be able to write directly to one dataset.

An existing push source can be deactivated using {{<schema "DisablePushSource">}} event.

Also note that, just like polling sources, push sources pass data through a [Merge Strategy]({{<relref "merge-strategies">}}), so they too can benefit, for example, from **event deduplication** of the {{<schema "Ledger" "MergeStrategy::Ledger">}} merge strategy.


## Pushing Data via CLI
To push data into dataset via `kamu` use [`kamu ingest`]({{<relref "cli-reference#kamu-ingest">}}) command.

You can push data from files:

```sh
echo '{"t": "2020-01-01T00:00:00Z", "long": -123.12, "lat": 49.28}' > data.json
kamu ingest gps data.json
```

Or from directly from STDIN:

```sh
echo '{"t": "2020-01-01T00:00:00Z", "long": -123.12, "lat": 49.28}' | kamu ingest gps --stdin
```

Result:

```sh
kamu tail gps
```
```sh
┌────────┬────┬──────────────────────────┬──────────────────────┬─────────┬───────┐
│ offset │ op │       system_time        │          t           │  long   │  lat  │
├────────┼────┼──────────────────────────┼──────────────────────┼─────────┼───────┤
│      0 │ +A │ 2024-01-31T03:51:03.618Z │ 2020-01-01T00:00:00Z │ -123.12 │ 49.28 │
└────────┴────┴──────────────────────────┴──────────────────────┴─────────┴───────┘
```

## Pushing Data via API
See [Kamu Node protocols documentation]({{<relref "protocols">}}) for various options of pushing data programmatically via APIs.

## Format Translation
While push sources define a specific {{<schema "read format" "ReadStep">}} for their data - there is some tolerance. For example you can push {{<schema "Csv" "ReadStep::Csv">}} data to the source that declares {{<schema "NdJson" "ReadStep::NdJson">}} format and `kamu` will attempt to read it using the same schema.

This behavior works both in CLI commands and in push APIs.
