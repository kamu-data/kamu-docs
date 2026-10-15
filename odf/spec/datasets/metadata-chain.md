---
# !!! THIS FILE IS AUTO-GENERATED - DO NOT MODIFY MANUALLY !!!
title: "Metadata Chain"
---

import {Diagram, Term, Schema, YouTube, YouTubeList} from '/components/common.jsx'

**Domain**: Datasets
**Depends on**: [Data Model](/odf/spec/datasets/data-model), [Data Schema](/odf/spec/datasets/data-schema), [Data & Checkpoint Hashing](/odf/spec/datasets/data-and-checkpoint-hashing)
**RFCs**: [RFC-004](/odf/rfcs/004-metadata-extensibility), [RFC-005](/odf/rfcs/005-dataset-annotations), [RFC-010](/odf/rfcs/010-data-schema-in-metadata), [RFC-012](/odf/rfcs/012-recommend-base16-encoding), [RFC-014](/odf/rfcs/014-minimize-offset-scanning)


## Abstract

This spec defines the structure of the <Term t="Metadata Chain" id="metadata-chain"/> - the append-only log of blocks that captures the entire history of a <Term t="Dataset" id="dataset"/>. It defines metadata blocks and the events they carry, the rules that keep the chain consistent, the formats used to represent metadata, and how blocks and other objects are hashed and linked together.


