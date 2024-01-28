---
# !!! THIS FILE IS AUTO-GENERATED - DO NOT MODIFY MANUALLY !!!
Title: Glossary
description: Definitions of commonly used terms in Open Data Fabric and Kamu projects
weight: 50
topLevelElement: true
categories: []
aliases:
---


# Open Data Fabric
## Event
As described in the [Nature of Data]({{<relref "spec#nature-of-data">}}) section, the system operates only on data expressed as past events, observations, or propositions believed to be true at a certain time. For simplicity, we will use the term "event" throughout to refer to such data tuples.

## Data
Data is a set of {{<term "Events" "event">}} stored in the system. Since events are immutable data can only grow over time. Conceptually it's best to think of data as a full log of a potentially infinite event stream.

Data never appears in the system alone as we would not be able to tell where it came from and whether it can be trusted. Data always appears as part of a {{<term "Dataset" "dataset">}}.

{{<image filename="/images/pages/glossary/dataset.svg" alt="Diagram: Dataset/Data">}}

See also:
- [Data Format]({{<relref "spec#data-format">}})
- [Common Data Schema]({{<relref "spec#common-data-schema">}})

## Schema
Schema describes the shape of the {{<term "data" "data">}} by associating names and data types to columns that data is composed of. Schema can change over time and its changes are tracked in the {{<term "Metadata Chain" "metadata-chain">}}.

Example:
```
registration_time TIMESTAMP(3),
registration_id UUID,
email STRING,
first_name STRING,
last_name STRING,
date_of_birth DATE,
```

See also:
- [Schema Format]({{<relref "spec#schema-format">}})
- [Schema Evolution]({{<relref "spec#schema-evolution">}})

## Offset
Offset is a monotonically increasing sequential numeric identifier that is assigned to every record and represents its position relative to the beginning of the dataset. Offsets are used to uniquely identify any record in the dataset. Offset of the first record in a dataset is `0`.

## Operation Type
Since past {{<term "Events" "event">}} are immutable, if some event is deemed incorrect later on it can only be rectified by issuing an explicit {{<term "retraction or correction" "retractions-and-corrections">}}. Retraction and corrections are also represented as {{<term "Events" "event">}} in the same stream of {{<term "Data" "data">}} and differentiated by a special "operation type" field.

See also:
- [Common data schema]({{<relref "spec#common-data-schema">}})
- [Representation of retractions and corrections]({{<relref "spec#representation-of-retractions-and-corrections">}})

## Data Slice
{{<term "Data" "data">}} arrives into the system as the arbitrary large sets of events. We refer to them as "slices".

More formally, a slice is a:
- Continuous part of {{<term "Data" "data">}}
- That has the same {{<term "Schema" "schema">}}
- Defined by its `[start; end]` {{<term "Offset" "offset">}} interval

{{<image filename="/images/pages/glossary/metadata.svg" alt="Diagram: Data Slices and Metadata">}}

## Metadata
Refers to information about a {{<term "Dataset" "dataset">}} stored in its {{<term "Metadata Chain" "metadata-chain">}}.

## Metadata Chain
Metadata Chain captures all essential information about the {{<term "Dataset" "dataset">}}, including:
- Where the data comes from (see [Data Ingestion]({{<relref "spec#data-ingestion">}}))
- How data was processed (see {{<term "Query" "query">}})
- Its {{<term "Schema" "schema">}}
- Log of all modifications made to the data, including information used to verify the integrity of data
- Current {{<term "Watermark" "watermark">}}

Just like {{<term "Data" "data">}}, the metadata chain also has a temporal nature. It consists of individual **Metadata Blocks** that refer to the previous block in the chain, forming a singly-linked list. Every block carries one of {{<schema "Metadata Events" "metadata-events">}} that describes how data evolved over time.

{{<image filename="/images/pages/glossary/metadata-chain.svg" alt="Diagram: Metadata Chain">}}

