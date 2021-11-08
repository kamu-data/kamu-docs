---
Title: Metadata Reference
description:
weight: 20
alwaysopen: false
categories: []
---

### Manifest Schema
An object that wraps the metadata resources providing versioning and type identification. All root-level resources are wrapped with a manifest when serialized to disk.

| Property  |   Type    | Required | Format | Description                                                                                                                                |
| :-------: | :-------: | :------: | :----: | ------------------------------------------------------------------------------------------------------------------------------------------ |
| `version` | `integer` |          |        | Major version number of the resource contained in this manifest. It provides the mechanism for introducing compatibility breaking changes. |
|  `kind`   | `string`  |    V     |        | Type name of the resource.                                                                                                                 |
| `content` | `object`  |    V     |        | Resource data.                                                                                                                             |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://github.com/kamu-data/open-data-fabric/blob/master/schemas/Manifest.json)
[![JSON Schema](https://img.shields.io/badge/schema-flatbuffers-blue)](https://github.com/kamu-data/open-data-fabric/blob/master/schemas/flatbuffers/opendatafabric.fbs)

### DatasetSnapshot Schema
Represents a snapshot of the dataset definition in a single point in time.
This type is typically used for defining new datasets and changing the existing ones.

| Property |                      Type                      | Required |    Format    | Description                                                                       |
| :------: | :--------------------------------------------: | :------: | :----------: | --------------------------------------------------------------------------------- |
|   `id`   |                    `string`                    |    V     | `dataset-id` | Unique identifier of the dataset                                                  |
| `source` |     [DatasetSource](#datasetsource-schema)     |    V     |              | Contains information about the source of the data and/or applied transformations. |
| `vocab`  | [DatasetVocabulary](#datasetvocabulary-schema) |          |              | Vocabulary lets you manipulate system column names to avoid conflicts.            |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://github.com/kamu-data/open-data-fabric/blob/master/schemas/DatasetSnapshot.json)
[![JSON Schema](https://img.shields.io/badge/schema-flatbuffers-blue)](https://github.com/kamu-data/open-data-fabric/blob/master/schemas/flatbuffers/opendatafabric.fbs)

### DatasetSource Schema
Defines the source of data within a dataset.

Union type:
- [DatasetSource::Root](#datasetsourceroot-schema)
- [DatasetSource::Derivative](#datasetsourcederivative-schema)

#### DatasetSource::Root Schema
Root sources are the points of entry of external data into the system.

Root source includes information like:
- Where to fetch the data from - e.g. source URL, a protocol to use, cache control
- How to prepare the binary data - e.g. decompression, file filtering, format conversions
- How to interpret the data - e.g. data format, schema to apply, error handling
- How to combine data ingested in the past with the new data - e.g. append as log or diff as a snapshot of the current state.

|   Property   |                  Type                  | Required | Format | Description                                                                |
| :----------: | :------------------------------------: | :------: | :----: | -------------------------------------------------------------------------- |
|   `fetch`    |     [FetchStep](#fetchstep-schema)     |    V     |        | Determines where data is sourced from.                                     |
|  `prepare`   |  array([PrepStep](#prepstep-schema))   |          |        | Defines how raw data is prepared before reading.                           |
|    `read`    |      [ReadStep](#readstep-schema)      |    V     |        | Defines how data is read into structured format.                           |
| `preprocess` |     [Transform](#transform-schema)     |          |        | Pre-processing query that shapes the data.                                 |
|   `merge`    | [MergeStrategy](#mergestrategy-schema) |    V     |        | Determines how newly-ingested data should be merged with existing history. |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://github.com/kamu-data/open-data-fabric/blob/master/schemas/DatasetSource.json)
[![JSON Schema](https://img.shields.io/badge/schema-flatbuffers-blue)](https://github.com/kamu-data/open-data-fabric/blob/master/schemas/flatbuffers/opendatafabric.fbs)

#### DatasetSource::Derivative Schema
Derivative sources produce data by transforming and combining one or multiple existing datasets.

|  Property   |              Type              | Required | Format | Description                                               |
| :---------: | :----------------------------: | :------: | :----: | --------------------------------------------------------- |
|  `inputs`   |        array(`string`)         |    V     |        | Identifiers of the datasets that will be used as sources. |
| `transform` | [Transform](#transform-schema) |    V     |        | Transformation that will be applied to produce new data   |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://github.com/kamu-data/open-data-fabric/blob/master/schemas/DatasetSource.json)
[![JSON Schema](https://img.shields.io/badge/schema-flatbuffers-blue)](https://github.com/kamu-data/open-data-fabric/blob/master/schemas/flatbuffers/opendatafabric.fbs)


### ReadStep Schema
Defines how raw data should be read into the structured form.

Union type:
- [ReadStep::Csv](#readstepcsv-schema)
- [ReadStep::JsonLines](#readstepjsonlines-schema)
- [ReadStep::GeoJson](#readstepgeojson-schema)
- [ReadStep::EsriShapefile](#readstepesrishapefile-schema)

#### ReadStep::Csv Schema
Reader for comma-separated files.

|          Property          |      Type       | Required | Format | Description                                                                                                                                                                                                                                                                                    |
| :------------------------: | :-------------: | :------: | :----: | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
|          `schema`          | array(`string`) |          |        | A DDL-formatted schema. Schema can be used to coerce values into more appropriate data types.                                                                                                                                                                                                  |
|        `separator`         |    `string`     |          |        | Sets a single character as a separator for each field and value.                                                                                                                                                                                                                               |
|         `encoding`         |    `string`     |          |        | Decodes the CSV files by the given encoding type.                                                                                                                                                                                                                                              |
|          `quote`           |    `string`     |          |        | Sets a single character used for escaping quoted values where the separator can be part of the value. Set an empty string to turn off quotations.                                                                                                                                              |
|          `escape`          |    `string`     |          |        | Sets a single character used for escaping quotes inside an already quoted value.                                                                                                                                                                                                               |
|         `comment`          |    `string`     |          |        | Sets a single character used for skipping lines beginning with this character.                                                                                                                                                                                                                 |
|          `header`          |    `boolean`    |          |        | Use the first line as names of columns.                                                                                                                                                                                                                                                        |
|      `enforceSchema`       |    `boolean`    |          |        | If it is set to true, the specified or inferred schema will be forcibly applied to datasource files, and headers in CSV files will be ignored. If the option is set to false, the schema will be validated against all headers in CSV files in the case when the header option is set to true. |
|       `inferSchema`        |    `boolean`    |          |        | Infers the input schema automatically from data. It requires one extra pass over the data.                                                                                                                                                                                                     |
| `ignoreLeadingWhiteSpace`  |    `boolean`    |          |        | A flag indicating whether or not leading whitespaces from values being read should be skipped.                                                                                                                                                                                                 |
| `ignoreTrailingWhiteSpace` |    `boolean`    |          |        | A flag indicating whether or not trailing whitespaces from values being read should be skipped.                                                                                                                                                                                                |
|        `nullValue`         |    `string`     |          |        | Sets the string representation of a null value.                                                                                                                                                                                                                                                |
|        `emptyValue`        |    `string`     |          |        | Sets the string representation of an empty value.                                                                                                                                                                                                                                              |
|         `nanValue`         |    `string`     |          |        | Sets the string representation of a non-number value.                                                                                                                                                                                                                                          |
|       `positiveInf`        |    `string`     |          |        | Sets the string representation of a positive infinity value.                                                                                                                                                                                                                                   |
|       `negativeInf`        |    `string`     |          |        | Sets the string representation of a negative infinity value.                                                                                                                                                                                                                                   |
|        `dateFormat`        |    `string`     |          |        | Sets the string that indicates a date format.                                                                                                                                                                                                                                                  |
|     `timestampFormat`      |    `string`     |          |        | Sets the string that indicates a timestamp format.                                                                                                                                                                                                                                             |
|        `multiLine`         |    `boolean`    |          |        | Parse one record, which may span multiple lines.                                                                                                                                                                                                                                               |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://github.com/kamu-data/open-data-fabric/blob/master/schemas/ReadStep.json)
[![JSON Schema](https://img.shields.io/badge/schema-flatbuffers-blue)](https://github.com/kamu-data/open-data-fabric/blob/master/schemas/flatbuffers/opendatafabric.fbs)

#### ReadStep::JsonLines Schema
Reader for files containing concatenation of multiple JSON records with the same schema.

|       Property       |      Type       | Required | Format | Description                                                                                   |
| :------------------: | :-------------: | :------: | :----: | --------------------------------------------------------------------------------------------- |
|       `schema`       | array(`string`) |          |        | A DDL-formatted schema. Schema can be used to coerce values into more appropriate data types. |
|     `dateFormat`     |    `string`     |          |        | Sets the string that indicates a date format.                                                 |
|      `encoding`      |    `string`     |          |        | Allows to forcibly set one of standard basic or extended encoding.                            |
|     `multiLine`      |    `boolean`    |          |        | Parse one record, which may span multiple lines, per file.                                    |
| `primitivesAsString` |    `boolean`    |          |        | Infers all primitive values as a string type.                                                 |
|  `timestampFormat`   |    `string`     |          |        | Sets the string that indicates a timestamp format.                                            |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://github.com/kamu-data/open-data-fabric/blob/master/schemas/ReadStep.json)
[![JSON Schema](https://img.shields.io/badge/schema-flatbuffers-blue)](https://github.com/kamu-data/open-data-fabric/blob/master/schemas/flatbuffers/opendatafabric.fbs)

#### ReadStep::GeoJson Schema
Reader for GeoJSON files.

| Property |      Type       | Required | Format | Description                                                                                   |
| :------: | :-------------: | :------: | :----: | --------------------------------------------------------------------------------------------- |
| `schema` | array(`string`) |          |        | A DDL-formatted schema. Schema can be used to coerce values into more appropriate data types. |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://github.com/kamu-data/open-data-fabric/blob/master/schemas/ReadStep.json)
[![JSON Schema](https://img.shields.io/badge/schema-flatbuffers-blue)](https://github.com/kamu-data/open-data-fabric/blob/master/schemas/flatbuffers/opendatafabric.fbs)

#### ReadStep::EsriShapefile Schema
Reader for ESRI Shapefile format.

| Property  |      Type       | Required | Format | Description                                                                                   |
| :-------: | :-------------: | :------: | :----: | --------------------------------------------------------------------------------------------- |
| `schema`  | array(`string`) |          |        | A DDL-formatted schema. Schema can be used to coerce values into more appropriate data types. |
| `subPath` |    `string`     |          |        | Path to a data file within a multi-file archive. Can contain glob patterns.                   |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://github.com/kamu-data/open-data-fabric/blob/master/schemas/ReadStep.json)
[![JSON Schema](https://img.shields.io/badge/schema-flatbuffers-blue)](https://github.com/kamu-data/open-data-fabric/blob/master/schemas/flatbuffers/opendatafabric.fbs)


### PrepStep Schema
Defines the steps to prepare raw data for ingestion.

Union type:
- [PrepStep::Decompress](#prepstepdecompress-schema)
- [PrepStep::Pipe](#prepsteppipe-schema)

#### PrepStep::Decompress Schema
Pulls data from one of the supported sources by its URL.

| Property  |   Type   | Required | Format | Description                                                                 |
| :-------: | :------: | :------: | :----: | --------------------------------------------------------------------------- |
| `format`  | `string` |    V     |        | Name of a compression algorithm used on data.                               |
| `subPath` | `string` |          |        | Path to a data file within a multi-file archive. Can contain glob patterns. |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://github.com/kamu-data/open-data-fabric/blob/master/schemas/PrepStep.json)
[![JSON Schema](https://img.shields.io/badge/schema-flatbuffers-blue)](https://github.com/kamu-data/open-data-fabric/blob/master/schemas/flatbuffers/opendatafabric.fbs)

#### PrepStep::Pipe Schema
Executes external command to process the data using piped input/output.

| Property  |      Type       | Required | Format | Description                           |
| :-------: | :-------------: | :------: | :----: | ------------------------------------- |
| `command` | array(`string`) |    V     |        | Command to execute and its arguments. |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://github.com/kamu-data/open-data-fabric/blob/master/schemas/PrepStep.json)
[![JSON Schema](https://img.shields.io/badge/schema-flatbuffers-blue)](https://github.com/kamu-data/open-data-fabric/blob/master/schemas/flatbuffers/opendatafabric.fbs)


### FetchStep Schema
Defines the external source of data.

Union type:
- [FetchStep::Url](#fetchstepurl-schema)
- [FetchStep::FilesGlob](#fetchstepfilesglob-schema)

#### FetchStep::Url Schema
Pulls data from one of the supported sources by its URL.

|  Property   |                    Type                    | Required | Format | Description                                                     |
| :---------: | :----------------------------------------: | :------: | :----: | --------------------------------------------------------------- |
|    `url`    |                  `string`                  |    V     | `url`  | URL of the data source                                          |
| `eventTime` | [EventTimeSource](#eventtimesource-schema) |          |        | Describes how event time is extracted from the source metadata. |
|   `cache`   |   [SourceCaching](#sourcecaching-schema)   |          |        | Describes the caching settings used for this source.            |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://github.com/kamu-data/open-data-fabric/blob/master/schemas/FetchStep.json)
[![JSON Schema](https://img.shields.io/badge/schema-flatbuffers-blue)](https://github.com/kamu-data/open-data-fabric/blob/master/schemas/flatbuffers/opendatafabric.fbs)

#### FetchStep::FilesGlob Schema
Uses glob operator to match files on the local file system.

|  Property   |                    Type                    | Required | Format | Description                                                     |
| :---------: | :----------------------------------------: | :------: | :----: | --------------------------------------------------------------- |
|   `path`    |                  `string`                  |    V     |        | Path with a glob pattern.                                       |
| `eventTime` | [EventTimeSource](#eventtimesource-schema) |          |        | Describes how event time is extracted from the source metadata. |
|   `cache`   |   [SourceCaching](#sourcecaching-schema)   |          |        | Describes the caching settings used for this source.            |
|   `order`   |                  `string`                  |          |        | Specifies how input files should be ordered before ingestion.   |
Order is important as every file will be processed individually
and will advance the dataset's watermark. |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://github.com/kamu-data/open-data-fabric/blob/master/schemas/FetchStep.json)
[![JSON Schema](https://img.shields.io/badge/schema-flatbuffers-blue)](https://github.com/kamu-data/open-data-fabric/blob/master/schemas/flatbuffers/opendatafabric.fbs)


### Transform Schema
Engine-specific processing queries that shape the resulting data.

Union type:
- [Transform::Sql](#transformsql-schema)

#### Transform::Sql Schema
Transform using one of the SQL dialects.

|     Property     |                     Type                      | Required | Format | Description                                                                                                                                                    |
| :--------------: | :-------------------------------------------: | :------: | :----: | -------------------------------------------------------------------------------------------------------------------------------------------------------------- |
|     `engine`     |                   `string`                    |    V     |        | Identifier of the engine used for this transformation.                                                                                                         |
|    `version`     |                   `string`                    |          |        | Version of the engine to use.                                                                                                                                  |
|     `query`      |                   `string`                    |          |        | SQL query the result of which will be used as an output.                                                                                                       |
|    `queries`     |  array([SqlQueryStep](#sqlquerystep-schema))  |          |        | Use this instead of query field for specifying multi-step SQL transformations. Each step acts as a shorthand for `CREATE TEMPORARY VIEW <alias> AS (<query>)`. |
| `temporalTables` | array([TemporalTable](#temporaltable-schema)) |          |        | Temporary Flink-specific extension for creating temporal tables from streams.                                                                                  |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://github.com/kamu-data/open-data-fabric/blob/master/schemas/Transform.json)
[![JSON Schema](https://img.shields.io/badge/schema-flatbuffers-blue)](https://github.com/kamu-data/open-data-fabric/blob/master/schemas/flatbuffers/opendatafabric.fbs)


### MergeStrategy Schema
Merge strategy determines how newly ingested data should be combined with the data that already exists in the dataset.

Union type:
- [MergeStrategy::Append](#mergestrategyappend-schema)
- [MergeStrategy::Ledger](#mergestrategyledger-schema)
- [MergeStrategy::Snapshot](#mergestrategysnapshot-schema)

#### MergeStrategy::Append Schema
Append merge strategy.

Under this strategy polled data will be appended in its original form to the already ingested data without modifications.

| Property | Type  | Required | Format | Description |
| :------: | :---: | :------: | :----: | ----------- |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://github.com/kamu-data/open-data-fabric/blob/master/schemas/MergeStrategy.json)
[![JSON Schema](https://img.shields.io/badge/schema-flatbuffers-blue)](https://github.com/kamu-data/open-data-fabric/blob/master/schemas/flatbuffers/opendatafabric.fbs)

#### MergeStrategy::Ledger Schema
Ledger merge strategy.

This strategy should be used for data sources containing append-only event
streams. New data dumps can have new rows added, but once data already
made it into one dump it never changes or disappears.

A system time column will be added to the data to indicate the time
when the record was observed first by the system.

It relies on a user-specified primary key columns to identify which records
were already seen and not duplicate them.

It will always preserve all columns from existing and new snapshots, so
the set of columns can only grow.

|   Property   |      Type       | Required | Format | Description                                                                    |
| :----------: | :-------------: | :------: | :----: | ------------------------------------------------------------------------------ |
| `primaryKey` | array(`string`) |    V     |        | Names of the columns that uniquely identify the record throughout its lifetime |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://github.com/kamu-data/open-data-fabric/blob/master/schemas/MergeStrategy.json)
[![JSON Schema](https://img.shields.io/badge/schema-flatbuffers-blue)](https://github.com/kamu-data/open-data-fabric/blob/master/schemas/flatbuffers/opendatafabric.fbs)

#### MergeStrategy::Snapshot Schema
Snapshot merge strategy.

This strategy can be used for data dumps that are taken periodical
and contain only the latest state of the observed entity or system.
Over time such dumps can have new rows added, and old rows either removed
or modified.

This strategy transforms snapshot data into an append-only event stream
where data already added is immutable. It does so by treating rows in
snapshots as "observation" events and adding an "observed" column
that will contain:
  - "I" - when a row appears for the first time
  - "D" - when row disappears
  - "U" - whenever any row data has changed

It relies on a user-specified primary key columns to correlate the rows
between the two snapshots.

The time when a snapshot was taken (event time) is usually captured in some
form of metadata (e.g. in the name of the snapshot file, or in the caching
headers). In order to populate the event time we rely on the `FetchStep`
to extract the event time from metadata. User then should specify the name
of the event time column that will be populated from this value.

If the data contains a column that is guaranteed to change whenever
any of the data columns changes (for example this can be a last
modification timestamp, an incremental version, or a data hash), then
it can be specified as modification indicator to speed up the detection of
modified rows.

Schema Changes:

This strategy will always preserve all columns from the existing and new snapshots, so the set of columns can only grow.

|      Property       |      Type       | Required | Format | Description                                                                                                                    |
| :-----------------: | :-------------: | :------: | :----: | ------------------------------------------------------------------------------------------------------------------------------ |
|    `primaryKey`     | array(`string`) |    V     |        | Names of the columns that uniquely identify the record throughout its lifetime.                                                |
|  `compareColumns`   | array(`string`) |          |        | Names of the columns to compared to determine if a row has changed between two snapshots.                                      |
| `observationColumn` |    `string`     |          |        | Name of the observation type column that will be added to the data.                                                            |
|     `obsvAdded`     |    `string`     |          |        | Name of the observation type when the data with certain primary key is seen for the first time.                                |
|    `obsvChanged`    |    `string`     |          |        | Name of the observation type when the data with certain primary key has changed compared to the last time it was seen.         |
|    `obsvRemoved`    |    `string`     |          |        | Name of the observation type when the data with certain primary key has been seen before but now is missing from the snapshot. |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://github.com/kamu-data/open-data-fabric/blob/master/schemas/MergeStrategy.json)
[![JSON Schema](https://img.shields.io/badge/schema-flatbuffers-blue)](https://github.com/kamu-data/open-data-fabric/blob/master/schemas/flatbuffers/opendatafabric.fbs)


### DatasetVocabulary Schema
Lets you manipulate names of the system columns to avoid conflicts.

|      Property      |   Type   | Required | Format | Description                     |
| :----------------: | :------: | :------: | :----: | ------------------------------- |
| `systemTimeColumn` | `string` |          |        | Name of the system time column. |
| `eventTimeColumn`  | `string` |          |        | Name of the event time column.  |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://github.com/kamu-data/open-data-fabric/blob/master/schemas/DatasetVocabulary.json)
[![JSON Schema](https://img.shields.io/badge/schema-flatbuffers-blue)](https://github.com/kamu-data/open-data-fabric/blob/master/schemas/flatbuffers/opendatafabric.fbs)

### MetadataBlock Schema
An individual block in the metadata chain that captures the history of modifications of a dataset.

|     Property      |                      Type                      | Required |                                              Format                                              | Description                                                                                                                                                                                                                                                                                                                                                   |
| :---------------: | :--------------------------------------------: | :------: | :----------------------------------------------------------------------------------------------: | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
|    `blockHash`    |                    `string`                    |    V     |                                            `sha3-256`                                            | Hash sum of this metadata block's information.                                                                                                                                                                                                                                                                                                                |
|  `prevBlockHash`  |                    `string`                    |          |                                            `sha3-256`                                            | Hash sum of the preceding block.                                                                                                                                                                                                                                                                                                                              |
|   `systemTime`    |                    `string`                    |    V     | [date-time](https://json-schema.org/draft/2019-09/json-schema-validation.html#rfc.section.7.3.1) | System time when this block was written.                                                                                                                                                                                                                                                                                                                      |
|   `outputSlice`   |         [DataSlice](#dataslice-schema)         |          |                                                                                                  | Properties of output data written during this update, if any.                                                                                                                                                                                                                                                                                                 |
| `outputWatermark` |                    `string`                    |          | [date-time](https://json-schema.org/draft/2019-09/json-schema-validation.html#rfc.section.7.3.1) | Last watermark of the output data stream. Watermarks are usually derived from the event times in data based on the properties of the source, but sometimes they can also be assigned manually. Manual watermarks are useful in cases of slow-moving datasets in order to let the computations continue even when no new events were observed for a long time. |
|   `inputSlices`   |     array([DataSlice](#dataslice-schema))      |          |                                                                                                  | Defines input datasets and their data slices used in this block, if any.                                                                                                                                                                                                                                                                                      |
|     `source`      |     [DatasetSource](#datasetsource-schema)     |          |                                                                                                  | Contains the definition of the source of data when it changes.                                                                                                                                                                                                                                                                                                |
|      `vocab`      | [DatasetVocabulary](#datasetvocabulary-schema) |          |                                                                                                  | Vocabulary lets you change system column names to avoid conflicts.                                                                                                                                                                                                                                                                                            |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://github.com/kamu-data/open-data-fabric/blob/master/schemas/MetadataBlock.json)
[![JSON Schema](https://img.shields.io/badge/schema-flatbuffers-blue)](https://github.com/kamu-data/open-data-fabric/blob/master/schemas/flatbuffers/opendatafabric.fbs)

### DataSlice Schema
Defines a subset of data in a dataset

|   Property   |   Type    | Required |        Format        | Description                                              |
| :----------: | :-------: | :------: | :------------------: | -------------------------------------------------------- |
|    `hash`    | `string`  |    V     |      `sha3-256`      | Hash sum of the data in this slice                       |
|  `interval`  | `string`  |    V     | `date-time-interval` | Defines the system time boundaries of data in this slice |
| `numRecords` | `integer` |    V     |       `int64`        | Number of records in this slice                          |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://github.com/kamu-data/open-data-fabric/blob/master/schemas/DataSlice.json)
[![JSON Schema](https://img.shields.io/badge/schema-flatbuffers-blue)](https://github.com/kamu-data/open-data-fabric/blob/master/schemas/flatbuffers/opendatafabric.fbs)

### EventTimeSource Schema
Defines the external source of data.

Union type:
- [EventTimeSource::FromMetadata](#eventtimesourcefrommetadata-schema)
- [EventTimeSource::FromPath](#eventtimesourcefrompath-schema)

#### EventTimeSource::FromMetadata Schema
Extracts event time from the source's metadata.

| Property | Type  | Required | Format | Description |
| :------: | :---: | :------: | :----: | ----------- |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://github.com/kamu-data/open-data-fabric/blob/master/schemas/EventTimeSource.json)
[![JSON Schema](https://img.shields.io/badge/schema-flatbuffers-blue)](https://github.com/kamu-data/open-data-fabric/blob/master/schemas/flatbuffers/opendatafabric.fbs)

#### EventTimeSource::FromPath Schema
Extracts event time from the path component of the source.

|     Property      |   Type   | Required | Format  | Description                                                          |
| :---------------: | :------: | :------: | :-----: | -------------------------------------------------------------------- |
|     `pattern`     | `string` |    V     | `regex` | Regular expression where first group contains the timestamp string.  |
| `timestampFormat` | `string` |          |         | Format of the expected timestamp in java.text.SimpleDateFormat form. |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://github.com/kamu-data/open-data-fabric/blob/master/schemas/EventTimeSource.json)
[![JSON Schema](https://img.shields.io/badge/schema-flatbuffers-blue)](https://github.com/kamu-data/open-data-fabric/blob/master/schemas/flatbuffers/opendatafabric.fbs)


### SourceCaching Schema
Defines the external source of data.

Union type:
- [SourceCaching::Forever](#sourcecachingforever-schema)

#### SourceCaching::Forever Schema
After source was processed once it will never be ingested again.

| Property | Type  | Required | Format | Description |
| :------: | :---: | :------: | :----: | ----------- |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://github.com/kamu-data/open-data-fabric/blob/master/schemas/SourceCaching.json)
[![JSON Schema](https://img.shields.io/badge/schema-flatbuffers-blue)](https://github.com/kamu-data/open-data-fabric/blob/master/schemas/flatbuffers/opendatafabric.fbs)
