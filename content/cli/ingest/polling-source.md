---
Title: Polling Sources
weight: 40
categories: []
aliases:
---

Polling sources are used for cases when external data is stored somewhere in bulk and we want to **periodically** synchronize its state with an ODF dataset.

Polling sources are suitable for ingesting data from:
- Periodic database dumps
- Data published as a set of files on the web
- Bulk data access APIs
- External systems using custom connector libraries.

## Source Metadata
Polling sources are defined via {{<schema "SetPollingSource">}} metadata event:

```yaml
---
kind: DatasetSnapshot
version: 1
content:
  name: com.example.city-populations
  kind: Root
  metadata:
    - kind: SetPollingSource
      # Where to fetch the data from.
      # Supports multiple protocols and file layouts
      fetch:
        kind: Url
        url: https://example.com/city_populations_over_time.zip
      # OPTIONAL: How to prepare the binary data
      # Includes decompression, file filtering, format conversions
      prepare:
        - kind: Decompress
          format: Zip
      # How to interpret the data.
      # Includes data format, schema to apply, error handling
      read:
        kind: Csv
        header: true
        schema:
          - "date DATE"
          - "city STRING"
          - "population STRING"
      # OPTIONAL: Pre-processing query that shapes the data.
      # Useful for converting text data into strict types
      preprocess:
        kind: Sql
        # Use one of the supported engines and a query in its dialect
        # See: https://docs.kamu.dev/cli/transform/supported-engines/
        engine: datafusion
        query: |
          select
            date,
            city,
            -- remove commas between thousands
            cast(replace(population, ",", "") as bigint)
          from input
      # How to combine data ingested in the past with the new data.
      merge:
        kind: Ledger
        primaryKey:
          - date
          - city
      # Lets you manipulate names of the system columns to avoid conflicts
      # or use names better suited for your data.
    - kind: SetVocab
      eventTimeColumn: date
```

The structure of the {{<schema "SetPollingSource">}} event directly reflects all the ingestion phases:
- `fetch` - specifies how to download the data from some external source (e.g. HTTP/FTP) and how to cache it efficiently
- `prepare` (optional) - specifies how to prepare raw binary data for reading (e.g. extracting an archive or converting between formats)
- `read` - specifies how to read the data into structured form (e.g. as CSV or Parquet)
- `preprocess` (optional) - allows to shape the structured data with queries (e.g. to parse and convert types into best suited form wit SQL)
- `merge` - specifies how to **combine the read data with the history of previously seen data** (this step is extremely important as it performs "ledgerization" / "historization" of the evolving state of data - see [Merge Strategies]({{<relref "merge-strategies">}}) section for explanation).

A polling source can later be deactivated using {{<schema "DisablePollingSource">}} event.

For multiple example of handling tricky data sources see [input formats]({{<relref "input-formats">}}) section.

## Polling Data via CLI
To poll data into dataset via `kamu` use the general-purpose [`kamu pull`]({{<relref "cli-reference#kamu-ingest">}}) command.

```sh
kamu pull com.example.city-populations
```

## Polling Data via API
See [Kamu Node protocols documentation]({{<relref "protocols">}}) for various options of polling data programmatically via APIs.

## Event Time
The perfect scenario for `kamu` is when data records contain {{<term "event time">}} within them as a column, but many data sources on the web are not like that.

If event time is not present in data - `kamu` will try to infer it. This can be:
- Modification time for files on local or remote file systems
- `Last-Modified` time for HTTP resources.

If no time can be extracted from the source - it will fall back to using {{<term "system time">}}.

Usually its best to be explicit about where your {{<term "event time">}} is coming by defining {{<schema "EventTimeSource">}} in the `fetch` section of {{<schema "SetPollingSource">}}. It's pretty flexible, allowing you to even extract time from timestamps that are part of file names:

```yaml
fetch:
  kind: FilesGlob
  # Ingest all files matching the pattern (in lexicographic order)
  path: /data/database-dump-*.json.gz
  eventTime:
    kind: FromPath
    # Extract timestamp as the first regex group in the pattern
    pattern: database-dump-(\d+-\d+-\d+)\.json\.gz
    # Parse timestamp
    timestampFormat: '%Y-%m-%d'
```

## Source Caching
`kamu` does its best to avoid redundant work and not ingest data if source was not updated since the lass poll.

Exact mechanism of cache control depends on the {{<schema "source type" "FetchStep">}} and the protocol used. In case of HTTP, for example, it will rely on standard HTTP caching headers like `ETag` and `Last-Modified`.

The latest caching information is stored in dataset metadata in {{<schema "AddData">}} event in a special {{<schema "SourceState">}} object. This means that it is possible for ingest to return no data and no new {{<term "watermark">}}, but still write a {{<term "metadata block" "metadata-chain">}} containing only the new source state.

You can control caching behavior via {{<schema "SourceCaching">}} object in the `fetch` section of {{<schema "SetPollingSource">}}.