All Metadata Blocks are immutable and changes by appending new blocks. With blocks, data, and checkpoints named after and referenced by the {{<term "hash" "hash">}} of their content - a dataset forms a type of [content-addressable](https://en.wikipedia.org/wiki/Content-addressable_storage) system, where having a reference to the last Metadata Block one can traverse the entire chain to discover all the components of the dataset.

{{<image filename="/images/pages/glossary/metadata-chain-2.svg" alt="Diagram: Dataset as a Content-Addressable Graph">}}

Metadata Chain also supports **Block References** that assign a certain symbolic name to a block hash, effectively acting as a named pointer. At the minimum all datasets have a `head` reference that indicates the current last block in the Metadata Chain. Using multiple references the metadata chain can be organized into a directed acyclic graph that can form branches, allowing for example to stage some subset of events for review or an automated QA process before they are accepted into the main chain.

In addition to core events like adding data, running a query, and change of schema the Metadata Chain is designed to be extended to carry other kinds of information like:
- Extra meaning and structure of knowledge that data represents (glossary, semantics, ontology)
- Relevant policies, terms, rules, compliance, and regulations (governance)
- License, privacy and security concerns (stewardship)
- Information that aids discovery
- Collaboration information

These extensions are out of scope of this document.

See also:
- [Metadata Format]({{<relref "spec#metadata-format">}})
- {{<schema "Metadata Events Reference" "metadata-events">}}

## Dataset
Dataset is the main unit of data exchange in the system. It's simply a combination of:
- [Identity]({{<relref "spec#dataset-identity">}})
- {{<term "Data" "data">}}
- {{<term "Metadata Chain" "metadata-chain">}}
- {{<term "Checkpoints" "checkpoint">}}

Depending on where the data comes from datasets can be of these kinds:
- {{<term "Root" "root-dataset">}}
- {{<term "Derivative" "derivative-dataset">}}

{{<image filename="/images/pages/glossary/dataset_graph.svg" alt="Diagram: Dataset Graph">}}

### Root Dataset
Root datasets are the points of entry of external data into the system. They are usually owned by the organization that has full authority and responsibility over that data, i.e. a trusted source.

Root dataset definition includes:
- Where to fetch the data from - e.g. source URL, a protocol to use, cache control
- How to prepare the binary data - e.g. decompression, file filtering, format conversions
- How to interpret the data - e.g. data format, schema to apply, error handling
- How to combine data ingested in the past with the new data - e.g. append as log or diff as a snapshot of the current state

All this information is stored in the {{<term "Metadata Chain" "metadata-chain">}} and can change over time as the dataset evolves.

See also:
- [Merge Strategy]({{<relref "spec#merge-strategies">}})

### Derivative Dataset
Derivative datasets are created by transforming/combining one or multiple existing datasets.

They are defined by the combination of:
- Input datasets
- A {{<term "Query" "query">}} to apply to those
- An {{<term "Engine" "engine">}} used to execute the query

This information is stored in the {{<term "Metadata Chain" "metadata-chain">}} and can change over time as the dataset evolves.

See also:
- [Derivative Data Transience]({{<relref "spec#derivative-data-transience">}})

## Query
Queries define how input data is combined, modified, and re-shaped to produce new data.

Queries are used in two contexts:
- When defining new {{<term "Derivative Datasets" "derivative-dataset">}}
- When analyzing and extracting data from an existing {{<term "Dataset" "dataset">}} (locally or from a {{<term "repository" "repository">}})

The system is agnostic to the exact language used to define the query and the set of supported dialects can be extended by implementing a new {{<term "Engine" "engine">}}.

All queries, however, must have the following properties:
- Deterministic
- Pure
- Stream/Batch agnostic

In other words, they should be guaranteed to always produce the same result for the same input data, without side effects.

Example windowed aggregation query in streaming SQL:

```sql
SELECT
  TUMBLE_ROWTIME(event_time, INTERVAL '1' MONTH) as event_time,
  sku_id,
  min(price) as min_monthly_price,
  max(price) as max_monthly_price,
  avg(price) as avg_monthly_price
FROM sku_prices
GROUP BY TUMBLE(event_time, INTERVAL '1' MONTH), sku_id
```

See also:
- [Stream Processing Model]({{<relref "spec#stream-processing-model">}})
- [Derivative Data Transience]({{<relref "spec#derivative-data-transience">}})
- [Engine Contract]({{<relref "spec#engine-contract">}})

## Engine
Engine is an interface shared by all specific implementations of a {{<term "Query" "query">}} dialect. Engine implementations are responsible for applying defined queries to input data and returning the result. For example, some engines allows you to query data using a series of streaming SQL statements.

Engines run in a sandboxed environments and are not permitted to use any external resources to guarantee the reproducibility of all operations.

{{<image filename="/images/pages/glossary/engine-execution-env.svg" alt="Diagram: Derivative Transformation">}}

As Engines are in the full control of all data transformations, they are also responsible for answering the {{<term "Provenance" "provenance">}} queries.

See also:
- [Engine Contract]({{<relref "spec#engine-contract">}})

## Checkpoint
Checkpoints are used by the {{<term "Engines" "engine">}} to store the computation state between the different invocations of a {{<term "Query" "query">}}. They are fully engine-specific and opaque to the system. They are however an essential durable part of a {{<term "Dataset" "dataset">}} as they are necessary to be able to pause and resume the streaming queries, and are essential in implementing "exactly-once" processing semantics.

## Coordinator
Coordinator is an application that implements the common {{<term "Dataset" "dataset">}} management logic.

Core responsibilities:
- Handles all {{<term "Metadata Chain" "metadata-chain">}} operations
- Splits the transformation work into batches based on the dataset's evolution timeline
- Collects relevant data slices of the input datasets
- Delegates data processing to the {{<term "Engines" "engine">}}, making all transformations look to them as conventional stream processing
- Commits the resulting data slices and new metadata blocks

See also:
- [Coordinator Contract]({{<relref "spec#coordinator-contract">}})

## Ingestion
Ingestion is the process by which external data gets into the system. Typical ingestion steps that describe how data is obtained and read (e.g. fetching data from some URL on the web, decompressing it, and reading it as CSV) are a part of the {{<term "Root Dataset" "root-dataset">}} definition.

See also:
- [Data Ingestion]({{<relref "spec#data-ingestion">}})

## Merge Strategy
By [design]({{<relref "spec#nature-of-data">}}), the system only stores data in the append-only event log format to preserve the entire history. Unfortunately, a lot of data in the world is not stored or exposed this way. Some organizations may expose their data in the form of periodic database dumps, while some choose to provide it as a log of changes between current and the previous export.

When {{<term "ingesting data" "ingestion">}} from external sources, the {{<term "Root Datasets" "root-dataset">}} can choose between different [Merge Strategies]({{<relref "spec#merge-strategies">}}) that define how to combine the newly-ingested data with the existing one.

For example, when dealing with the daily database dumps, a user can choose the merge strategy that performs [change data capture](https://en.wikipedia.org/wiki/Change_data_capture), transforming dumps into a set of events that signify record creation, update, or deletion.

See also:
- [Merge Strategies]({{<relref "spec#merge-strategies">}})

## Hash
[Cryptographic hash functions](https://en.wikipedia.org/wiki/Cryptographic_hash_function) are used by the system in these three scenarios:
- Computing a logical hash sum of a {{<term "Data Slice" "data-slice">}}.
- Computing a physical hash sum of a {{<term "Data Slice" "data-slice">}}.
- Computing a hash sum of a {{<term "MetadataBlock" "metadata-chain">}}.

Whenever new events are appended to the {{<term "Data" "data">}} the {{<term "Metadata Chain" "metadata-chain">}} will also be extended with a block containing a hash sum of the new data slice. The hash sum provides a very quick and reliable way to later validate that the data matches the one that has been written earlier.

The new {{<term "MetadataBlock" "metadata-chain">}} will also be cryptographically signed to guarantee its integrity - this excludes any malicious or accidental alterations to the block.

Usage examples:
- If the {{<term "Metadata Chain" "metadata-chain">}} of a certain dataset is reliably known (e.g. available from many independent peers) a peer can then download the {{<term "Data" "data">}} from any untrusted source and use the hash function to validate the authenticity of every data slice that composes it.
- The trustworthiness of any {{<term "Dataset" "dataset">}} can be established by reviewing the transformations it claims to be performing on data (contained in the {{<term "Metadata Chain" "metadata-chain">}}), re-applying those transformations in a trusted environment, and then comparing the hash sums of the result slices.

See also:
- [Data Hashing]({{<relref "spec#data-hashing">}})
- [Checkpoint Hashing]({{<relref "spec#checkpoint-hashing">}})
- [Metadata Block Hashing]({{<relref "spec#metadata-block-hashing">}})

## Provenance
Data provenance describes the origins and the history of data and adds value to data by explaining how it was obtained.

{{<term "Metadata Chain" "metadata-chain">}} alone can already significantly narrow down the search space when you want to explain how a certain piece of data came to be, as it keeps track of all the inputs and queries used to create a dataset. But the goal of the provenance system is to make this type of inquiry effortless.

We differentiate the following kinds of provenance:
- **Why-provenance** - tells us which input data elements were inspected to decide that an element should be present in the output at all - i.e. defines a sufficient set of elements needed to produce the output.
- **How-provenance** - tells us the process by which the elements of *why-provenance* caused the output to appear
- **Where-provenance** - narrows down *why-provenance* to input data elements that were copied or transformed to determine the output element value.

Since the {{<term "Engines" "engine">}} are responsible for all data transformations, it's also the Engine's responsibility to answer provenance queries.

There are many different ways to implement provenance:
- By statically analyzing the queries
- By inverting transformations
- By repeating the computations and logging the data used at every step
- By propagating provenance data through all computations

Depending on the language used by an {{<term "Engine" "engine">}} one approach may work better in one situation than the other, so we avoid prescribing the exact method to use but instead standardize the language used for provenance-related queries and responses.

See also:
- [Provenance in Databases: Why, How, and Where](http://homepages.inf.ed.ac.uk/jcheney/publications/provdbsurvey.pdf)
- [Engine Contract: Derive Provenance]({{<relref "spec#derive-provenance">}})

## Verifiability
In the scope of this specification, verifiability of data means the ability to establish:
- The ultimate source(s) of data:
  - Which {{<term "Root Datasets" "root-dataset">}} the data is coming from
  - Who these datasets belong to (ownership)
  - And which actor has added the specific records (accountability)
- The transformations performed to create this data:
  - The graph of {{<term "Derivative Datasets" "derivative-dataset">}} upstream to the one being verified
  - Authorship of those datasets (accountability)
- And finally, that the data in fact corresponds to performing declared transformations on the source data.

In other words, having root datasets `A`, `B` and a derivative dataset `C = f(A, B)`:
- The data in `A` (and similarly in `B`) is verifiable if:
  - {{<term "Metadata Chain" "metadata-chain">}} of `A` is valid
    - Metadata block hashes are valid, forming a valid chain
    - Blocks point to {{<term "Data Slices" "data-slice">}} and {{<term "Checkpoints" "checkpoint">}} with valid hashes
- The data in `C` is verifiable if:
  - {{<term "Metadata Chain" "metadata-chain">}} of `C` is valid
  - Data in `C` corresponds to applying `f(A, B)` according to all transformation steps declared in the {{<term "Metadata Chain" "metadata-chain">}}.

The last step of ensuring that `f(A, B) = C` can be achieved by several means:
- Reproducibility - by applying same transformations and comparing the results
- Verifiable computing - different types of proofs that can attest to validity of results without redoing the computations.

Examples of verifiable computing can include:
- [Trusted Execution Environments](https://en.wikipedia.org/wiki/Trusted_execution_environment) (TEEs)
- [Non-interactive Proofs](https://en.wikipedia.org/wiki/Non-interactive_zero-knowledge_proof) (including "zero-knowledge").

Verifiability should not be confused with *trustworthiness* or *reality* of data. Verifying a dataset doesn't prove that the data in it is either truthful or more "real" than other data. The value of verifiability comes from establishing the provenance of data so that:
- One could understand whether data is coming from reputable sources - sources they can trust (attribution)
- One could review all derivative transformations applied to the data by intermediate actors (auditability).

Verifiability provides the foundation upon which *trust* in data can be built:
- First in the form **authority** - organizations putting their name behind the data they publish
- Secondly in the form of **reputation** - trusting the sources or pipelines used by large parts of the community
- Thirdly in the form of **cross-validation** - e.g. performing outlier detection on data from several similar publishers to establish common truth.

## Time
The system applies the idea of [bitemporal data modelling](https://en.wikipedia.org/wiki/Bitemporal_Modeling) to the event streams. It differentiates two kinds of time:
- {{<term "System time" "system-time">}} - tells us when some event was observed by the system
- {{<term "Event time" "event-time">}} - tells when some event occurred from the perspective of the outside world

Every record in the system has exactly one system time associated with it upon the ingestion but can have zero to many event times.

### System Time
System time gives us a reference point for when something has occurred from the perspective of the system.

{{<term "Projecting" "projection">}} the data onto the system time axis answers the question: *"what did the system know at the time T?"*, meaning that such projections effectively freeze data in time, providing the natural way to achieve **reproducibility**.

For all intents and purposes system time is treated as **ordered monotonically non-decreasing value** that lets us establish a *before-after* relationship between certain events. Note, however, that *before-after* relationship is only meaningful for data within one {{<term "Dataset" "dataset">}} and its upstream dependencies. System time cannot be used to establish an exact *before-after* relationship between the events of the independent datasets.

### Event Time
Event time tells us when something happened from the outside world's perspective. This time, therefore, is usually the most useful one for querying and joining data.

There are no restrictions on the event time in the system - there can be many event times associated with any record, and unlike system time, event times don't have to be monotonic. This allows the system to support many kinds and varieties of event time use, like:
- Post-dated events and predictions - with event time set into the future
- Back-dated events and corrections - with event time set into the past

Depending on the type of transformations these restrictions may be more strict, e.g. joining datasets based on event time may require it to be quasi-monotonic increasing to know when the join operation can be considered complete (see {{<term "Watermarks" "watermark">}}).

See also:
* {{<term "Projections" "projection">}}
* {{<term "Watermarks" "watermark">}}
* [Streaming 101 by Tyler Akidau](https://www.oreilly.com/radar/the-world-beyond-batch-streaming-101/)
* [The Dataflow Model  by Tyler Akidau et al](https://static.googleusercontent.com/media/research.google.com/en//pubs/archive/43864.pdf)

## Watermark
A watermark defines the point in {{<term "Event Time" "event-time">}} for which with a high probability we've already observed all preceding events.

{{<image filename="/images/pages/glossary/watermarks_in_stream.svg" alt="Diagram: Watermarks in the Stream">}}

When performing time-based windowed operation, aggregations, or joins it is important to know when a certain time window can be considered closed. Watermark tells the system "You most likely will not get event with time less than `T` anymore".

In the {{<term "Root Dataset" "root-dataset">}} events can still arrive even after their time interval has been already been closed by the watermark. Such events are considered "late" and it's up to the individual {{<term "Queries" "query">}} to decide how to handle them. They can be simply ignored, emitted into a side output, or still considered by emitting the "correction" event into the output.

Watermarks in the system are defined per every {{<term "Metadata Block" "metadata-chain">}}. By default, the {{<term "Root Dataset" "root-dataset">}} will assign the watermark to the maximum observed {{<term "Event Time" "event-time">}} in the {{<term "Data Slice" "data-slice">}}. You can and should override this behavior if you expect events to arrive out-of-order to some degree, e.g. offsetting the watermark by `1 day` prior to last seen event.

{{<image filename="/images/pages/glossary/watermarks_vs_time.svg" alt="Diagram: Watermarks in Time Domains">}}

Watermarks can also be set based on the {{<term "System Time" "system-time">}} manually or semi-automatically. This is valuable for the slow moving {{<term "Datasets" "dataset">}} where it's normal not to see any events in days or even months. Setting the watermark explicitly allows all computations based on such stream to proceed, knowing that there were no events for that time period, where otherwise the output would be stalled assuming the {{<term "Dataset" "dataset">}} was not updated for a while and old data can still arrive.

## Retractions and Corrections
Errors in source data are inevitable and require a mechanism for correcting them. Unlike databases, where one could issue `DELETE` or `UPDATE` queries, ODF's core data model is an immutable append-only stream, and thus requires a different mechanism.

Retractions and corrections are explicit events that can appear in {{<term "Root" "root-dataset">}} datasets to signify that some previous event was published in error, or to correct some of its fields. They are differentiated from regular events by the special {{<term "Operation Type" "operation-type">}} field.

Retractions and corrections can also naturally occur in {{<term "Derivative" "derivative-dataset">}} datasets in cases when a stream processing operation encounters late data (data arriving past the current {{<term "Watermark" "watermark">}}). In such cases streaming transformation may publish corrections or retractions for previously produced result records that were influenced by the late events.

Retractions and corrections model is fundamental to making data processing **maximally autonomous**.

See also:
- [Common data schema]({{<relref "spec#common-data-schema">}})
- [Representation of retractions and corrections]({{<relref "spec#representation-of-retractions-and-corrections">}})

## Repository
Repositories let participants of the system exchange {{<term "Datasets" "dataset">}} with one another.

Repository definition includes:
- Location where the repository can be reached (URL)
- Protocols that it supports
- Credentials needed to access it
- Any necessary protocol-specific configuration

In the most basic form, a {{<term "Repository" "repository">}} can simply be a location where the dataset files are hosted over one of the [supported]({{<relref "spec#supported-protocols">}}) file or object-based data transfer protocols. The owner of a dataset will have push privileges to this location, while other participants can pull data from it.

An advanced repository can support more functionality like:
- Push data API for publishers
- Subscription API for consumers
- Query API for making use of repository's compute resources and reducing the amount of transferred data

See also:
- [Repository Contract]({{<relref "spec#repository-contract">}})

## Projection
In relational algebra, a [projection](https://en.wikipedia.org/wiki/Projection_(relational_algebra)) is an operation that removes one or many dimensions from a data tuple. In the context of our system the most common projections are *temporal projections* involving the {{<term "System Time" "system-time">}} and {{<term "Event Time" "event-time">}} dimensions.

Depending on the time axis, we arrive at two most important types of projections in [bitemporal data modelling](https://en.wikipedia.org/wiki/Bitemporal_Modeling):
- **AS AT** or *"As we knew at that time"*. This projection collapses the system time dimension and shows us what the state of the data was at that time to the best knowledge of the system.
- **AS OF** or *“As we should've known at the time”*. This projection collapses the event time dimension and shows us what **should've happened** at that time if we knew about all potential corrections and compensating events that were added since then.

Understanding the difference between these projections is essential when working with time series data and for achieving the reproducibility of results.

See also:
- [A Brief History of Time in Data Modelling: OLAP Systems](https://www.kamu.dev/blog/a-brief-history-of-time-in-data-modelling-olap-systems/)

## Manifest
When {{<term "Metadata" "metadata">}} objects are saved on disk or transmitted on the network the typically wrapped in an extra {{<schema "Manifest" "manifest">}} layer.

# Kamu

## Workspace
A workspace in the context of [Kamu CLI]({{<relref "cli">}}) is a directory that contains a hidden `.kamu` sub-directory where `kamu` stores local copies of datasets and configuration, including connection parameters to remote ODF repositories.

## Node
[Kamu Node]({{<relref "node">}}) is a set of [Kubernetes](https://kubernetes.io/) applications that can be installed in a distributed environment to operate data pipelines, verify computations done by other parties, and execute queries on co-located data. It is a horizontally-scalable **back-end implementation** of ODF protocol. Operating a node is the primary way to contribute compute resources to the ODF network.

## Dataset Snapshot
A {{<term "manifest">}} with {{<schema "DatasetSnapshot">}} schema
