---
# !!! THIS FILE IS AUTO-GENERATED - DO NOT MODIFY MANUALLY !!!
Title: Reference
description: Schemas of common metadata objects
weight: 20
categories: []
aliases:
---

<a name="reference-manifests"></a>
# Manifests
<a name="manifest-schema"></a>
## `Manifest`
An object that wraps the metadata resources providing versioning and type identification. All root-level resources are wrapped with a manifest when serialized to disk.

| Property | Type | Required | Format | Description |
| --- | --- | :---: | :---: | --- |
| `kind` | `string` | ✔️ | [`multicodec`](https://github.com/multiformats/multicodec) | Type of the resource. |
| `version` | `integer` | ✔️ |  | Major version number of the resource contained in this manifest. It provides the mechanism for introducing compatibility breaking changes. |
| `content` | `string` | ✔️ | [`flatbuffers`](https://flatbuffers.dev/) | Resource data. |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://github.com/open-data-fabric/open-data-fabric/tree/master/schemas/Manifest.json)
[![Flatbuffers Schema](https://img.shields.io/badge/schema-flatbuffers-blue)](https://github.com/open-data-fabric/open-data-fabric/tree/master/schemas-generated/flatbuffers/opendatafabric.fbs)

<a name="datasetsnapshot-schema"></a>
## `DatasetSnapshot`
Represents a projection of the dataset metadata at a single point in time.
This type is typically used for defining new datasets and changing the existing ones.

| Property | Type | Required | Format | Description |
| --- | --- | :---: | :---: | --- |
| `name` | `string` | ✔️ | [`dataset-alias`]({{<relref "spec#dataset-identity">}}) | Alias of the dataset. |
| `kind` | [`DatasetKind`](#datasetkind-schema) | ✔️ |  | Type of the dataset. |
| `metadata` | `array(`[`MetadataEvent`](#metadataevent-schema)`)` | ✔️ |  | An array of metadata events that will be used to populate the chain. Here you can define polling and push sources, set licenses, add attachments etc. |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://github.com/open-data-fabric/open-data-fabric/tree/master/schemas/DatasetSnapshot.json)
[![Flatbuffers Schema](https://img.shields.io/badge/schema-flatbuffers-blue)](https://github.com/open-data-fabric/open-data-fabric/tree/master/schemas-generated/flatbuffers/opendatafabric.fbs)

<a name="metadatablock-schema"></a>
## `MetadataBlock`
An individual block in the metadata chain that captures the history of modifications of a dataset.

| Property | Type | Required | Format | Description |
| --- | --- | :---: | :---: | --- |
| `systemTime` | `string` | ✔️ | [`date-time`](https://json-schema.org/draft/2019-09/json-schema-validation.html#rfc.section.7.3.1) | System time when this block was written. |
| `prevBlockHash` | `string` |  | [`multihash`](https://github.com/multiformats/multihash) | Hash sum of the preceding block. |
| `sequenceNumber` | `integer` | ✔️ | `uint64` | Block sequence number, starting from zero at the seed block. |
| `event` | [`MetadataEvent`](#metadataevent-schema) | ✔️ |  | Event data. |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://github.com/open-data-fabric/open-data-fabric/tree/master/schemas/MetadataBlock.json)
[![Flatbuffers Schema](https://img.shields.io/badge/schema-flatbuffers-blue)](https://github.com/open-data-fabric/open-data-fabric/tree/master/schemas-generated/flatbuffers/opendatafabric.fbs)

<a name="reference-metadata-events"></a>
# Metadata Events
<a name="metadataevent-schema"></a>
## `MetadataEvent`
Represents a transaction that occurred on a dataset.

| Union Type | Description |
| --- | --- |
| [`AddData`](#adddata-schema) | Indicates that data has been ingested into a root dataset. |
| [`ExecuteTransform`](#executetransform-schema) | Indicates that derivative transformation has been performed. |
| [`Seed`](#seed-schema) | Establishes the identity of the dataset. Always the first metadata event in the chain. |
| [`SetPollingSource`](#setpollingsource-schema) | Contains information on how externally-hosted data can be ingested into the root dataset. |
| [`SetTransform`](#settransform-schema) | Defines a transformation that produces data in a derivative dataset. |
| [`SetVocab`](#setvocab-schema) | Lets you manipulate names of the system columns to avoid conflicts. |
| [`SetAttachments`](#setattachments-schema) | Associates a set of files with this dataset. |
| [`SetInfo`](#setinfo-schema) | Provides basic human-readable information about a dataset. |
| [`SetLicense`](#setlicense-schema) | Defines a license that applies to this dataset. |
| [`SetDataSchema`](#setdataschema-schema) | Specifies the complete schema of Data Slices added to the Dataset following this event. |
| [`AddPushSource`](#addpushsource-schema) | Describes how to ingest data into a root dataset from a certain logical source. |
| [`DisablePushSource`](#disablepushsource-schema) | Disables the previously defined source. |
| [`DisablePollingSource`](#disablepollingsource-schema) | Disables the previously defined polling source. |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://github.com/open-data-fabric/open-data-fabric/tree/master/schemas/metadata-events/MetadataEvent.json)
[![Flatbuffers Schema](https://img.shields.io/badge/schema-flatbuffers-blue)](https://github.com/open-data-fabric/open-data-fabric/tree/master/schemas-generated/flatbuffers/opendatafabric.fbs)


<a name="adddata-schema"></a>
## `AddData`
Indicates that data has been ingested into a root dataset.

| Property | Type | Required | Format | Description |
| --- | --- | :---: | :---: | --- |
| `prevCheckpoint` | `string` |  | [`multihash`](https://github.com/multiformats/multihash) | Hash of the checkpoint file used to restore ingestion state, if any. |
| `prevOffset` | `integer` |  | `uint64` | Last offset of the previous data slice, if any. Must be equal to the last non-empty `newData.offsetInterval.end`. |
| `newData` | [`DataSlice`](#dataslice-schema) |  |  | Describes output data written during this transaction, if any. |
| `newCheckpoint` | [`Checkpoint`](#checkpoint-schema) |  |  | Describes checkpoint written during this transaction, if any. If an engine operation resulted in no updates to the checkpoint, but checkpoint is still relevant for subsequent runs - a hash of the previous checkpoint should be specified. |
| `newWatermark` | `string` |  | [`date-time`](https://json-schema.org/draft/2019-09/json-schema-validation.html#rfc.section.7.3.1) | Last watermark of the output data stream, if any. Initial blocks may not have watermarks, but once watermark is set - all subsequent blocks should either carry the same watermark or specify a new (greater) one. Thus, watermarks are monotonically non-decreasing. |
| `newSourceState` | [`SourceState`](#sourcestate-schema) |  |  | The state of the source the data was added from to allow fast resuming. If the state did not change but is still relevant for subsequent runs it should be carried, i.e. only the last state per source is considered when resuming. |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://github.com/open-data-fabric/open-data-fabric/tree/master/schemas/metadata-events/AddData.json)
[![Flatbuffers Schema](https://img.shields.io/badge/schema-flatbuffers-blue)](https://github.com/open-data-fabric/open-data-fabric/tree/master/schemas-generated/flatbuffers/opendatafabric.fbs)

<a name="addpushsource-schema"></a>
## `AddPushSource`
Describes how to ingest data into a root dataset from a certain logical source.

| Property | Type | Required | Format | Description |
| --- | --- | :---: | :---: | --- |
| `sourceName` | `string` | ✔️ |  | Identifies the source within this dataset. |
| `read` | [`ReadStep`](#readstep-schema) | ✔️ |  | Defines how data is read into structured format. |
| `preprocess` | [`Transform`](#transform-schema) |  |  | Pre-processing query that shapes the data. |
| `merge` | [`MergeStrategy`](#mergestrategy-schema) | ✔️ |  | Determines how newly-ingested data should be merged with existing history. |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://github.com/open-data-fabric/open-data-fabric/tree/master/schemas/metadata-events/AddPushSource.json)
[![Flatbuffers Schema](https://img.shields.io/badge/schema-flatbuffers-blue)](https://github.com/open-data-fabric/open-data-fabric/tree/master/schemas-generated/flatbuffers/opendatafabric.fbs)

<a name="disablepollingsource-schema"></a>
## `DisablePollingSource`
Disables the previously defined polling source.

| Property | Type | Required | Format | Description |
| --- | --- | :---: | :---: | --- |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://github.com/open-data-fabric/open-data-fabric/tree/master/schemas/metadata-events/DisablePollingSource.json)
[![Flatbuffers Schema](https://img.shields.io/badge/schema-flatbuffers-blue)](https://github.com/open-data-fabric/open-data-fabric/tree/master/schemas-generated/flatbuffers/opendatafabric.fbs)

<a name="disablepushsource-schema"></a>
## `DisablePushSource`
Disables the previously defined source.

| Property | Type | Required | Format | Description |
| --- | --- | :---: | :---: | --- |
| `sourceName` | `string` | ✔️ |  | Identifies the source to be disabled. |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://github.com/open-data-fabric/open-data-fabric/tree/master/schemas/metadata-events/DisablePushSource.json)
[![Flatbuffers Schema](https://img.shields.io/badge/schema-flatbuffers-blue)](https://github.com/open-data-fabric/open-data-fabric/tree/master/schemas-generated/flatbuffers/opendatafabric.fbs)

<a name="executetransform-schema"></a>
## `ExecuteTransform`
Indicates that derivative transformation has been performed.

| Property | Type | Required | Format | Description |
| --- | --- | :---: | :---: | --- |
| `queryInputs` | `array(`[`ExecuteTransformInput`](#executetransforminput-schema)`)` | ✔️ |  | Defines inputs used in this transaction. Slices corresponding to every input dataset must be present. |
| `prevCheckpoint` | `string` |  | [`multihash`](https://github.com/multiformats/multihash) | Hash of the checkpoint file used to restore transformation state, if any. |
| `prevOffset` | `integer` |  | `uint64` | Last offset of the previous data slice, if any. Must be equal to the last non-empty `newData.offsetInterval.end`. |
| `newData` | [`DataSlice`](#dataslice-schema) |  |  | Describes output data written during this transaction, if any. |
| `newCheckpoint` | [`Checkpoint`](#checkpoint-schema) |  |  | Describes checkpoint written during this transaction, if any. If an engine operation resulted in no updates to the checkpoint, but checkpoint is still relevant for subsequent runs - a hash of the previous checkpoint should be specified. |
| `newWatermark` | `string` |  | [`date-time`](https://json-schema.org/draft/2019-09/json-schema-validation.html#rfc.section.7.3.1) | Last watermark of the output data stream, if any. Initial blocks may not have watermarks, but once watermark is set - all subsequent blocks should either carry the same watermark or specify a new (greater) one. Thus, watermarks are monotonically non-decreasing. |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://github.com/open-data-fabric/open-data-fabric/tree/master/schemas/metadata-events/ExecuteTransform.json)
[![Flatbuffers Schema](https://img.shields.io/badge/schema-flatbuffers-blue)](https://github.com/open-data-fabric/open-data-fabric/tree/master/schemas-generated/flatbuffers/opendatafabric.fbs)

<a name="seed-schema"></a>
## `Seed`
Establishes the identity of the dataset. Always the first metadata event in the chain.

| Property | Type | Required | Format | Description |
| --- | --- | :---: | :---: | --- |
| `datasetId` | `string` | ✔️ | [`dataset-id`]({{<relref "spec#dataset-identity">}}) | Unique identity of the dataset. |
| `datasetKind` | [`DatasetKind`](#datasetkind-schema) | ✔️ |  | Type of the dataset. |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://github.com/open-data-fabric/open-data-fabric/tree/master/schemas/metadata-events/Seed.json)
[![Flatbuffers Schema](https://img.shields.io/badge/schema-flatbuffers-blue)](https://github.com/open-data-fabric/open-data-fabric/tree/master/schemas-generated/flatbuffers/opendatafabric.fbs)

<a name="setattachments-schema"></a>
## `SetAttachments`
Associates a set of files with this dataset.

| Property | Type | Required | Format | Description |
| --- | --- | :---: | :---: | --- |
| `attachments` | [`Attachments`](#attachments-schema) | ✔️ |  | One of the supported attachment sources. |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://github.com/open-data-fabric/open-data-fabric/tree/master/schemas/metadata-events/SetAttachments.json)
[![Flatbuffers Schema](https://img.shields.io/badge/schema-flatbuffers-blue)](https://github.com/open-data-fabric/open-data-fabric/tree/master/schemas-generated/flatbuffers/opendatafabric.fbs)

<a name="setdataschema-schema"></a>
## `SetDataSchema`
Specifies the complete schema of Data Slices added to the Dataset following this event.

| Property | Type | Required | Format | Description |
| --- | --- | :---: | :---: | --- |
| `schema` | `string` | ✔️ | [`flatbuffers`](https://flatbuffers.dev/) | Apache Arrow schema encoded in its native flatbuffers representation. |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://github.com/open-data-fabric/open-data-fabric/tree/master/schemas/metadata-events/SetDataSchema.json)
[![Flatbuffers Schema](https://img.shields.io/badge/schema-flatbuffers-blue)](https://github.com/open-data-fabric/open-data-fabric/tree/master/schemas-generated/flatbuffers/opendatafabric.fbs)

<a name="setinfo-schema"></a>
## `SetInfo`
Provides basic human-readable information about a dataset.

| Property | Type | Required | Format | Description |
| --- | --- | :---: | :---: | --- |
| `description` | `string` |  |  | Brief single-sentence summary of a dataset. |
| `keywords` | `array(string)` |  |  | Keywords, search terms, or tags used to describe the dataset. |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://github.com/open-data-fabric/open-data-fabric/tree/master/schemas/metadata-events/SetInfo.json)
[![Flatbuffers Schema](https://img.shields.io/badge/schema-flatbuffers-blue)](https://github.com/open-data-fabric/open-data-fabric/tree/master/schemas-generated/flatbuffers/opendatafabric.fbs)

<a name="setlicense-schema"></a>
## `SetLicense`
Defines a license that applies to this dataset.

| Property | Type | Required | Format | Description |
| --- | --- | :---: | :---: | --- |
| `shortName` | `string` | ✔️ |  | Abbreviated name of the license. |
| `name` | `string` | ✔️ |  | Full name of the license. |
| `spdxId` | `string` |  |  | License identifier from the SPDX License List. |
| `websiteUrl` | `string` | ✔️ | `url` |  |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://github.com/open-data-fabric/open-data-fabric/tree/master/schemas/metadata-events/SetLicense.json)
[![Flatbuffers Schema](https://img.shields.io/badge/schema-flatbuffers-blue)](https://github.com/open-data-fabric/open-data-fabric/tree/master/schemas-generated/flatbuffers/opendatafabric.fbs)

<a name="setpollingsource-schema"></a>
## `SetPollingSource`
Contains information on how externally-hosted data can be ingested into the root dataset.

| Property | Type | Required | Format | Description |
| --- | --- | :---: | :---: | --- |
| `fetch` | [`FetchStep`](#fetchstep-schema) | ✔️ |  | Determines where data is sourced from. |
| `prepare` | `array(`[`PrepStep`](#prepstep-schema)`)` |  |  | Defines how raw data is prepared before reading. |
| `read` | [`ReadStep`](#readstep-schema) | ✔️ |  | Defines how data is read into structured format. |
| `preprocess` | [`Transform`](#transform-schema) |  |  | Pre-processing query that shapes the data. |
| `merge` | [`MergeStrategy`](#mergestrategy-schema) | ✔️ |  | Determines how newly-ingested data should be merged with existing history. |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://github.com/open-data-fabric/open-data-fabric/tree/master/schemas/metadata-events/SetPollingSource.json)
[![Flatbuffers Schema](https://img.shields.io/badge/schema-flatbuffers-blue)](https://github.com/open-data-fabric/open-data-fabric/tree/master/schemas-generated/flatbuffers/opendatafabric.fbs)

<a name="settransform-schema"></a>
## `SetTransform`
Defines a transformation that produces data in a derivative dataset.

| Property | Type | Required | Format | Description |
| --- | --- | :---: | :---: | --- |
| `inputs` | `array(`[`TransformInput`](#transforminput-schema)`)` | ✔️ |  | Datasets that will be used as sources. |
| `transform` | [`Transform`](#transform-schema) | ✔️ |  | Transformation that will be applied to produce new data. |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://github.com/open-data-fabric/open-data-fabric/tree/master/schemas/metadata-events/SetTransform.json)
[![Flatbuffers Schema](https://img.shields.io/badge/schema-flatbuffers-blue)](https://github.com/open-data-fabric/open-data-fabric/tree/master/schemas-generated/flatbuffers/opendatafabric.fbs)

<a name="setvocab-schema"></a>
## `SetVocab`
Lets you manipulate names of the system columns to avoid conflicts.

| Property | Type | Required | Format | Description |
| --- | --- | :---: | :---: | --- |
| `offsetColumn` | `string` |  |  | Name of the offset column. |
| `operationTypeColumn` | `string` |  |  | Name of the operation type column. |
| `systemTimeColumn` | `string` |  |  | Name of the system time column. |
| `eventTimeColumn` | `string` |  |  | Name of the event time column. |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://github.com/open-data-fabric/open-data-fabric/tree/master/schemas/metadata-events/SetVocab.json)
[![Flatbuffers Schema](https://img.shields.io/badge/schema-flatbuffers-blue)](https://github.com/open-data-fabric/open-data-fabric/tree/master/schemas-generated/flatbuffers/opendatafabric.fbs)

<a name="reference-engine-protocol"></a>
# Engine Protocol
<a name="rawqueryrequest-schema"></a>
## `RawQueryRequest`
Sent by the coordinator to an engine to perform query on raw input data, usually as part of ingest preprocessing step

| Property | Type | Required | Format | Description |
| --- | --- | :---: | :---: | --- |
| `inputDataPaths` | `array(string)` | ✔️ |  | Paths to input data files to perform query over. Must all have identical schema. |
| `transform` | [`Transform`](#transform-schema) | ✔️ |  | Transformation that will be applied to produce new data. |
| `outputDataPath` | `string` | ✔️ | `path` | Path where query result will be written. |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://github.com/open-data-fabric/open-data-fabric/tree/master/schemas/engine-ops/RawQueryRequest.json)
[![Flatbuffers Schema](https://img.shields.io/badge/schema-flatbuffers-blue)](https://github.com/open-data-fabric/open-data-fabric/tree/master/schemas-generated/flatbuffers/opendatafabric.fbs)

<a name="rawqueryresponse-schema"></a>
## `RawQueryResponse`
Sent by an engine to coordinator when performing the raw query operation

| Union Type | Description |
| --- | --- |
| [`RawQueryResponse::Progress`](#rawqueryresponse-progress-schema) |  |
| [`RawQueryResponse::Success`](#rawqueryresponse-success-schema) |  |
| [`RawQueryResponse::InvalidQuery`](#rawqueryresponse-invalidquery-schema) |  |
| [`RawQueryResponse::InternalError`](#rawqueryresponse-internalerror-schema) |  |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://github.com/open-data-fabric/open-data-fabric/tree/master/schemas/engine-ops/RawQueryResponse.json)
[![Flatbuffers Schema](https://img.shields.io/badge/schema-flatbuffers-blue)](https://github.com/open-data-fabric/open-data-fabric/tree/master/schemas-generated/flatbuffers/opendatafabric.fbs)

<a name="rawqueryresponse-progress-schema"></a>
## `RawQueryResponse::Progress`


| Property | Type | Required | Format | Description |
| --- | --- | :---: | :---: | --- |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://github.com/open-data-fabric/open-data-fabric/tree/master/schemas/engine-ops/RawQueryResponse.json)
[![Flatbuffers Schema](https://img.shields.io/badge/schema-flatbuffers-blue)](https://github.com/open-data-fabric/open-data-fabric/tree/master/schemas-generated/flatbuffers/opendatafabric.fbs)

<a name="rawqueryresponse-success-schema"></a>
## `RawQueryResponse::Success`


| Property | Type | Required | Format | Description |
| --- | --- | :---: | :---: | --- |
| `numRecords` | `integer` | ✔️ | `uint64` | Number of records produced by the query |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://github.com/open-data-fabric/open-data-fabric/tree/master/schemas/engine-ops/RawQueryResponse.json)
[![Flatbuffers Schema](https://img.shields.io/badge/schema-flatbuffers-blue)](https://github.com/open-data-fabric/open-data-fabric/tree/master/schemas-generated/flatbuffers/opendatafabric.fbs)

<a name="rawqueryresponse-invalidquery-schema"></a>
## `RawQueryResponse::InvalidQuery`


| Property | Type | Required | Format | Description |
| --- | --- | :---: | :---: | --- |
| `message` | `string` | ✔️ |  | Explanation of an error |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://github.com/open-data-fabric/open-data-fabric/tree/master/schemas/engine-ops/RawQueryResponse.json)
[![Flatbuffers Schema](https://img.shields.io/badge/schema-flatbuffers-blue)](https://github.com/open-data-fabric/open-data-fabric/tree/master/schemas-generated/flatbuffers/opendatafabric.fbs)

<a name="rawqueryresponse-internalerror-schema"></a>
## `RawQueryResponse::InternalError`


| Property | Type | Required | Format | Description |
| --- | --- | :---: | :---: | --- |
| `message` | `string` | ✔️ |  | Brief description of an error |
| `backtrace` | `string` |  |  | Details of an error (e.g. a backtrace) |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://github.com/open-data-fabric/open-data-fabric/tree/master/schemas/engine-ops/RawQueryResponse.json)
[![Flatbuffers Schema](https://img.shields.io/badge/schema-flatbuffers-blue)](https://github.com/open-data-fabric/open-data-fabric/tree/master/schemas-generated/flatbuffers/opendatafabric.fbs)


<a name="transformrequest-schema"></a>
## `TransformRequest`
Sent by the coordinator to an engine to perform the next step of data transformation

| Property | Type | Required | Format | Description |
| --- | --- | :---: | :---: | --- |
| `datasetId` | `string` | ✔️ | [`dataset-id`]({{<relref "spec#dataset-identity">}}) | Unique identifier of the output dataset. |
| `datasetAlias` | `string` | ✔️ | [`dataset-alias`]({{<relref "spec#dataset-identity">}}) | Alias of the output dataset, for logging purposes only. |
| `systemTime` | `string` | ✔️ | [`date-time`](https://json-schema.org/draft/2019-09/json-schema-validation.html#rfc.section.7.3.1) | System time to use for new records. |
| `vocab` | [`DatasetVocabulary`](#datasetvocabulary-schema) | ✔️ |  |  |
| `transform` | [`Transform`](#transform-schema) | ✔️ |  | Transformation that will be applied to produce new data. |
| `queryInputs` | `array(`[`TransformRequestInput`](#transformrequestinput-schema)`)` | ✔️ |  | Defines inputs used in this transaction. Slices corresponding to every input dataset must be present. |
| `nextOffset` | `integer` | ✔️ | `uint64` | Starting offset to use for new data records. |
| `prevCheckpointPath` | `string` |  | `path` | TODO: This will be removed when coordinator will be speaking to engines purely through Arrow. |
| `newCheckpointPath` | `string` | ✔️ | `path` | TODO: This will be removed when coordinator will be speaking to engines purely through Arrow. |
| `newDataPath` | `string` | ✔️ | `path` | TODO: This will be removed when coordinator will be speaking to engines purely through Arrow. |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://github.com/open-data-fabric/open-data-fabric/tree/master/schemas/engine-ops/TransformRequest.json)
[![Flatbuffers Schema](https://img.shields.io/badge/schema-flatbuffers-blue)](https://github.com/open-data-fabric/open-data-fabric/tree/master/schemas-generated/flatbuffers/opendatafabric.fbs)

<a name="transformrequestinput-schema"></a>
## `TransformRequestInput`
Sent as part of the engine transform request operation to describe the input

| Property | Type | Required | Format | Description |
| --- | --- | :---: | :---: | --- |
| `datasetId` | `string` | ✔️ | [`dataset-id`]({{<relref "spec#dataset-identity">}}) | Unique identifier of the dataset. |
| `datasetAlias` | `string` | ✔️ | [`dataset-alias`]({{<relref "spec#dataset-identity">}}) | Alias of the output dataset, for logging purposes only. |
| `queryAlias` | `string` | ✔️ |  | An alias of this input to be used in queries. |
| `vocab` | [`DatasetVocabulary`](#datasetvocabulary-schema) | ✔️ |  |  |
| `offsetInterval` | [`OffsetInterval`](#offsetinterval-schema) |  |  | Subset of data that goes into this transaction. |
| `dataPaths` | `array(string)` | ✔️ |  | TODO: This will be removed when coordinator will be slicing data for the engine. |
| `schemaFile` | `string` | ✔️ | `path` | TODO: replace with actual DDL or Parquet schema. |
| `explicitWatermarks` | `array(`[`Watermark`](#watermark-schema)`)` | ✔️ |  |  |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://github.com/open-data-fabric/open-data-fabric/tree/master/schemas/engine-ops/TransformRequestInput.json)
[![Flatbuffers Schema](https://img.shields.io/badge/schema-flatbuffers-blue)](https://github.com/open-data-fabric/open-data-fabric/tree/master/schemas-generated/flatbuffers/opendatafabric.fbs)

<a name="transformresponse-schema"></a>
## `TransformResponse`
Sent by an engine to coordinator when performing the data transformation

| Union Type | Description |
| --- | --- |
| [`TransformResponse::Progress`](#transformresponse-progress-schema) |  |
| [`TransformResponse::Success`](#transformresponse-success-schema) |  |
| [`TransformResponse::InvalidQuery`](#transformresponse-invalidquery-schema) |  |
| [`TransformResponse::InternalError`](#transformresponse-internalerror-schema) |  |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://github.com/open-data-fabric/open-data-fabric/tree/master/schemas/engine-ops/TransformResponse.json)
[![Flatbuffers Schema](https://img.shields.io/badge/schema-flatbuffers-blue)](https://github.com/open-data-fabric/open-data-fabric/tree/master/schemas-generated/flatbuffers/opendatafabric.fbs)

<a name="transformresponse-progress-schema"></a>
## `TransformResponse::Progress`


| Property | Type | Required | Format | Description |
| --- | --- | :---: | :---: | --- |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://github.com/open-data-fabric/open-data-fabric/tree/master/schemas/engine-ops/TransformResponse.json)
[![Flatbuffers Schema](https://img.shields.io/badge/schema-flatbuffers-blue)](https://github.com/open-data-fabric/open-data-fabric/tree/master/schemas-generated/flatbuffers/opendatafabric.fbs)

<a name="transformresponse-success-schema"></a>
## `TransformResponse::Success`


| Property | Type | Required | Format | Description |
| --- | --- | :---: | :---: | --- |
| `newOffsetInterval` | [`OffsetInterval`](#offsetinterval-schema) |  |  | Data slice produced by the transaction, if any. |
| `newWatermark` | `string` |  | [`date-time`](https://json-schema.org/draft/2019-09/json-schema-validation.html#rfc.section.7.3.1) | Watermark advanced by the transaction, if any. |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://github.com/open-data-fabric/open-data-fabric/tree/master/schemas/engine-ops/TransformResponse.json)
[![Flatbuffers Schema](https://img.shields.io/badge/schema-flatbuffers-blue)](https://github.com/open-data-fabric/open-data-fabric/tree/master/schemas-generated/flatbuffers/opendatafabric.fbs)

<a name="transformresponse-invalidquery-schema"></a>
## `TransformResponse::InvalidQuery`


| Property | Type | Required | Format | Description |
| --- | --- | :---: | :---: | --- |
| `message` | `string` | ✔️ |  | Explanation of an error |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://github.com/open-data-fabric/open-data-fabric/tree/master/schemas/engine-ops/TransformResponse.json)
[![Flatbuffers Schema](https://img.shields.io/badge/schema-flatbuffers-blue)](https://github.com/open-data-fabric/open-data-fabric/tree/master/schemas-generated/flatbuffers/opendatafabric.fbs)

<a name="transformresponse-internalerror-schema"></a>
## `TransformResponse::InternalError`


| Property | Type | Required | Format | Description |
| --- | --- | :---: | :---: | --- |
| `message` | `string` | ✔️ |  | Brief description of an error |
| `backtrace` | `string` |  |  | Details of an error (e.g. a backtrace) |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://github.com/open-data-fabric/open-data-fabric/tree/master/schemas/engine-ops/TransformResponse.json)
[![Flatbuffers Schema](https://img.shields.io/badge/schema-flatbuffers-blue)](https://github.com/open-data-fabric/open-data-fabric/tree/master/schemas-generated/flatbuffers/opendatafabric.fbs)


<a name="reference-fragments"></a>
# Fragments
<a name="attachmentembedded-schema"></a>
## `AttachmentEmbedded`
Embedded attachment item.

| Property | Type | Required | Format | Description |
| --- | --- | :---: | :---: | --- |
| `path` | `string` | ✔️ |  | Path to an attachment if it was materialized into a file. |
| `content` | `string` | ✔️ |  | Content of the attachment. |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://github.com/open-data-fabric/open-data-fabric/tree/master/schemas/fragments/AttachmentEmbedded.json)
[![Flatbuffers Schema](https://img.shields.io/badge/schema-flatbuffers-blue)](https://github.com/open-data-fabric/open-data-fabric/tree/master/schemas-generated/flatbuffers/opendatafabric.fbs)

<a name="attachments-schema"></a>
## `Attachments`
Defines the source of attachment files.

| Union Type | Description |
| --- | --- |
| [`Attachments::Embedded`](#attachments-embedded-schema) | For attachments that are specified inline and are embedded in the metadata. |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://github.com/open-data-fabric/open-data-fabric/tree/master/schemas/fragments/Attachments.json)
[![Flatbuffers Schema](https://img.shields.io/badge/schema-flatbuffers-blue)](https://github.com/open-data-fabric/open-data-fabric/tree/master/schemas-generated/flatbuffers/opendatafabric.fbs)

<a name="attachments-embedded-schema"></a>
## `Attachments::Embedded`
For attachments that are specified inline and are embedded in the metadata.

| Property | Type | Required | Format | Description |
| --- | --- | :---: | :---: | --- |
| `items` | `array(`[`AttachmentEmbedded`](#attachmentembedded-schema)`)` | ✔️ |  |  |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://github.com/open-data-fabric/open-data-fabric/tree/master/schemas/fragments/Attachments.json)
[![Flatbuffers Schema](https://img.shields.io/badge/schema-flatbuffers-blue)](https://github.com/open-data-fabric/open-data-fabric/tree/master/schemas-generated/flatbuffers/opendatafabric.fbs)


<a name="checkpoint-schema"></a>
## `Checkpoint`
Describes a checkpoint produced by an engine

| Property | Type | Required | Format | Description |
| --- | --- | :---: | :---: | --- |
| `physicalHash` | `string` | ✔️ | [`multihash`](https://github.com/multiformats/multihash) | Hash sum of the checkpoint file. |
| `size` | `integer` | ✔️ | `uint64` | Size of checkpoint file in bytes. |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://github.com/open-data-fabric/open-data-fabric/tree/master/schemas/fragments/Checkpoint.json)
[![Flatbuffers Schema](https://img.shields.io/badge/schema-flatbuffers-blue)](https://github.com/open-data-fabric/open-data-fabric/tree/master/schemas-generated/flatbuffers/opendatafabric.fbs)

<a name="dataslice-schema"></a>
## `DataSlice`
Describes a slice of data added to a dataset or produced via transformation

| Property | Type | Required | Format | Description |
| --- | --- | :---: | :---: | --- |
| `logicalHash` | `string` | ✔️ | [`multihash`](https://github.com/multiformats/multihash) | Logical hash sum of the data in this slice. |
| `physicalHash` | `string` | ✔️ | [`multihash`](https://github.com/multiformats/multihash) | Hash sum of the data part file. |
| `offsetInterval` | [`OffsetInterval`](#offsetinterval-schema) | ✔️ |  | Data slice produced by the transaction. |
| `size` | `integer` | ✔️ | `uint64` | Size of data file in bytes. |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://github.com/open-data-fabric/open-data-fabric/tree/master/schemas/fragments/DataSlice.json)
[![Flatbuffers Schema](https://img.shields.io/badge/schema-flatbuffers-blue)](https://github.com/open-data-fabric/open-data-fabric/tree/master/schemas-generated/flatbuffers/opendatafabric.fbs)

<a name="datasetkind-schema"></a>
## `DatasetKind`
Represents type of the dataset.

| Enum Value |
| :---: |
| `Root` |
| `Derivative` |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://github.com/open-data-fabric/open-data-fabric/tree/master/schemas/fragments/DatasetKind.json)
[![Flatbuffers Schema](https://img.shields.io/badge/schema-flatbuffers-blue)](https://github.com/open-data-fabric/open-data-fabric/tree/master/schemas-generated/flatbuffers/opendatafabric.fbs)

<a name="datasetvocabulary-schema"></a>
## `DatasetVocabulary`
Specifies the mapping of system columns onto dataset schema.

| Property | Type | Required | Format | Description |
| --- | --- | :---: | :---: | --- |
| `offsetColumn` | `string` | ✔️ |  | Name of the offset column. |
| `operationTypeColumn` | `string` | ✔️ |  | Name of the operation type column. |
| `systemTimeColumn` | `string` | ✔️ |  | Name of the system time column. |
| `eventTimeColumn` | `string` | ✔️ |  | Name of the event time column. |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://github.com/open-data-fabric/open-data-fabric/tree/master/schemas/fragments/DatasetVocabulary.json)
[![Flatbuffers Schema](https://img.shields.io/badge/schema-flatbuffers-blue)](https://github.com/open-data-fabric/open-data-fabric/tree/master/schemas-generated/flatbuffers/opendatafabric.fbs)

<a name="envvar-schema"></a>
## `EnvVar`
Defines an environment variable passed into some job.

| Property | Type | Required | Format | Description |
| --- | --- | :---: | :---: | --- |
| `name` | `string` | ✔️ |  | Name of the variable. |
| `value` | `string` |  |  | Value of the variable. |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://github.com/open-data-fabric/open-data-fabric/tree/master/schemas/fragments/EnvVar.json)
[![Flatbuffers Schema](https://img.shields.io/badge/schema-flatbuffers-blue)](https://github.com/open-data-fabric/open-data-fabric/tree/master/schemas-generated/flatbuffers/opendatafabric.fbs)

<a name="eventtimesource-schema"></a>
## `EventTimeSource`
Defines the external source of data.

| Union Type | Description |
| --- | --- |
| [`EventTimeSource::FromMetadata`](#eventtimesource-frommetadata-schema) | Extracts event time from the source's metadata. |
| [`EventTimeSource::FromPath`](#eventtimesource-frompath-schema) | Extracts event time from the path component of the source. |
| [`EventTimeSource::FromSystemTime`](#eventtimesource-fromsystemtime-schema) | Assigns event time from the system time source. |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://github.com/open-data-fabric/open-data-fabric/tree/master/schemas/fragments/EventTimeSource.json)
[![Flatbuffers Schema](https://img.shields.io/badge/schema-flatbuffers-blue)](https://github.com/open-data-fabric/open-data-fabric/tree/master/schemas-generated/flatbuffers/opendatafabric.fbs)

<a name="eventtimesource-frommetadata-schema"></a>
## `EventTimeSource::FromMetadata`
Extracts event time from the source's metadata.

| Property | Type | Required | Format | Description |
| --- | --- | :---: | :---: | --- |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://github.com/open-data-fabric/open-data-fabric/tree/master/schemas/fragments/EventTimeSource.json)
[![Flatbuffers Schema](https://img.shields.io/badge/schema-flatbuffers-blue)](https://github.com/open-data-fabric/open-data-fabric/tree/master/schemas-generated/flatbuffers/opendatafabric.fbs)

<a name="eventtimesource-fromsystemtime-schema"></a>
## `EventTimeSource::FromSystemTime`
Assigns event time from the system time source.

| Property | Type | Required | Format | Description |
| --- | --- | :---: | :---: | --- |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://github.com/open-data-fabric/open-data-fabric/tree/master/schemas/fragments/EventTimeSource.json)
[![Flatbuffers Schema](https://img.shields.io/badge/schema-flatbuffers-blue)](https://github.com/open-data-fabric/open-data-fabric/tree/master/schemas-generated/flatbuffers/opendatafabric.fbs)

<a name="eventtimesource-frompath-schema"></a>
## `EventTimeSource::FromPath`
Extracts event time from the path component of the source.

| Property | Type | Required | Format | Description |
| --- | --- | :---: | :---: | --- |
| `pattern` | `string` | ✔️ | `regex` | Regular expression where first group contains the timestamp string. |
| `timestampFormat` | `string` |  |  | Format of the expected timestamp in java.text.SimpleDateFormat form. |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://github.com/open-data-fabric/open-data-fabric/tree/master/schemas/fragments/EventTimeSource.json)
[![Flatbuffers Schema](https://img.shields.io/badge/schema-flatbuffers-blue)](https://github.com/open-data-fabric/open-data-fabric/tree/master/schemas-generated/flatbuffers/opendatafabric.fbs)


<a name="executetransforminput-schema"></a>
## `ExecuteTransformInput`
Describes a slice of the input dataset used during a transformation

| Property | Type | Required | Format | Description |
| --- | --- | :---: | :---: | --- |
| `datasetId` | `string` | ✔️ | [`dataset-id`]({{<relref "spec#dataset-identity">}}) | Input dataset identifier. |
| `prevBlockHash` | `string` |  | [`multihash`](https://github.com/multiformats/multihash) | Last block of the input dataset that was previously incorporated into the derivative transformation, if any. Must be equal to the last non-empty `newBlockHash`. Together with `newBlockHash` defines a half-open `(prevBlockHash, newBlockHash]` interval of blocks that will be considered in this transaction. |
| `newBlockHash` | `string` |  | [`multihash`](https://github.com/multiformats/multihash) | Hash of the last block that will be incorporated into the derivative transformation. When present, defines a half-open `(prevBlockHash, newBlockHash]` interval of blocks that will be considered in this transaction. |
| `prevOffset` | `integer` |  | `uint64` | Last data record offset in the input dataset that was previously incorporated into the derivative transformation, if any. Must be equal to the last non-empty `newOffset`. Together with `newOffset` defines a half-open `(prevOffset, newOffset]` interval of data records that will be considered in this transaction. |
| `newOffset` | `integer` |  | `uint64` | Offset of the last data record that will be incorporated into the derivative transformation, if any. When present, defines a half-open `(prevOffset, newOffset]` interval of data records that will be considered in this transaction. |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://github.com/open-data-fabric/open-data-fabric/tree/master/schemas/fragments/ExecuteTransformInput.json)
[![Flatbuffers Schema](https://img.shields.io/badge/schema-flatbuffers-blue)](https://github.com/open-data-fabric/open-data-fabric/tree/master/schemas-generated/flatbuffers/opendatafabric.fbs)

<a name="fetchstep-schema"></a>
## `FetchStep`
Defines the external source of data.

| Union Type | Description |
| --- | --- |
| [`FetchStep::Url`](#fetchstep-url-schema) | Pulls data from one of the supported sources by its URL. |
| [`FetchStep::FilesGlob`](#fetchstep-filesglob-schema) | Uses glob operator to match files on the local file system. |
| [`FetchStep::Container`](#fetchstep-container-schema) | Runs the specified OCI container to fetch data from an arbitrary source. |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://github.com/open-data-fabric/open-data-fabric/tree/master/schemas/fragments/FetchStep.json)
[![Flatbuffers Schema](https://img.shields.io/badge/schema-flatbuffers-blue)](https://github.com/open-data-fabric/open-data-fabric/tree/master/schemas-generated/flatbuffers/opendatafabric.fbs)

<a name="fetchstep-url-schema"></a>
## `FetchStep::Url`
Pulls data from one of the supported sources by its URL.

| Property | Type | Required | Format | Description |
| --- | --- | :---: | :---: | --- |
| `url` | `string` | ✔️ | `url` | URL of the data source |
| `eventTime` | [`EventTimeSource`](#eventtimesource-schema) |  |  | Describes how event time is extracted from the source metadata. |
| `cache` | [`SourceCaching`](#sourcecaching-schema) |  |  | Describes the caching settings used for this source. |
| `headers` | `array(`[`RequestHeader`](#requestheader-schema)`)` |  |  | Headers to pass during the request (e.g. HTTP Authorization) |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://github.com/open-data-fabric/open-data-fabric/tree/master/schemas/fragments/FetchStep.json)
[![Flatbuffers Schema](https://img.shields.io/badge/schema-flatbuffers-blue)](https://github.com/open-data-fabric/open-data-fabric/tree/master/schemas-generated/flatbuffers/opendatafabric.fbs)

<a name="fetchstep-filesglob-schema"></a>
## `FetchStep::FilesGlob`
Uses glob operator to match files on the local file system.

| Property | Type | Required | Format | Description |
| --- | --- | :---: | :---: | --- |
| `path` | `string` | ✔️ |  | Path with a glob pattern. |
| `eventTime` | [`EventTimeSource`](#eventtimesource-schema) |  |  | Describes how event time is extracted from the source metadata. |
| `cache` | [`SourceCaching`](#sourcecaching-schema) |  |  | Describes the caching settings used for this source. |
| `order` | `string` |  |  | Specifies how input files should be ordered before ingestion.<br/>Order is important as every file will be processed individually<br/>and will advance the dataset's watermark. |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://github.com/open-data-fabric/open-data-fabric/tree/master/schemas/fragments/FetchStep.json)
[![Flatbuffers Schema](https://img.shields.io/badge/schema-flatbuffers-blue)](https://github.com/open-data-fabric/open-data-fabric/tree/master/schemas-generated/flatbuffers/opendatafabric.fbs)

<a name="fetchstep-container-schema"></a>
## `FetchStep::Container`
Runs the specified OCI container to fetch data from an arbitrary source.

| Property | Type | Required | Format | Description |
| --- | --- | :---: | :---: | --- |
| `image` | `string` | ✔️ |  | Image name and and an optional tag. |
| `command` | `array(string)` |  |  | Specifies the entrypoint. Not executed within a shell. The default OCI image's ENTRYPOINT is used if this is not provided. |
| `args` | `array(string)` |  |  | Arguments to the entrypoint. The OCI image's CMD is used if this is not provided. |
| `env` | `array(`[`EnvVar`](#envvar-schema)`)` |  |  | Environment variables to propagate into or set in the container. |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://github.com/open-data-fabric/open-data-fabric/tree/master/schemas/fragments/FetchStep.json)
[![Flatbuffers Schema](https://img.shields.io/badge/schema-flatbuffers-blue)](https://github.com/open-data-fabric/open-data-fabric/tree/master/schemas-generated/flatbuffers/opendatafabric.fbs)


<a name="mergestrategy-schema"></a>
## `MergeStrategy`
Merge strategy determines how newly ingested data should be combined with the data that already exists in the dataset.

| Union Type | Description |
| --- | --- |
| [`MergeStrategy::Append`](#mergestrategy-append-schema) | Append merge strategy. |
| [`MergeStrategy::Ledger`](#mergestrategy-ledger-schema) | Ledger merge strategy. |
| [`MergeStrategy::Snapshot`](#mergestrategy-snapshot-schema) | Snapshot merge strategy. |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://github.com/open-data-fabric/open-data-fabric/tree/master/schemas/fragments/MergeStrategy.json)
[![Flatbuffers Schema](https://img.shields.io/badge/schema-flatbuffers-blue)](https://github.com/open-data-fabric/open-data-fabric/tree/master/schemas-generated/flatbuffers/opendatafabric.fbs)

<a name="mergestrategy-append-schema"></a>
## `MergeStrategy::Append`
Append merge strategy.

Under this strategy new data will be appended to the dataset in its entirety, without any deduplication.

| Property | Type | Required | Format | Description |
| --- | --- | :---: | :---: | --- |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://github.com/open-data-fabric/open-data-fabric/tree/master/schemas/fragments/MergeStrategy.json)
[![Flatbuffers Schema](https://img.shields.io/badge/schema-flatbuffers-blue)](https://github.com/open-data-fabric/open-data-fabric/tree/master/schemas-generated/flatbuffers/opendatafabric.fbs)

<a name="mergestrategy-ledger-schema"></a>
## `MergeStrategy::Ledger`
Ledger merge strategy.

This strategy should be used for data sources containing ledgers of events. Currently this strategy will only perform deduplication of events using user-specified primary key columns. This means that the source data can contain partially overlapping set of records and only those records that were not previously seen will be appended.

| Property | Type | Required | Format | Description |
| --- | --- | :---: | :---: | --- |
| `primaryKey` | `array(string)` | ✔️ |  | Names of the columns that uniquely identify the record throughout its lifetime |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://github.com/open-data-fabric/open-data-fabric/tree/master/schemas/fragments/MergeStrategy.json)
[![Flatbuffers Schema](https://img.shields.io/badge/schema-flatbuffers-blue)](https://github.com/open-data-fabric/open-data-fabric/tree/master/schemas-generated/flatbuffers/opendatafabric.fbs)

<a name="mergestrategy-snapshot-schema"></a>
## `MergeStrategy::Snapshot`
Snapshot merge strategy.

This strategy can be used for data state snapshots that are taken periodically and contain only the latest state of the observed entity or system. Over time such snapshots can have new rows added, and old rows either removed or modified.

This strategy transforms snapshot data into an append-only event stream where data already added is immutable. It does so by performing Change Data Capture - essentially diffing the current state of data against the reconstructed previous state and recording differences as retractions or corrections. The Operation Type "op" column will contain:
  - append (`+A`) when a row appears for the first time
  - retraction (`-D`) when row disappears
  - correction (`-C`, `+C`) when row data has changed, with `-C` event carrying the old value of the row and `+C` carrying the new value.

To correctly associate rows between old and new snapshots this strategy relies on user-specified primary key columns.

To identify whether a row has changed this strategy will compare all other columns one by one. If the data contains a column that is guaranteed to change whenever any of the data columns changes (for example a last modification timestamp, an incremental version, or a data hash), then it can be specified in `compareColumns` property to speed up the detection of modified rows.

| Property | Type | Required | Format | Description |
| --- | --- | :---: | :---: | --- |
| `primaryKey` | `array(string)` | ✔️ |  | Names of the columns that uniquely identify the record throughout its lifetime. |
| `compareColumns` | `array(string)` |  |  | Names of the columns to compared to determine if a row has changed between two snapshots. |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://github.com/open-data-fabric/open-data-fabric/tree/master/schemas/fragments/MergeStrategy.json)
[![Flatbuffers Schema](https://img.shields.io/badge/schema-flatbuffers-blue)](https://github.com/open-data-fabric/open-data-fabric/tree/master/schemas-generated/flatbuffers/opendatafabric.fbs)


<a name="offsetinterval-schema"></a>
## `OffsetInterval`
Describes a range of data as a closed arithmetic interval of offsets

| Property | Type | Required | Format | Description |
| --- | --- | :---: | :---: | --- |
| `start` | `integer` | ✔️ | `uint64` | Start of the closed interval [start; end]. |
| `end` | `integer` | ✔️ | `uint64` | End of the closed interval [start; end]. |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://github.com/open-data-fabric/open-data-fabric/tree/master/schemas/fragments/OffsetInterval.json)
[![Flatbuffers Schema](https://img.shields.io/badge/schema-flatbuffers-blue)](https://github.com/open-data-fabric/open-data-fabric/tree/master/schemas-generated/flatbuffers/opendatafabric.fbs)

<a name="prepstep-schema"></a>
## `PrepStep`
Defines the steps to prepare raw data for ingestion.

| Union Type | Description |
| --- | --- |
| [`PrepStep::Decompress`](#prepstep-decompress-schema) | Pulls data from one of the supported sources by its URL. |
| [`PrepStep::Pipe`](#prepstep-pipe-schema) | Executes external command to process the data using piped input/output. |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://github.com/open-data-fabric/open-data-fabric/tree/master/schemas/fragments/PrepStep.json)
[![Flatbuffers Schema](https://img.shields.io/badge/schema-flatbuffers-blue)](https://github.com/open-data-fabric/open-data-fabric/tree/master/schemas-generated/flatbuffers/opendatafabric.fbs)

<a name="prepstep-decompress-schema"></a>
## `PrepStep::Decompress`
Pulls data from one of the supported sources by its URL.

| Property | Type | Required | Format | Description |
| --- | --- | :---: | :---: | --- |
| `format` | `string` | ✔️ |  | Name of a compression algorithm used on data. |
| `subPath` | `string` |  |  | Path to a data file within a multi-file archive. Can contain glob patterns. |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://github.com/open-data-fabric/open-data-fabric/tree/master/schemas/fragments/PrepStep.json)
[![Flatbuffers Schema](https://img.shields.io/badge/schema-flatbuffers-blue)](https://github.com/open-data-fabric/open-data-fabric/tree/master/schemas-generated/flatbuffers/opendatafabric.fbs)

<a name="prepstep-pipe-schema"></a>
## `PrepStep::Pipe`
Executes external command to process the data using piped input/output.

| Property | Type | Required | Format | Description |
| --- | --- | :---: | :---: | --- |
| `command` | `array(string)` | ✔️ |  | Command to execute and its arguments. |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://github.com/open-data-fabric/open-data-fabric/tree/master/schemas/fragments/PrepStep.json)
[![Flatbuffers Schema](https://img.shields.io/badge/schema-flatbuffers-blue)](https://github.com/open-data-fabric/open-data-fabric/tree/master/schemas-generated/flatbuffers/opendatafabric.fbs)


<a name="readstep-schema"></a>
## `ReadStep`
Defines how raw data should be read into the structured form.

| Union Type | Description |
| --- | --- |
| [`ReadStep::Csv`](#readstep-csv-schema) | Reader for comma-separated files. |
| [`ReadStep::GeoJson`](#readstep-geojson-schema) | Reader for GeoJSON files. It expects one `FeatureCollection` object in the root and will create a record per each `Feature` inside it extracting the properties into individual columns and leaving the feature geometry in its own column. |
| [`ReadStep::EsriShapefile`](#readstep-esrishapefile-schema) | Reader for ESRI Shapefile format. |
| [`ReadStep::Parquet`](#readstep-parquet-schema) | Reader for Apache Parquet format. |
| [`ReadStep::Json`](#readstep-json-schema) | Reader for JSON files that contain an array of objects within them. |
| [`ReadStep::NdJson`](#readstep-ndjson-schema) | Reader for files containing multiple newline-delimited JSON objects with the same schema. |
| [`ReadStep::NdGeoJson`](#readstep-ndgeojson-schema) | Reader for Newline-delimited GeoJSON files. It is similar to `GeoJson` format but instead of `FeatureCollection` object in the root it expects every individual feature object to appear on its own line. |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://github.com/open-data-fabric/open-data-fabric/tree/master/schemas/fragments/ReadStep.json)
[![Flatbuffers Schema](https://img.shields.io/badge/schema-flatbuffers-blue)](https://github.com/open-data-fabric/open-data-fabric/tree/master/schemas-generated/flatbuffers/opendatafabric.fbs)

<a name="readstep-csv-schema"></a>
## `ReadStep::Csv`
Reader for comma-separated files.

| Property | Type | Required | Format | Description |
| --- | --- | :---: | :---: | --- |
| `schema` | `array(string)` |  |  | A DDL-formatted schema. Schema can be used to coerce values into more appropriate data types. |
| `separator` | `string` |  |  | Sets a single character as a separator for each field and value. |
| `encoding` | `string` |  |  | Decodes the CSV files by the given encoding type. |
| `quote` | `string` |  |  | Sets a single character used for escaping quoted values where the separator can be part of the value. Set an empty string to turn off quotations. |
| `escape` | `string` |  |  | Sets a single character used for escaping quotes inside an already quoted value. |
| `header` | `boolean` |  |  | Use the first line as names of columns. |
| `inferSchema` | `boolean` |  |  | Infers the input schema automatically from data. It requires one extra pass over the data. |
| `nullValue` | `string` |  |  | Sets the string representation of a null value. |
| `dateFormat` | `string` |  |  | Sets the string that indicates a date format. The `rfc3339` is the only required format, the other format strings are implementation-specific. |
| `timestampFormat` | `string` |  |  | Sets the string that indicates a timestamp format. The `rfc3339` is the only required format, the other format strings are implementation-specific. |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://github.com/open-data-fabric/open-data-fabric/tree/master/schemas/fragments/ReadStep.json)
[![Flatbuffers Schema](https://img.shields.io/badge/schema-flatbuffers-blue)](https://github.com/open-data-fabric/open-data-fabric/tree/master/schemas-generated/flatbuffers/opendatafabric.fbs)

<a name="readstep-json-schema"></a>
## `ReadStep::Json`
Reader for JSON files that contain an array of objects within them.

| Property | Type | Required | Format | Description |
| --- | --- | :---: | :---: | --- |
| `subPath` | `string` |  |  | Path in the form of `a.b.c` to a sub-element of the root JSON object that is an array or objects. If not specified it is assumed that the root element is an array. |
| `schema` | `array(string)` |  |  | A DDL-formatted schema. Schema can be used to coerce values into more appropriate data types. |
| `dateFormat` | `string` |  |  | Sets the string that indicates a date format. The `rfc3339` is the only required format, the other format strings are implementation-specific. |
| `encoding` | `string` |  |  | Allows to forcibly set one of standard basic or extended encodings. |
| `timestampFormat` | `string` |  |  | Sets the string that indicates a timestamp format. The `rfc3339` is the only required format, the other format strings are implementation-specific. |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://github.com/open-data-fabric/open-data-fabric/tree/master/schemas/fragments/ReadStep.json)
[![Flatbuffers Schema](https://img.shields.io/badge/schema-flatbuffers-blue)](https://github.com/open-data-fabric/open-data-fabric/tree/master/schemas-generated/flatbuffers/opendatafabric.fbs)

<a name="readstep-ndjson-schema"></a>
## `ReadStep::NdJson`
Reader for files containing multiple newline-delimited JSON objects with the same schema.

| Property | Type | Required | Format | Description |
| --- | --- | :---: | :---: | --- |
| `schema` | `array(string)` |  |  | A DDL-formatted schema. Schema can be used to coerce values into more appropriate data types. |
| `dateFormat` | `string` |  |  | Sets the string that indicates a date format. The `rfc3339` is the only required format, the other format strings are implementation-specific. |
| `encoding` | `string` |  |  | Allows to forcibly set one of standard basic or extended encodings. |
| `timestampFormat` | `string` |  |  | Sets the string that indicates a timestamp format. The `rfc3339` is the only required format, the other format strings are implementation-specific. |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://github.com/open-data-fabric/open-data-fabric/tree/master/schemas/fragments/ReadStep.json)
[![Flatbuffers Schema](https://img.shields.io/badge/schema-flatbuffers-blue)](https://github.com/open-data-fabric/open-data-fabric/tree/master/schemas-generated/flatbuffers/opendatafabric.fbs)

<a name="readstep-geojson-schema"></a>
## `ReadStep::GeoJson`
Reader for GeoJSON files. It expects one `FeatureCollection` object in the root and will create a record per each `Feature` inside it extracting the properties into individual columns and leaving the feature geometry in its own column.

| Property | Type | Required | Format | Description |
| --- | --- | :---: | :---: | --- |
| `schema` | `array(string)` |  |  | A DDL-formatted schema. Schema can be used to coerce values into more appropriate data types. |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://github.com/open-data-fabric/open-data-fabric/tree/master/schemas/fragments/ReadStep.json)
[![Flatbuffers Schema](https://img.shields.io/badge/schema-flatbuffers-blue)](https://github.com/open-data-fabric/open-data-fabric/tree/master/schemas-generated/flatbuffers/opendatafabric.fbs)

<a name="readstep-ndgeojson-schema"></a>
## `ReadStep::NdGeoJson`
Reader for Newline-delimited GeoJSON files. It is similar to `GeoJson` format but instead of `FeatureCollection` object in the root it expects every individual feature object to appear on its own line.

| Property | Type | Required | Format | Description |
| --- | --- | :---: | :---: | --- |
| `schema` | `array(string)` |  |  | A DDL-formatted schema. Schema can be used to coerce values into more appropriate data types. |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://github.com/open-data-fabric/open-data-fabric/tree/master/schemas/fragments/ReadStep.json)
[![Flatbuffers Schema](https://img.shields.io/badge/schema-flatbuffers-blue)](https://github.com/open-data-fabric/open-data-fabric/tree/master/schemas-generated/flatbuffers/opendatafabric.fbs)

<a name="readstep-esrishapefile-schema"></a>
## `ReadStep::EsriShapefile`
Reader for ESRI Shapefile format.

| Property | Type | Required | Format | Description |
| --- | --- | :---: | :---: | --- |
| `schema` | `array(string)` |  |  | A DDL-formatted schema. Schema can be used to coerce values into more appropriate data types. |
| `subPath` | `string` |  |  | If the ZIP archive contains multiple shapefiles use this field to specify a sub-path to the desired `.shp` file. Can contain glob patterns to act as a filter. |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://github.com/open-data-fabric/open-data-fabric/tree/master/schemas/fragments/ReadStep.json)
[![Flatbuffers Schema](https://img.shields.io/badge/schema-flatbuffers-blue)](https://github.com/open-data-fabric/open-data-fabric/tree/master/schemas-generated/flatbuffers/opendatafabric.fbs)

<a name="readstep-parquet-schema"></a>
## `ReadStep::Parquet`
Reader for Apache Parquet format.

| Property | Type | Required | Format | Description |
| --- | --- | :---: | :---: | --- |
| `schema` | `array(string)` |  |  | A DDL-formatted schema. Schema can be used to coerce values into more appropriate data types. |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://github.com/open-data-fabric/open-data-fabric/tree/master/schemas/fragments/ReadStep.json)
[![Flatbuffers Schema](https://img.shields.io/badge/schema-flatbuffers-blue)](https://github.com/open-data-fabric/open-data-fabric/tree/master/schemas-generated/flatbuffers/opendatafabric.fbs)


<a name="requestheader-schema"></a>
## `RequestHeader`
Defines a header (e.g. HTTP) to be passed into some request.

| Property | Type | Required | Format | Description |
| --- | --- | :---: | :---: | --- |
| `name` | `string` | ✔️ |  | Name of the header. |
| `value` | `string` | ✔️ |  | Value of the header. |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://github.com/open-data-fabric/open-data-fabric/tree/master/schemas/fragments/RequestHeader.json)
[![Flatbuffers Schema](https://img.shields.io/badge/schema-flatbuffers-blue)](https://github.com/open-data-fabric/open-data-fabric/tree/master/schemas-generated/flatbuffers/opendatafabric.fbs)

<a name="sourcecaching-schema"></a>
## `SourceCaching`
Defines how external data should be cached.

| Union Type | Description |
| --- | --- |
| [`SourceCaching::Forever`](#sourcecaching-forever-schema) | After source was processed once it will never be ingested again. |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://github.com/open-data-fabric/open-data-fabric/tree/master/schemas/fragments/SourceCaching.json)
[![Flatbuffers Schema](https://img.shields.io/badge/schema-flatbuffers-blue)](https://github.com/open-data-fabric/open-data-fabric/tree/master/schemas-generated/flatbuffers/opendatafabric.fbs)

<a name="sourcecaching-forever-schema"></a>
## `SourceCaching::Forever`
After source was processed once it will never be ingested again.

| Property | Type | Required | Format | Description |
| --- | --- | :---: | :---: | --- |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://github.com/open-data-fabric/open-data-fabric/tree/master/schemas/fragments/SourceCaching.json)
[![Flatbuffers Schema](https://img.shields.io/badge/schema-flatbuffers-blue)](https://github.com/open-data-fabric/open-data-fabric/tree/master/schemas-generated/flatbuffers/opendatafabric.fbs)


<a name="sourcestate-schema"></a>
## `SourceState`
The state of the source the data was added from to allow fast resuming.

| Property | Type | Required | Format | Description |
| --- | --- | :---: | :---: | --- |
| `sourceName` | `string` | ✔️ |  | Identifies the source that the state corresponds to. |
| `kind` | `string` | ✔️ |  | Identifies the type of the state. Standard types include: `odf/etag`, `odf/last-modified`. |
| `value` | `string` | ✔️ |  | Opaque value representing the state. |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://github.com/open-data-fabric/open-data-fabric/tree/master/schemas/fragments/SourceState.json)
[![Flatbuffers Schema](https://img.shields.io/badge/schema-flatbuffers-blue)](https://github.com/open-data-fabric/open-data-fabric/tree/master/schemas-generated/flatbuffers/opendatafabric.fbs)

<a name="sqlquerystep-schema"></a>
## `SqlQueryStep`
Defines a query in a multi-step SQL transformation.

| Property | Type | Required | Format | Description |
| --- | --- | :---: | :---: | --- |
| `alias` | `string` |  |  | Name of the temporary view that will be created from result of the query. Step without this alias will be treated as an output of the transformation. |
| `query` | `string` | ✔️ |  | SQL query the result of which will be exposed under the alias. |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://github.com/open-data-fabric/open-data-fabric/tree/master/schemas/fragments/SqlQueryStep.json)
[![Flatbuffers Schema](https://img.shields.io/badge/schema-flatbuffers-blue)](https://github.com/open-data-fabric/open-data-fabric/tree/master/schemas-generated/flatbuffers/opendatafabric.fbs)

<a name="temporaltable-schema"></a>
## `TemporalTable`
Temporary Flink-specific extension for creating temporal tables from streams.

| Property | Type | Required | Format | Description |
| --- | --- | :---: | :---: | --- |
| `name` | `string` | ✔️ |  | Name of the dataset to be converted into a temporal table. |
| `primaryKey` | `array(string)` | ✔️ |  | Column names used as the primary key for creating a table. |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://github.com/open-data-fabric/open-data-fabric/tree/master/schemas/fragments/TemporalTable.json)
[![Flatbuffers Schema](https://img.shields.io/badge/schema-flatbuffers-blue)](https://github.com/open-data-fabric/open-data-fabric/tree/master/schemas-generated/flatbuffers/opendatafabric.fbs)

<a name="transform-schema"></a>
## `Transform`
Engine-specific processing queries that shape the resulting data.

| Union Type | Description |
| --- | --- |
| [`Transform::Sql`](#transform-sql-schema) | Transform using one of the SQL dialects. |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://github.com/open-data-fabric/open-data-fabric/tree/master/schemas/fragments/Transform.json)
[![Flatbuffers Schema](https://img.shields.io/badge/schema-flatbuffers-blue)](https://github.com/open-data-fabric/open-data-fabric/tree/master/schemas-generated/flatbuffers/opendatafabric.fbs)

<a name="transform-sql-schema"></a>
## `Transform::Sql`
Transform using one of the SQL dialects.

| Property | Type | Required | Format | Description |
| --- | --- | :---: | :---: | --- |
| `engine` | `string` | ✔️ |  | Identifier of the engine used for this transformation. |
| `version` | `string` |  |  | Version of the engine to use. |
| `query` | `string` |  |  | SQL query the result of which will be used as an output. This is a convenience property meant only for defining queries by hand. When stored in the metadata this property will never be set and instead will be converted into a single-iter `queries` array. |
| `queries` | `array(`[`SqlQueryStep`](#sqlquerystep-schema)`)` |  |  | Specifies multi-step SQL transformations. Each step acts as a shorthand for `CREATE TEMPORARY VIEW <alias> AS (<query>)`. Last query in the array should have no alias and will be treated as an output. |
| `temporalTables` | `array(`[`TemporalTable`](#temporaltable-schema)`)` |  |  | Temporary Flink-specific extension for creating temporal tables from streams. |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://github.com/open-data-fabric/open-data-fabric/tree/master/schemas/fragments/Transform.json)
[![Flatbuffers Schema](https://img.shields.io/badge/schema-flatbuffers-blue)](https://github.com/open-data-fabric/open-data-fabric/tree/master/schemas-generated/flatbuffers/opendatafabric.fbs)


<a name="transforminput-schema"></a>
## `TransformInput`
Describes a derivative transformation input

| Property | Type | Required | Format | Description |
| --- | --- | :---: | :---: | --- |
| `datasetRef` | `string` | ✔️ | [`dataset-ref`]({{<relref "spec#dataset-identity">}}) | A local or remote dataset reference. When block is accepted this MUST be in the form of a DatasetId to guarantee reproducibility, as aliases can change over time. |
| `alias` | `string` |  |  | An alias under which this input will be available in queries. Will be populated from `datasetRef` if not provided before resolving it to DatasetId. |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://github.com/open-data-fabric/open-data-fabric/tree/master/schemas/fragments/TransformInput.json)
[![Flatbuffers Schema](https://img.shields.io/badge/schema-flatbuffers-blue)](https://github.com/open-data-fabric/open-data-fabric/tree/master/schemas-generated/flatbuffers/opendatafabric.fbs)

<a name="watermark-schema"></a>
## `Watermark`
Represents a watermark in the event stream.

| Property | Type | Required | Format | Description |
| --- | --- | :---: | :---: | --- |
| `systemTime` | `string` | ✔️ | [`date-time`](https://json-schema.org/draft/2019-09/json-schema-validation.html#rfc.section.7.3.1) |  |
| `eventTime` | `string` | ✔️ | [`date-time`](https://json-schema.org/draft/2019-09/json-schema-validation.html#rfc.section.7.3.1) |  |

[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)](https://github.com/open-data-fabric/open-data-fabric/tree/master/schemas/fragments/Watermark.json)
[![Flatbuffers Schema](https://img.shields.io/badge/schema-flatbuffers-blue)](https://github.com/open-data-fabric/open-data-fabric/tree/master/schemas-generated/flatbuffers/opendatafabric.fbs)

