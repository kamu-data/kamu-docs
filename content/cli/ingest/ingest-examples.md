---
Title: Examples
description:
weight: 30
categories: []
aliases:
---

# Compressed Data & Archives

Use `decompress` preparation step to extract data from `gzip`, `zip` archives.

```yaml
prepare:
- kind: decompress
  format: gzip
```

In case of a multi-file archive you can specify which file should be extracted:

```yaml
prepare:
- kind: decompress
  format: zip
  subPath: specific-file-*.csv  # Note: can contain glob patterns
```

See also: [PrepStep::Decompress](https://github.com/kamu-data/open-data-fabric/blob/master/open-data-fabric.md#prepstep-decompress-schema)

# CSV and Variants

Tab-separated file:

```yaml
read:
  kind: csv
  separator: "\t"
  quote: '"'
```

See also: [ReadStep::Csv](https://github.com/kamu-data/open-data-fabric/blob/master/open-data-fabric.md#readstep-csv-schema)

# JSON Document

A JSON document such as the following:

```json
{
    "values": [
        {"id": 1, "key": "value"},
        {"id": 2, "key": "value"},
    ]
}
```

Can be "flattened" into a columnar form and read using an external command (`jq` has to be installed on your system):

```yaml
prepare:
- kind: pipe
  command:
  - 'jq'
  - '-r'
  - '.values[] | [.id, .key] | @csv'
read:
  kind: csv
  schema:
  - id BIGINT
  - key STRING
```

# JSON Lines

JSONL, aka newline-delimited JSON file such as:

```json
{"id": 1, "key": "value"}
{"id": 2, "key": "value"}
```

Can be read using:

```yaml
read:
  kind: jsonLines
  schema:
  - id BIGINT
  - key STRING
```

See also: [ReadStep::JsonLines](https://github.com/kamu-data/open-data-fabric/blob/master/open-data-fabric.md#readstep-jsonlines-schema)

# Directory of Timestamped CSV files

The [FetchStep::FilesGlob](https://github.com/kamu-data/open-data-fabric/blob/master/open-data-fabric.md#fetchstep-filesglob-schema) is used in cases where directory contains a growing set of files. Files can be periodic snapshots of your database or represent batches of new data in a ledger. In either case file content should never change - once `kamu` processes a file it will not consider it again. It's OK for files to disappear - `kamu` will remember the name of the file it ingested last and will only consider files that are higher in order than that one (lexicographically based on file name, or based on event time as shown below).

In the example below data inside the files is in snapshot format, and to complicate things it does not itself contain an event time - the event time is written into the file's name.

Directory contents:

```bash
db-table-dump-2020-01-01.csv
db-table-dump-2020-01-02.csv
db-table-dump-2020-01-03.csv
```

Fetch step:

```yaml
fetch:
  kind: filesGlob
  path: /home/username/data/db-table-dump-*.csv
  eventTime:
    kind: fromPath
    pattern: 'db-table-dump-(\d+-\d+-\d+)\.csv'
    timestampFormat: '%Y-%m-%d'
  cache:
    kind: forever
```

# Esri Shapefile

```yaml
read:
  kind: esriShapefile
  subPath: specific_data.*
# Use preprocess to optionally convert between different projections
preprocess:
  kind: sql
  engine: spark
  query: >
    SELECT
      ST_Transform(geometry, "epsg:3157", "epsg:4326") as geometry,
      ...
    FROM input
```

# Need More Examples?

To give you more examples on how to deal with **different ingest scenarios** we've created an experimental repository where we publish Root Dataset manifests for a variety of Open Data sources - check out [kamu-contrib repo](https://github.com/kamu-data/kamu-contrib).