## Metadata Blocks
The metadata chain consists of individual **metadata blocks** (<Schema t="MetadataBlock" id="metadatablock"/>) that refer to the previous block in the chain, forming a singly-linked list. Every block contains:
- `systemTime` - <Term t="System Time" id="system-time"/> when the block was written
- `prevBlockHash` - [hash](#metadata-block-hashing) of the preceding block (absent in the first block)
- `sequenceNumber` - sequence number of the block, starting from zero at the first block
- `event` - one [metadata event](#metadata-events) that describes the transaction that occurred on the dataset

<Diagram src="/images/odf/specs/datasets/metadata-chain/metadata-chain.svg" alt="Diagram: Metadata Chain"/>

Blocks are immutable - the chain only changes by appending new blocks. Since blocks, data part files, and checkpoints are named after and referenced by the hash of their content, a dataset forms a [content-addressable](https://en.wikipedia.org/wiki/Content-addressable_storage) graph, where having a reference to the last block one can traverse the entire chain to discover all components of the dataset (see [Storage Layout](/odf/spec/datasets/storage-layout)).

<Diagram src="/images/odf/specs/datasets/metadata-chain/metadata-chain-2.svg" alt="Diagram: Dataset as a Content-Addressable Graph"/>

A block contains exactly one event. Bringing a dataset into a desired state may therefore require several blocks. Consistency is achieved similarly to `git` - a group of blocks that constitutes a consistent state is committed atomically by updating the [block reference](#block-references).


## Metadata Events
Every event (<Schema t="MetadataEvent" id="metadataevent"/>) corresponds to a certain transaction on the dataset and contains only the fields relevant to it.


### Core Events

| Event | Description |
| --- | --- |
| <Schema t="Seed" id="seed"/> | Establishes the identity (`datasetId`) and the kind (`Root` or `Derivative`) of the dataset. Always the first event in the chain |
| <Schema t="SetDataSchema" id="setdataschema"/> | Specifies the complete <Term t="schema" id="schema"/> of <Term t="Data Slices" id="data-slice"/> added to the dataset following this event (see [Data Schema](/odf/spec/datasets/data-schema)) |
| <Schema t="SetVocab" id="setvocab"/> | Specifies the names of the system columns (see [Data Model](/odf/spec/datasets/data-model#common-data-schema)) |
| <Schema t="AddData" id="adddata"/> | Indicates that data has been ingested into a <Term t="Root Dataset" id="root-dataset"/> (see [Ingestion](/odf/spec/datasets/ingestion#committing-data)) |
| <Schema t="SetTransform" id="settransform"/> | Defines the inputs and the <Term t="Query" id="query"/> that produce data of a <Term t="Derivative Dataset" id="derivative-dataset"/> |
| <Schema t="ExecuteTransform" id="executetransform"/> | Indicates that a derivative transformation has been performed |

`AddData` and `ExecuteTransform` events describe the outcome of a transaction:
- `prevOffset` and `newData` (<Schema t="DataSlice" id="dataslice"/>) - the last offset of the previous data slice, and the new data slice with its [physical and logical hashes](/odf/spec/datasets/data-and-checkpoint-hashing), offset interval, and size
- `prevCheckpoint` and `newCheckpoint` (<Schema t="Checkpoint" id="checkpoint"/>) - the <Term t="Checkpoint" id="checkpoint"/> used to restore the processing state and the new checkpoint with its physical hash and size
- `newWatermark` - the new <Term t="Watermark" id="watermark"/> of the dataset

In addition, `AddData` carries the `newSourceState` (see [Source State](/odf/spec/datasets/ingestion#source-state)), while `ExecuteTransform` carries `queryInputs` (<Schema t="ExecuteTransformInput" id="executetransforminput"/>) - the intervals of blocks and records of every input dataset that were used in the transaction.

A transaction may produce no new data and still be committed, e.g. to advance the watermark or to update the source state.

`SetDataSchema` events are normally not specified by users, but are generated by implementations when the schema of the data is first established (e.g. during the first ingestion or transformation) and when it evolves. Multiple `SetDataSchema` events can appear in the chain according to the [Schema Evolution](/odf/spec/datasets/data-model#schema-evolution) rules.


### Annotation Events
Annotation events provide human-oriented information about the dataset:

| Event | Description |
| --- | --- |
| <Schema t="SetInfo" id="setinfo"/> | Brief description and keywords of the dataset |
| <Schema t="SetLicense" id="setlicense"/> | License that applies to the dataset, with an optional [SPDX](https://spdx.org/licenses/) identifier |
| <Schema t="SetAttachments" id="setattachments"/> | Files associated with the dataset (e.g. a README), currently only in the form of items embedded in the metadata |

Example:

```yaml
- kind: SetInfo
  description: Confirmed positive cases of COVID-19 in Ontario
  keywords:
    - Healthcare
    - Epidemiology
- kind: SetLicense
  shortName: OGL-Ontario
  name: Open Government Licence - Ontario
  websiteUrl: https://www.ontario.ca/page/open-government-licence-ontario
- kind: SetAttachments
  attachments:
    kind: Embedded
    items:
      - path: README.md
        content: |
          # Confirmed positive cases of COVID-19 in Ontario
          Detailed description follows...
```

The metadata chain is not meant to replace version control systems - larger sets of files (e.g. notebooks) are expected to be associated with datasets by referencing external systems.


### Legacy Events
> **Deprecated:** The `SetPollingSource`, `DisablePollingSource`, `AddPushSource`, and `DisablePushSource` events used to define ingestion sources in the metadata chain. They are superseded by `Source` resources, but can still appear in existing chains. See [Ingestion: Legacy Source Events](/odf/spec/datasets/ingestion#legacy-source-events).


## Consistency Rules
Implementations must ensure that:
- The first block of the chain contains the `Seed` event, and `Seed` appears only once
- Every block except the first refers to the hash of the preceding block, and sequence numbers increase by one with every block
- `AddData` events only appear in root datasets, while `SetTransform` and `ExecuteTransform` only appear in derivative datasets
- All data slices conform to the schema defined by the last preceding `SetDataSchema` event
- Watermarks are monotonically non-decreasing - once a watermark is set, all subsequent blocks either carry the same watermark or specify a greater one
- If a transaction did not update the checkpoint but it is still relevant for subsequent transactions, the hash of the previous checkpoint is carried over into `newCheckpoint`
- Data slices, checkpoints, and input datasets referenced by blocks have valid hashes


### Offsets and Intervals
`AddData` and `ExecuteTransform` events always carry enough information to prepare the next transaction from the last such event, without deep scanning of the chain:
- `prevOffset` is equal to the end of the offset interval of the last non-empty `newData`, or is absent if no data was written yet
- The `newData.offsetInterval` of the next non-empty slice starts at `prevOffset + 1` (or `0`)

For example, a chain of `AddData` events where the last one only advances the watermark:

```yaml
- prevOffset: null
  newData:
    offsetInterval: {start: 0, end: 9}
  newWatermark: "2023-12-31T00:00:00Z"
- prevOffset: 9
  newData:
    offsetInterval: {start: 10, end: 19}
  newWatermark: "2023-12-31T01:00:00Z"
- prevOffset: 19
  newData: null
  newWatermark: "2023-12-31T03:00:00Z"
```

Similarly, `queryInputs` of `ExecuteTransform` describe the inputs using half-open intervals `(prevBlockHash, newBlockHash]` and `(prevOffset, newOffset]`, where the starting point is always carried over from the previous transaction, even when the interval itself is empty.


## Validation
Since metadata blocks are content-addressed, a chain obtained from any untrusted source can be validated by knowing only the hash of its last block, obtained from a trusted source. Validation involves:
- Recomputing the [hash](#metadata-block-hashing) of every block and comparing it to the hash by which the block was referenced (via a [block reference](#block-references) or the `prevBlockHash` of the following block)
- Checking that all [consistency rules](#consistency-rules) are satisfied

A valid chain guarantees the integrity of all data slices and checkpoints it references, as long as their hashes are also validated (see [Data & Checkpoint Hashing: Validation and Verification](/odf/spec/datasets/data-and-checkpoint-hashing#validation-and-verification)).


## Block References
**Block references** assign symbolic names to block hashes, effectively acting as named pointers. All datasets have a `head` reference that points to the current last block of the chain.

Using multiple references the chain can be organized into a directed acyclic graph that forms branches, e.g. to stage a subset of events for review or an automated QA process before they are accepted into the main chain. The semantics of references other than `head` are not yet specified.


## Extensibility
The metadata chain is designed to be extended with new event types that carry other kinds of information, such as:
- Meaning and structure of knowledge that data represents (glossary, semantics, ontology)
- Relevant policies, terms, rules, compliance, and regulations (governance)
- License, privacy, and security concerns (stewardship)
- Information that aids discovery
- Collaboration information

Some events (e.g. `AddData`) also carry the `extra` field (<Schema t="ExtraAttributes" id="extraattributes"/>) that allows attaching custom information to the event, with keys in the `<domain>/<attribute-name>` format (see [Data Schema: Extra Attributes](/odf/spec/datasets/data-schema#extra-attributes)).


## Metadata Format
The requirements we put towards the metadata format are:
- Compactness
- Fast read performance
- Complex type support (particularly nested structures and unions)
- Allows for forward and backward compatibility
- Allows for a controlled way of making breaking changes
- Possibility to read and write in human-friendly easily editable format
- Schema-based validation for user-specified data

We use the following combination of formats to satisfy these requirements:
- [YAML](https://yaml.org/) is used for human-friendly input and output
  - This format is concise and very readable and widely supported
  - Only a [JSON-compatible](https://json.org/) subset of `YAML` is used
- [JSON Schema](https://json-schema.org/) is used for validating user-specified `YAML` files
  - Widely supported and expressive grammar for validating `JSON` and `YAML`
  - Generates readable and easy to understand errors
- [FlatBuffers](https://google.github.io/flatbuffers/) format is used for binary representation
  - Highly efficient and cross-platform serialization format

The JSON Schemas of all metadata objects are provided in the [`schemas`](https://github.com/open-data-fabric/open-data-fabric/tree/master/schemas) directory, and the FlatBuffers schema is [generated](https://github.com/open-data-fabric/open-data-fabric/blob/master/contracts/metadata/opendatafabric.fbs) from them.


## Hash Representation
To be able to evolve hashing algorithms over time we encode the identity of the algorithm used along with the hash sum itself using the [multiformats](https://github.com/multiformats/multiformats) specification, specifically:
- [multihash](https://github.com/multiformats/multihash) - describes how to encode algorithm ID alongside the hash value.
- [multibase](https://github.com/multiformats/multibase) - describes encoding used to represent a binary value as text (e.g. in YAML format or as a file name) without ambiguity of which encoding was used.

It is expected that the specific `multibase` encoding is largely a presentation-layer concern that can vary between implementations. For protocol compatibility all implementations must support all encodings in the `final` state of approval in the [`multibase` specification](https://github.com/multiformats/multibase), transcoding the representations when needed.

For consistency, we recommend implementations to prefer the `base16` encoding. Although it produces longer hashes than other encodings, it:
- Is case-insensitive and can appear in subdomains
- Does not contain symbols that can be easily confused
- Does not have a risk of forming an accidental obscenity
- Does not require padding
- Is easier to use for partitioning by prefix

For representing the identity of hashing algorithms the official [multicodec](https://github.com/multiformats/multicodec/) table is used.


## Metadata Block Hashing
Blocks of the metadata chain are referred to and linked together using their cryptographic hashes. The process of serializing and computing a stable hash is as follows:

1. The <Schema t="MetadataBlock" id="metadatablock"/> is serialized into [FlatBuffers](https://google.github.io/flatbuffers/) format following a two-step process to ensure that all variable-size buffers are laid out in memory in a consistent order:
   1. First, we iterate over all fields of the block in the same order they appear in the schemas serializing into buffers all vector-like and variable-size fields and recursing into nested data structures (tables) in the depth-first order.
   2. Second, we iterate over all fields again this time serializing all leftover fixed-size fields
2. Block content is then nested into a [`Manifest`](https://github.com/open-data-fabric/open-data-fabric/blob/master/schemas/legacy/v0/Manifest.json) object using same serialization rules as above
3. The resulting `flatbuffer` data is fed into [SHA3-256](https://en.wikipedia.org/wiki/SHA-3) digest algorithm.

For use in the `Manifest`'s `kind` field the `multicodec` table is extended with the following codes in the "private use area":

| Codec | Code |
| --- | --- |
| `odf-metadata-block` | `0x400000` |

The block hashes are represented using [multihash](https://github.com/multiformats/multihash) and [multibase](https://github.com/multiformats/multibase) described [above](#hash-representation).


## Populating the Chain
The initial events of a dataset are specified via the `metadata` field of the `Dataset` <Term t="resource" id="resource"/> (<Schema t="DatasetSpec" id="datasetspec"/>). When the resource is applied, the node creates the `Seed` block and appends a block for every specified event:

```yaml
$schema: https://opendatafabric.org/schemas/datasets/v1alpha1/Dataset
headers:
  name: ca.bankofcanada
spec:
  kind: Root
  metadata:
    - kind: SetInfo
      description: Daily exchange rates published by the Bank of Canada
    - kind: SetLicense
      shortName: Apache-2.0
      name: Apache 2.0
      spdxId: Apache-2.0
      websiteUrl: https://www.apache.org/licenses/LICENSE-2.0
```

Subsequent blocks are appended by ingestion and transformation processes.

As the dataset evolves, the `metadata` field of the resource maintains a **snapshot** of the key events that describe the dataset in its present (latest) state. The snapshot excludes:
- All intermediate transitions, e.g. when the schema changes multiple times only the latest `SetDataSchema` event is retained
- All events related to ingestions and transformations, like `AddData` and `ExecuteTransform`

The metadata chain, on the other hand, preserves the full history of all events.


## Schemas

| Schema | Description |
| --- | --- |
| <Schema t="MetadataBlock" id="metadatablock"/> | Block of the metadata chain |
| <Schema t="MetadataEvent" id="metadataevent"/> | Union of all metadata events |
| <Schema t="DataSlice" id="dataslice"/> | Data part file added in a transaction |
| <Schema t="Checkpoint" id="checkpoint"/> | Checkpoint file written in a transaction |
| <Schema t="OffsetInterval" id="offsetinterval"/> | Closed interval of record offsets |
| <Schema t="ExecuteTransformInput" id="executetransforminput"/> | Input of a derivative transformation |
| <Schema t="TransformInput" id="transforminput"/> | Input dataset of a `SetTransform` |
| <Schema t="Transform" id="transform"/> | Engine-specific transformation query |
| <Schema t="DatasetVocabulary" id="datasetvocabulary"/> | Names of the system columns |
| <Schema t="Attachments" id="attachments"/> | Files associated with a dataset |
| [`Manifest`](https://github.com/open-data-fabric/open-data-fabric/blob/master/schemas/legacy/v0/Manifest.json) | Legacy wrapper used in block hashing |
