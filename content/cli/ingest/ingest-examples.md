---
Title: Examples
description: Examples of handling tricky formats during ingestion
weight: 30
categories: []
aliases:
---

`kamu` supports multiple [data sources](https://github.com/open-data-fabric/open-data-fabric/blob/master/open-data-fabric.md#fetchstep-schema) and [data formats](https://github.com/open-data-fabric/open-data-fabric/blob/master/open-data-fabric.md#readstep) that in combination with custom [preparation steps](https://github.com/open-data-fabric/open-data-fabric/blob/master/open-data-fabric.md#prepstep-schema) can be used ingest all kinds of data.

Note that `kamu` is not intened to be or replace data masaging tool like Apache Airflow or Ni-Fi, or data extraction tool like Debezium. Utilities described below are here only to simplify the initial data ingestion step - the very first step in the data's journey through a web of structured stream processing pipelines.


# CSV Variants
You can customize a lot of formatting options for CSV format parser.

For example, a tab-separated file can be read as:

```yaml
read:
  kind: csv
  separator: "\t"
  quote: '"'
```

See: [ReadStep::Csv](https://github.com/kamu-data/open-data-fabric/blob/master/open-data-fabric.md#readstep-csv-schema)


# JSON Document
If you have a JSON document such as this:

```json
{
  "nested": {
    "values": [
        {"id": 1, "key": "value"},
        {"id": 2, "key": "value"},
    ]
  }
}
```

first consider if you can use [NDJSON](#ndjson) instead, as ordinary JSON documents cannot be split and read efficiently. 

If not, use:

```yaml
read:
  kind: json
  subPath: nested.values
```

Where `subPath` points at the array of records withing the document.

See: [ReadStep::Json](https://github.com/kamu-data/open-data-fabric/blob/master/open-data-fabric.md#readstep-json-schema)


# NDJSON
[NDJSON](https://ndjson.org/), aka newline-delimited JSON file such as:

```json
{"id": 1, "key": "value"}
{"id": 2, "key": "value"}
```

Can be read using:

```yaml
read:
  kind: ndJson
  schema:
  - id BIGINT
  - key STRING
```

See: [ReadStep::NdJson](https://github.com/kamu-data/open-data-fabric/blob/master/open-data-fabric.md#readstep-ndjson-schema)


# GeoJSON Document
Simply use:

```yaml
read:
  kind: geoJson
```

The reader expects one `FeatureCollection` object in the root and will create a record per each `Feature` inside it, extracting the properties into individual columns and leaving the feature `geometry` in its own column.

See: [ReadStep::GeoJson](https://github.com/kamu-data/open-data-fabric/blob/master/open-data-fabric.md#readstep-geojson-schema)


# NDGeoJSON Document
Simply use:

```yaml
read:
  kind: ndGeoJson
```

It is similar to [GeoJSON](#geojson-document) format but instead of `FeatureCollection` object in the root it expects every individual `Feature` to appear on its own line.

See: [ReadStep::NdGeoJson](https://github.com/kamu-data/open-data-fabric/blob/master/open-data-fabric.md#readstep-ndgeojson-schema)


# Esri Shapefile
GIS data in ESRI format can be read as:

```yaml
read:
  kind: esriShapefile
  subPath: specific_data-*.shp
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

See: [ReadStep::EsriShapefile](https://github.com/open-data-fabric/open-data-fabric/blob/master/open-data-fabric.md#readstep-esrishapefile-schema)


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

See: [PrepStep::Decompress](https://github.com/kamu-data/open-data-fabric/blob/master/open-data-fabric.md#prepstep-decompress-schema)


# Other Formats
If you have to work with formats that are not natively supported you'll need to transcode them.

Using the `pipe` preparation step you can specify a custom program or a script that will get data via STDIN and output result to STDOUT.

For example here's how transcoding a JSON document into CSV using `jq` may look like:

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

See: [PrepStep::Pipe](https://github.com/open-data-fabric/open-data-fabric/blob/master/open-data-fabric.md#prepstep-pipe-schema)


# Directory of Timestamped Files
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

See: [FetchStep::FilesGlob](https://github.com/open-data-fabric/open-data-fabric/blob/master/open-data-fabric.md#fetchstep-filesglob-schema)


# Dealing with API Keys

Sometimes you may want to parametrize the URL to include things like API keys and auth tokens. For this `kamu` supports basic variable substitution:

```yaml
fetch:
  kind: url
  url: "https://api.etherscan.io/api?apikey=${{ env.ETHERSCAN_API_KEY }}"
```

# Using Ingest Scripts
Sometimes you may need the power of a general purpose programming language to deal with particularly complex API, or when doing web scraping. For this `kamu` supports containerized ingestion tasks:

```yaml
fetch:
  kind: container
  image: "ghcr.io/kamu-data/fetch-my-dataset:0.1.0"
  env:
    - name: ETH_NODE_PROVIDER_URL
```

The specified container image is expected to conform to the following interface:
- Produce data to `stdout`
- Write warnings / errors to `sterr`
- Use following environment variables:
  - `ODF_LAST_MODIFIED` - last modified time of data from the previous ingest run, if any (in RFC3339 format)
  - `ODF_ETAG` - caching tag of data from the previous ingest run, if any
  - `ODF_NEW_LAST_MODIFIED_PATH` - path to a text file where ingest script may write new `Last-Modified` timestamp
  - `ODF_NEW_ETAG_PATH` - path to a text file where ingest script may write new `eTag`


# Need More Examples?
To give you more examples on how to deal with **different ingest scenarios** we've created an experimental repository where we publish Root Dataset manifests for a variety of Open Data sources - check out [kamu-contrib repo](https://github.com/kamu-data/kamu-contrib).
