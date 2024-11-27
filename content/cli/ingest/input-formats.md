---
Title: Input Formats
description: Examples of handling tricky formats during ingestion
weight: 20
categories: []
aliases:
  - /cli/ingest/ingest-examples
---

`kamu` supports multiple {{<schema "data sources" "FetchStep">}} and {{<schema "data formats" "ReadStep">}} that in combination with custom {{<schema "preparation steps" "PrepStep">}} can be used ingest all kinds of data.

Note that `kamu` is not made to be or replace data workflow tools like [Apache Airflow](https://airflow.apache.org/) or [Apache Ni-Fi](https://nifi.apache.org/), or data extraction tool like [Debezium](https://debezium.io/). Utilities described below are here only to simplify the initial data ingestion step - the very first step in the data's journey through a web of structured stream processing pipelines.


# CSV Variants
You can customize a lot of formatting options for CSV format parser.

For example, a tab-separated file can be read as:

```yaml
read:
  kind: Csv
  separator: "\t"
  quote: '"'
```

See: {{<schema "ReadStep::Csv">}}


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
  kind: Json
  subPath: nested.values
```

Where `subPath` points at the array of records withing the document.

See: {{<schema "ReadStep::Json">}}


# NDJSON
[NDJSON](https://ndjson.org/), aka newline-delimited JSON file such as:

```json
{"id": 1, "key": "value"}
{"id": 2, "key": "value"}
```

Can be read using:

```yaml
read:
  kind: NdJson
  schema:
  - id BIGINT
  - key STRING
```

See: {{<schema "ReadStep::NdJson">}}


# GeoJSON Document
Simply use:

```yaml
read:
  kind: GeoJson
```

The reader expects one `FeatureCollection` object in the root and will create a record per each `Feature` inside it, extracting the properties into individual columns and leaving the feature `geometry` in its own column.

See: {{<schema "ReadStep::GeoJson">}}


# NDGeoJSON Document
Simply use:

```yaml
read:
  kind: NdGeoJson
```

It is similar to [GeoJSON](#geojson-document) format but instead of `FeatureCollection` object in the root it expects every individual `Feature` to appear on its own line.

See: {{<schema "ReadStep::NdGeoJson">}}


# Esri Shapefile
GIS data in ESRI format can be read as:

```yaml
read:
  kind: EsriShapefile
  subPath: specific_data-*.shp
# Use preprocess to optionally convert between different projections
preprocess:
  kind: Sql
  engine: spark
  query: |
    SELECT
      ST_Transform(geometry, "epsg:3157", "epsg:4326") as geometry,
      ...
    FROM input
```

See: {{<schema "ReadStep::EsriShapefile">}}


# Compressed Data & Archives
Use `decompress` preparation step to extract data from `gzip`, `zip` archives.

```yaml
prepare:
- kind: Decompress
  format: Gzip
```

In case of a multi-file archive you can specify which file should be extracted:

```yaml
prepare:
- kind: Decompress
  format: Zip
  subPath: specific-file-*.csv  # Note: can contain glob patterns
```

See: {{<schema "PrepStep::Decompress">}}


# Other Formats
If you have to work with formats that are not natively supported you'll need to transcode them.

Using the `pipe` preparation step you can specify a custom program or a script that will get data via STDIN and output result to STDOUT.

For example here's how transcoding a JSON document into CSV using `jq` may look like:

```yaml
prepare:
- kind: Pipe
  command:
  - 'jq'
  - '-r'
  - '.values[] | [.id, .key] | @csv'
read:
  kind: Csv
  schema:
  - id BIGINT
  - key STRING
```

See: {{<schema "PrepStep::Pipe">}}


# Directory of Timestamped Files
The {{<schema "FetchStep::FilesGlob">}} is used in cases where directory contains a growing set of files. Files can be periodic snapshots of your database or represent batches of new data in a ledger. In either case file content should never change - once `kamu` processes a file it will not consider it again. It's OK for files to disappear - `kamu` will remember the name of the file it ingested last and will only consider files that are higher in order than that one (lexicographically based on file name, or based on event time as shown below).

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
  kind: FilesGlob
  path: /home/username/data/db-table-dump-*.csv
  eventTime:
    kind: FromPath
    pattern: 'db-table-dump-(\d+-\d+-\d+)\.csv'
    timestampFormat: '%Y-%m-%d'
  cache:
    kind: Forever
```

See: {{<schema "FetchStep::FilesGlob">}}


# Dealing with API Keys
Sometimes you may want to parametrize the URL to include things like API keys and auth tokens. For this `kamu` supports basic variable substitution:

```yaml
fetch:
  kind: Url
  url: "https://api.etherscan.io/api?apikey=${{ env.ETHERSCAN_API_KEY }}"
```

You can use default values for parameters:
```yaml
fetch:
  kind: Container
  image: "ghcr.io/kamu-data/fetch-com.defillama:0.1.5"
  args:
    - --request-interval
    - '${{ env.request_interval || 2 }}'
```

# Using Ingest Scripts
Sometimes you may need the power of a general purpose programming language to deal with particularly complex API, or when doing web scraping. For this `kamu` supports containerized ingestion tasks:

```yaml
fetch:
  kind: Container
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
  - `ODF_BATCH_SIZE` - is the recommended number of records, for ingest scripts that provide continuous stream of data and can resume from previous state
    - default value is 10 000, can be overridden via `env`
  - `ODF_NEW_LAST_MODIFIED_PATH` - path to a text file where ingest script may write new `Last-Modified` timestamp
  - `ODF_NEW_ETAG_PATH` - path to a text file where ingest script may write new `eTag`
  - `ODF_NEW_HAS_MORE_DATA_PATH` - path to a text file which ingest script can create to indicate about having more data for the next batch
    - **⚠️ Please note:** if the file is created, one of the following output marks must also be present: `eTag` or `Last-Modified` timestamp


# Need More Examples?
To give you more examples on how to deal with **different ingest scenarios** we've created an experimental repository where we publish Root Dataset manifests for a variety of Open Data sources - check out [kamu-contrib repo](https://github.com/kamu-data/kamu-contrib).
