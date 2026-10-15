---
# !!! THIS FILE IS AUTO-GENERATED - DO NOT MODIFY MANUALLY !!!
title: "Engine Contract"
---

import {Diagram, Term, Schema, YouTube, YouTubeList} from '/components/common.jsx'

**Domain**: Transformations\
**Depends on**: [Data Model](/odf/spec/datasets/data-model)\
**RFCs**: [RFC-015](/odf/rfcs/015-unified-changelog-stream-schema)


## Abstract

This spec defines the contract between a <Term t="Coordinator" id="coordinator"/> and an <Term t="Engine" id="engine"/> - the sandboxed execution environment of engines, the communication interface and the operations engines must support, and how engine versions are pinned and deprecated to preserve reproducibility of transformations.


## Execution Model
<Term t="Engine" id="engine"/> executes in a very restricted environment (a "sandbox") that prevents it from accessing any external resources other than those explicitly provided by the <Term t="Coordinator" id="coordinator"/>. Isolating the <Term t="Engine" id="engine"/> from making network calls and accessing any random files ensures both that the <Term t="Data" id="data"/> being processed cannot be leaked, and that non-deterministic behavior is harder to introduce accidentally.

Our isolation technology of choice is  [OCI containers](https://opencontainers.org/) - a lightweight mechanism that provides good performance and strong isolation guarantees. We rely on OCI-compatible images as the distribution mechanism for the engines.

> **WIP:** Add exact `podman` and `docker` commands to reproduce the sandboxed environment


## Communication Interface
This section describes the [RPC](https://en.wikipedia.org/wiki/Remote_procedure_call) mechanism used in communications between the <Term t="Coordinator" id="coordinator"/> and the <Term t="Engine" id="engine"/>.

The requirements we put towards the RPC mechanism are:
- Use common network protocols
- Wide support in many programming languages
- Support streaming responses (e.g. for streaming back the operation status and logs)

Our RPC technology of choice is [gRPC](https://grpc.io/) because:
- It's cross-platform, mature, and available in many languages
- Natively supports [FlatBuffers](https://google.github.io/flatbuffers/flatbuffers_grpc_guide_use_cpp.html) which is our [metadata format](/odf/spec/datasets/metadata-chain#metadata-format) of choice, letting us reuse object schemas
- Supports streaming
- For our narrow use case, its convenience is more important than interoperability, as we don't expect to have many server and client implementations

<Term t="Engine" id="engine"/> implementations must expose the `gRPC` API on port `5544`.

Request and response messages are defined by the [message schemas](#message-schemas) and serialized using FlatBuffers. Every operation responds with a stream of messages, where zero or more `Progress` messages are followed by exactly one terminal message:
- `Success` - operation completed successfully
- `InvalidQuery` - the query did not pass validation, with a `message` explaining the error
- `InternalError` - an unexpected error occurred, with a `message` and an optional `backtrace` with details

> Note: When starting an <Term t="Engine" id="engine"/> container, the <Term t="Coordinator" id="coordinator"/> will consider it fully initialized when it can establish a TCP connection to the port `5544`.


### Data Exchange
The exchange of raw data happens out-of-band of the `gRPC` API.

Currently, data and checkpoints are exchanged via files and object stores. The <Term t="Coordinator" id="coordinator"/> makes input data part files and the previous <Term t="Checkpoint" id="checkpoint"/> available to the <Term t="Engine" id="engine"/> and passes their paths in the request, along with the paths where the <Term t="Engine" id="engine"/> must write the output data and the new <Term t="Checkpoint" id="checkpoint"/>.

In future, input and output <Term t="Data Slices" id="data-slice"/> may be also exchanged using memory-mapped files (`mmap`) containing data in the common [in-memory format](/odf/spec/datasets/data-model#in-memory-and-on-disk-formats). This avoids any intermediate IO and minimizes the copying of data for the best performance.


## Operations
Engine implementation should support the following operations:
- [Execute query](#execute-query) - Performs the next iteration of the transformation.
- [Raw query](#raw-query) - Executes a query over raw data, e.g. during preprocessing of data in ingest.
- [Validate query](#validate-query) - Validates the user-specified query for basic syntax and schema correctness.
- [Migrate query](#migrate-query) - Updates the transformation state from one query to another.
- [Derive Provenance](#derive-provenance) - Explains the origin of some data produced in the past.

> **WIP:** Validate query, Migrate query, and Derive Provenance operations do not yet have defined [message schemas](#message-schemas).


### Execute Query
This operation is used by the <Term t="Coordinator" id="coordinator"/> to perform the next iteration of the transformation.

The <Term t="Coordinator" id="coordinator"/> is designed to isolate the <Term t="Engines" id="engine"/> from the complexity of managing the <Term t="Metadata Chain" id="metadata-chain"/> and make processing look as close as possible to a regular stream processing.

<Diagram src="/images/odf/specs/transformations/engine-contract/engine_transform.svg" alt="Sequence Diagram: Execute Query"/>

Inputs (`TransformRequest`):
- ID and alias of the output <Term t="Dataset" id="dataset"/>
- <Term t="System Time" id="system-time"/> to assign to new records
- Offset to assign to the first new record
- Vocabulary of the output <Term t="Dataset" id="dataset"/> - mapping of system columns onto its schema
- Transformation <Term t="Query" id="query"/>
- Inputs - for every input <Term t="Dataset" id="dataset"/>:
  - ID and alias of the dataset
  - Alias under which the input is referred to in the <Term t="Query" id="query"/>
  - Vocabulary of the input dataset
  - Offset interval of the input <Term t="Data Slice" id="data-slice"/> that goes into this transaction
  - Schema and data files of the input
  - Explicit <Term t="Watermarks" id="watermark"/> that should be injected into the stream to separate micro-batches for reproducibility
- Previous <Term t="Checkpoint" id="checkpoint"/>
- Locations where new data and the new <Term t="Checkpoint" id="checkpoint"/> should be written

Outputs (`TransformResponse`):
- Offset interval of the output <Term t="Data Slice" id="data-slice"/>, if any data was produced
- Output <Term t="Watermark" id="watermark"/>, if it was advanced
- New <Term t="Checkpoint" id="checkpoint"/>
- Operation progress and status

This operation must be [idempotent](https://en.wikipedia.org/wiki/Idempotence).

Input and output data are changelog streams that can contain <Term t="retractions and corrections" id="retractions-and-corrections"/> (see [Processing Model: Retractions and Corrections](/odf/spec/transformations/processing-model#retractions-and-corrections)). The <Term t="Engine" id="engine"/> must:
- Consume input records in the order of their <Term t="Offsets" id="offset"/>, as the order of retractions and corrections relative to the events they apply to is significant
- Take the operation type of input records into account and propagate retractions and corrections into the output
- Produce output that is a valid changelog stream (see [Data Model](/odf/spec/datasets/data-model#representation-of-retractions-and-corrections)) - in particular, it must not reorder records in a way that separates a correction pair or places a retraction before the event it retracts, and must write both events of a correction pair into the same output <Term t="Data Slice" id="data-slice"/>

Engines that process data in batches and parallelize work must preserve the order of records (e.g. by coalescing inputs into one partition). Such engines that only support simple record-by-record operations (like `map` and `filter`) must propagate the operation type column as-is, so that operations apply identically to appends, retractions, and corrections and produce a valid changelog stream.

When an operation is committed by the <Term t="Coordinator" id="coordinator"/>, the <Term t="Engine" id="engine"/> will not see the same input data again. If due to the nature of the query (e.g. windowing or watermarking configuration) <Term t="Engine" id="engine"/> cannot fully process and discard the input data - it should use the <Term t="Checkpoint" id="checkpoint"/> to buffer it.


### Raw Query
This operation is used by the <Term t="Coordinator" id="coordinator"/> to execute a <Term t="Query" id="query"/> over raw data that is not yet part of any dataset, e.g. during the preprocessing step of <Term t="Ingestion" id="ingestion"/>.

Inputs (`RawQueryRequest`):
- Input data files to perform the query over - all files must have identical schema
- Transformation <Term t="Query" id="query"/>
- Location where the query result should be written

Outputs (`RawQueryResponse`):
- Number of records produced by the query
- Operation progress and status


### Validate Query
This operation may be used by the <Term t="Coordinator" id="coordinator"/> when creating a new <Term t="Derivative Dataset" id="derivative-dataset"/> or when changing the <Term t="Query" id="query"/> of an existing one to validate the user-specified query for basic syntax and schema correctness.

Inputs:
- <Term t="Schemas" id="schema"/> of the input <Term t="Datasets" id="dataset"/>
- <Term t="Query" id="query"/>
- (optional) Previous <Term t="Query" id="query"/> in case of an existing <Term t="Dataset" id="dataset"/> modification

Outputs:
- <Term t="Schema" id="schema"/> of the result
- (alternatively) Validation errors


### Migrate Query
This operation is used by the <Term t="Coordinator" id="coordinator"/> when data processing hits the point where one transformation <Term t="Query" id="query"/> is being replaced by another one. It gives the <Term t="Engine" id="engine"/> all information needed to handle the transition as gracefully as possible, e.g. by reconciling the existing <Term t="Checkpoints" id="checkpoint"/> with the new <Term t="Query" id="query"/>, or, at the very least, finalizing the processing of the old <Term t="Query" id="query"/> and clearing the <Term t="Checkpoints" id="checkpoint"/> before the new one starts to execute.

Inputs:
- Transaction ID
- Previous <Term t="Query" id="query"/>
- Next <Term t="Query" id="query"/>
- Previous <Term t="Checkpoint" id="checkpoint"/>

Outputs:
- New <Term t="Checkpoint" id="checkpoint"/>
- (optional) <Term t="Data" id="data"/> that has been produced when finalizing the old <Term t="Query" id="query"/>


### Derive Provenance
This operation is used to trace back a set of events in the output <Term t="Dataset" id="dataset"/> to input events that contributed to their values or their existence (see <Term t="Provenance" id="provenance"/>).

> **WIP:** The design of this operation is in progress.


## Engine Versioning
As described in [Components of Trust](/odf/spec/overview#components-of-trust), to guarantee the reproducibility and verifiability of the results a transformation must be associated with an exact version of an <Term t="Engine" id="engine"/> that is used to perform it. We want to exclude any possibility that the code changes in the <Term t="Engine" id="engine"/> will break this guarantee.

Whenever the <Term t="Coordinator" id="coordinator"/> uses an <Term t="Engine" id="engine"/> to execute a query it must specify the full digest of the OCI container image in the resulting <Term t="Metadata Block" id="metadata-chain"/>. <Term t="Engine" id="engine"/> maintainers are therefore responsible for treating the images as immutable and ensure old versions are never lost.

See also:
- [Engine Deprecation](#engine-deprecation)


## Engine Deprecation
Pinning the exact <Term t="Engine" id="engine"/> version used by every transformation guarantees the reproducibility and verifiability of the results (see [Components of Trust](/odf/spec/overview#components-of-trust)). In the long run, however, this creates a problem where in order to [verify a dataset](/odf/spec/transformations/processing-model#verification) the <Term t="Coordinator" id="coordinator"/> will have to use a very large number of different versions of an <Term t="Engine" id="engine"/> that might've accumulated over the years. This slows down the verification procedure and can result in a significant disk space required for storing these images.

To mitigate this problem the <Term t="Coordinator" id="coordinator"/> offers the **engine deprecation** operation that works as follows:
1. The <Term t="Coordinator" id="coordinator"/> reconstructs the dataset from scratch by repeating all transformation in the <Term t="Metadata Chain" id="metadata-chain"/>.
2. Instead of the <Term t="Engine" id="engine"/> version specified in the block, it uses the latest (or provided) version.
3. If the results produced in every step match the recorded ones - we can safely consider that the newer version of the <Term t="Engine" id="engine"/> is fully compatible with the older one.
4. A special <Term t="Metadata" id="metadata-chain"/> record is created to record this compatibility, therefore, allowing all users to use the latest version of the <Term t="Engine" id="engine"/> instead of downloading all the versions seen previously.


## Message Schemas
Messages exchanged between the <Term t="Coordinator" id="coordinator"/> and the <Term t="Engine" id="engine"/> are defined by the following schemas:

| Schema | Description |
| --- | --- |
| <Schema t="TransformRequest" id="transformrequest"/> | Sent by the coordinator to perform the next step of data transformation |
| <Schema t="TransformRequestInput" id="transformrequestinput"/> | Describes an input of the transform request |
| <Schema t="TransformResponse" id="transformresponse"/> | Sent by the engine when performing the data transformation |
| <Schema t="RawQueryRequest" id="rawqueryrequest"/> | Sent by the coordinator to perform a query on raw input data |
| <Schema t="RawQueryResponse" id="rawqueryresponse"/> | Sent by the engine when performing the raw query |
