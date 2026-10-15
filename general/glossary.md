---
# !!! THIS FILE IS AUTO-GENERATED - DO NOT MODIFY MANUALLY !!!
title: "Glossary"
description: "Definitions of commonly used terms in Open Data Fabric and Kamu projects"
icon: arrow-down-a-z
---

import {Diagram, Term, Schema, YouTube, YouTubeList} from '/components/common.jsx'


# Open Data Fabric

## Account
A named identity within a <Term t="Node" id="node"/> that can own <Term t="Resources" id="resource"/> or act as a <Term t="Principal" id="principal"/>. Accounts can be users, organizations, service accounts, or the node itself.

Every resource belongs to an account, making accounts the unit of multi-tenancy - resources of the same type and name can exist under different accounts.

See also:
- [Authorization: Accounts](/odf/spec/auth-and-privacy/authorization#accounts)
- [Resource Framework: Ownership](/odf/spec/automation/resource-framework#ownership)


## Checkpoint
Checkpoints are used by the <Term t="Engines" id="engine"/> to store the computation state between the different invocations of a <Term t="Query" id="query"/>. They are fully engine-specific and opaque to the system. They are however an essential durable part of a <Term t="Dataset" id="dataset"/> as they are necessary to be able to pause and resume the streaming queries, and are essential in implementing "exactly-once" processing semantics.


## Coordinator
Coordinator is an application that implements the common <Term t="Dataset" id="dataset"/> management logic.

Core responsibilities:
- Handles all <Term t="Metadata Chain" id="metadata-chain"/> operations
- Splits the transformation work into batches based on the dataset's evolution timeline
- Collects relevant data slices of the input datasets
- Delegates data processing to the <Term t="Engines" id="engine"/>, making all transformations look to them as conventional stream processing
- Commits the resulting data slices and new metadata blocks

See also:
- [Components: Coordinator](/odf/spec/overview#coordinator)


## Data
Data is a set of <Term t="Events" id="event"/> stored in the system. Since events are immutable data can only grow over time. Conceptually it's best to think of data as a full log of a potentially infinite event stream.

Data never appears in the system alone as we would not be able to tell where it came from and whether it can be trusted. Data always appears as part of a <Term t="Dataset" id="dataset"/>.

<Diagram src="/images/odf/specs/datasets/logical-structure/dataset.svg" alt="Diagram: Dataset/Data"/>

See also:
- [Data Model](/odf/spec/datasets/data-model)
- [Common Data Schema](/odf/spec/datasets/data-model#common-data-schema)


## Data Slice
<Term t="Data" id="data"/> arrives into the system as the arbitrary large sets of events. We refer to them as "slices".

More formally, a slice is a:
- Continuous part of <Term t="Data" id="data"/>
- That has the same <Term t="Schema" id="schema"/>
- Defined by its `[start; end]` <Term t="Offset" id="offset"/> interval

<Diagram src="/images/odf/specs/datasets/logical-structure/metadata.svg" alt="Diagram: Data Slices and Metadata"/>


## Dataset
Dataset is the main unit of data exchange in the system. It's simply a combination of:
- [Identity](/odf/spec/datasets/identity)
- <Term t="Data" id="data"/>
- <Term t="Metadata Chain" id="metadata-chain"/>
- <Term t="Checkpoints" id="checkpoint"/>

Depending on where the data comes from datasets can be of these kinds:
- <Term t="Root" id="root-dataset"/>
- <Term t="Derivative" id="derivative-dataset"/>

<Diagram src="/images/odf/specs/datasets/logical-structure/dataset_graph.svg" alt="Diagram: Dataset Graph"/>

See also:
- [Logical Structure](/odf/spec/datasets/logical-structure)


### Root Dataset
Root datasets are the points of entry of external data into the system. They are usually owned by the organization that has full authority and responsibility over that data, i.e. a trusted source.

Data gets into root datasets via <Term t="Ingestion" id="ingestion"/> from sources that are defined separately from the dataset as `Source` <Term t="Resources" id="resource"/>. A source definition includes:
- Where to fetch the data from - e.g. source URL, a protocol to use, cache control
- How to prepare the binary data - e.g. decompression, file filtering, format conversions
- How to interpret the data - e.g. data format, schema to apply, error handling
- How to combine data ingested in the past with the new data - e.g. append as log or diff as a snapshot of the current state

Source definitions are not part of the <Term t="Metadata Chain" id="metadata-chain"/>, as they don't contribute to provenance or validity of data, and may reveal sensitive information about the infrastructure of a publisher. The metadata chain records the outcome of every ingestion, including the data, its schema, and the state of the source needed to resume ingestion.

See also:
- [Ingestion](/odf/spec/datasets/ingestion)
- [Merge Strategy](/odf/spec/datasets/ingestion#merge-strategies)


### Derivative Dataset
Derivative datasets are created by transforming/combining one or multiple existing datasets.

They are defined by the combination of:
- Input datasets
- A <Term t="Query" id="query"/> to apply to those
- An <Term t="Engine" id="engine"/> used to execute the query

This information is stored in the <Term t="Metadata Chain" id="metadata-chain"/> and can change over time as the dataset evolves.

See also:
- [Processing Model](/odf/spec/transformations/processing-model)
- [Derivative Data Transience](/odf/spec/transformations/processing-model#derivative-data-transience)


## Engine
Engine is an interface shared by all specific implementations of a <Term t="Query" id="query"/> dialect. Engine implementations are responsible for applying defined queries to input data and returning the result. For example, some engines allows you to query data using a series of streaming SQL statements.

Engines run in a sandboxed environments and are not permitted to use any external resources to guarantee the reproducibility of all operations.

<Diagram src="/images/odf/specs/glossary/engine-execution-env.svg" alt="Diagram: Derivative Transformation"/>

As Engines are in the full control of all data transformations, they are also responsible for answering the <Term t="Provenance" id="provenance"/> queries.

See also:
- [Engine Contract](/odf/spec/transformations/engine-contract)


## Entity
A data plane object materialized from a <Term t="Resource" id="resource"/> to fulfill its desired state, e.g. an ODF <Term t="Dataset" id="dataset"/> stored in an S3 bucket, a secret, or an encryption key.

Entities are separate from the resources that describe them. For example, when a dataset is replicated between two nodes, each node has its own `Dataset` resource with a different ID, while both describe the same dataset entity with the same DID.

See also:
- [Resource Framework: Resources and Entities](/odf/spec/automation/resource-framework#resources-and-entities)


## Event
As described in the [Nature of Data](/odf/spec/overview#nature-of-data) section, the system operates only on data expressed as past events, observations, or propositions believed to be true at a certain time. For simplicity, we will use the term "event" throughout to refer to such data tuples.


## Hash
[Cryptographic hash functions](https://en.wikipedia.org/wiki/Cryptographic_hash_function) are used by the system in these three scenarios:
- Computing a logical hash sum of a <Term t="Data Slice" id="data-slice"/>.
- Computing a physical hash sum of a <Term t="Data Slice" id="data-slice"/>.
- Computing a hash sum of a <Term t="MetadataBlock" id="metadata-chain"/>.

Whenever new events are appended to the <Term t="Data" id="data"/> the <Term t="Metadata Chain" id="metadata-chain"/> will also be extended with a block containing a hash sum of the new data slice. The hash sum provides a very quick and reliable way to later validate that the data matches the one that has been written earlier.

The new <Term t="MetadataBlock" id="metadata-chain"/> will also be cryptographically signed to guarantee its integrity - this excludes any malicious or accidental alterations to the block.

Usage examples:
- If the <Term t="Metadata Chain" id="metadata-chain"/> of a certain dataset is reliably known (e.g. available from many independent peers) a peer can then download the <Term t="Data" id="data"/> from any untrusted source and use the hash function to validate the authenticity of every data slice that composes it.
- The trustworthiness of any <Term t="Dataset" id="dataset"/> can be established by reviewing the transformations it claims to be performing on data (contained in the <Term t="Metadata Chain" id="metadata-chain"/>), re-applying those transformations in a trusted environment, and then comparing the hash sums of the result slices.

See also:
- [Data Hashing](/odf/spec/datasets/data-and-checkpoint-hashing#physical-vs-logical-hashes)
- [Checkpoint Hashing](/odf/spec/datasets/data-and-checkpoint-hashing#checkpoint-hashing)
- [Metadata Block Hashing](/odf/spec/datasets/metadata-chain#metadata-block-hashing)


## Ingestion
Ingestion is the process by which external data gets into the system. Typical ingestion steps that describe how data is obtained and read (e.g. fetching data from some URL on the web, decompressing it, and reading it as CSV) are defined by `Source` <Term t="Resources" id="resource"/>, and the ingested data is added to <Term t="Root Datasets" id="root-dataset"/>.

See also:
- [Ingestion](/odf/spec/datasets/ingestion)


## Manifest
A declarative configuration (e.g. a YAML file) that describes the desired state of a <Term t="Resource" id="resource"/>. Applying a manifest to a <Term t="Node" id="node"/> creates or updates the corresponding resource, after which controllers reconcile the actual state of the system with the desired state.

```yaml
$schema: https://opendatafabric.org/schemas/config/v1alpha1/SecretSet
headers:
  name: my-secrets
spec: {}
```

> **Note:** Earlier versions of the spec used the term for the legacy [`Manifest`](https://github.com/open-data-fabric/open-data-fabric/blob/master/schemas/legacy/v0/Manifest.json) wrapper of metadata objects (e.g. `DatasetSnapshot`) that is now deprecated.

See also:
- [Resource Framework: Resource Manifests](/odf/spec/automation/resource-framework#resource-manifests)


## Merge Strategy
By [design](/odf/spec/overview#nature-of-data), the system only stores data in the append-only event log format to preserve the entire history. Unfortunately, a lot of data in the world is not stored or exposed this way. Some organizations may expose their data in the form of periodic database dumps, while some choose to provide it as a log of changes between current and the previous export.

When <Term t="ingesting data" id="ingestion"/> from external sources, the <Term t="Root Datasets" id="root-dataset"/> can choose between different [Merge Strategies](/odf/spec/datasets/ingestion#merge-strategies) that define how to combine the newly-ingested data with the existing one.

For example, when dealing with the daily database dumps, a user can choose the merge strategy that performs [change data capture](https://en.wikipedia.org/wiki/Change_data_capture), transforming dumps into a set of events that signify record creation, update, or deletion.

See also:
- [Merge Strategies](/odf/spec/datasets/ingestion#merge-strategies)


## Metadata
Refers to information about a <Term t="Dataset" id="dataset"/> stored in its <Term t="Metadata Chain" id="metadata-chain"/>.


## Metadata Chain
Metadata Chain is an append-only log of **Metadata Blocks** that captures the entire history of a <Term t="Dataset" id="dataset"/>: its identity, <Term t="Schema" id="schema"/>, what data was added and when, how it was processed (see <Term t="Query" id="query"/>), and other information like licenses and descriptions.

Every block carries one metadata event and refers to the <Term t="hash" id="hash"/> of the previous block, so having a reference to the last block one can traverse the entire chain and discover and verify all components of the dataset.

See also:
- [Metadata Chain](/odf/spec/datasets/metadata-chain)


## Node
An entire ODF deployment acting under a single identity. A node hosts <Term t="Datasets" id="dataset"/> and other <Term t="Resources" id="resource"/> belonging to one or many <Term t="Accounts" id="account"/>, manages them using the <Term t="Coordinator" id="coordinator"/> logic, and exposes them to other participants via <Term t="Repository" id="repository"/> and query protocols.

A node also acts as a <Term t="Principal" id="principal"/> in system tasks and node-to-node communications.

See also:
- [Authorization: Node](/odf/spec/auth-and-privacy/authorization#node)


## Offset
Offset is a monotonically increasing sequential numeric identifier that is assigned to every record and represents its position relative to the beginning of the dataset. Offsets are used to uniquely identify any record in the dataset. Offset of the first record in a dataset is `0`.


## Operation Type
Since past <Term t="Events" id="event"/> are immutable, if some event is deemed incorrect later on it can only be rectified by issuing an explicit <Term t="retraction or correction" id="retractions-and-corrections"/>. Retraction and corrections are also represented as <Term t="Events" id="event"/> in the same stream of <Term t="Data" id="data"/> and differentiated by a special "operation type" field.

See also:
- [Common data schema](/odf/spec/datasets/data-model#common-data-schema)
- [Representation of retractions and corrections](/odf/spec/datasets/data-model#representation-of-retractions-and-corrections)


## Principal
The identity performing an action, established through authentication: a user, a service account, a <Term t="Node" id="node"/>, or an anonymous caller. Principals are the parties whose permissions are checked during authorization, and are recorded as initiators of operations (e.g. the identity a scheduled flow runs as).

See also:
- [Authorization: Principals](/odf/spec/auth-and-privacy/authorization#principals)


## Projection
In relational algebra, a [projection](https://en.wikipedia.org/wiki/Projection_(relational_algebra)) is an operation that removes one or many dimensions from a data tuple. In the context of our system the most common projections are *temporal projections* involving the <Term t="System Time" id="system-time"/> and <Term t="Event Time" id="event-time"/> dimensions.

Depending on the time axis, we arrive at two most important types of projections in [bitemporal data modelling](https://en.wikipedia.org/wiki/Bitemporal_Modeling):
- **AS AT** or *"As we knew at that time"*. This projection collapses the system time dimension and shows us what the state of the data was at that time to the best knowledge of the system.
- **AS OF** or *“As we should've known at the time”*. This projection collapses the event time dimension and shows us what **should've happened** at that time if we knew about all potential corrections and compensating events that were added since then.

Understanding the difference between these projections is essential when working with time series data and for achieving the reproducibility of results.

See also:
- [A Brief History of Time in Data Modelling: OLAP Systems](https://www.kamu.dev/blog/a-brief-history-of-time-in-data-modelling-olap-systems/)


## Provenance
Data provenance describes the origins and the history of data and adds value to data by explaining how it was obtained.

<Term t="Metadata Chain" id="metadata-chain"/> alone can already significantly narrow down the search space when you want to explain how a certain piece of data came to be, as it keeps track of all the inputs and queries used to create a dataset. But the goal of the provenance system is to make this type of inquiry effortless.

We differentiate the following kinds of provenance:
- **Why-provenance** - tells us which input data elements were inspected to decide that an element should be present in the output at all - i.e. defines a sufficient set of elements needed to produce the output.
- **How-provenance** - tells us the process by which the elements of *why-provenance* caused the output to appear
- **Where-provenance** - narrows down *why-provenance* to input data elements that were copied or transformed to determine the output element value.

Since the <Term t="Engines" id="engine"/> are responsible for all data transformations, it's also the Engine's responsibility to answer provenance queries.

There are many different ways to implement provenance:
- By statically analyzing the queries
- By inverting transformations
- By repeating the computations and logging the data used at every step
- By propagating provenance data through all computations

Depending on the language used by an <Term t="Engine" id="engine"/> one approach may work better in one situation than the other, so we avoid prescribing the exact method to use but instead standardize the language used for provenance-related queries and responses.

See also:
- [Provenance in Databases: Why, How, and Where](http://homepages.inf.ed.ac.uk/jcheney/publications/provdbsurvey.pdf)
- [Engine Contract: Derive Provenance](/odf/spec/transformations/engine-contract#derive-provenance)


## Query
Queries define how input data is combined, modified, and re-shaped to produce new data.

Queries are used in two contexts:
- When defining new <Term t="Derivative Datasets" id="derivative-dataset"/>
- When analyzing and extracting data from an existing <Term t="Dataset" id="dataset"/> (locally or from a <Term t="repository" id="repository"/>)

The system is agnostic to the exact language used to define the query and the set of supported dialects can be extended by implementing a new <Term t="Engine" id="engine"/>.

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
- [Stream Processing Model](/odf/spec/overview#stream-processing-model)
- [Derivative Data Transience](/odf/spec/transformations/processing-model#derivative-data-transience)
- [Engine Contract](/odf/spec/transformations/engine-contract)


## Repository
Repositories let participants of the system exchange <Term t="Datasets" id="dataset"/> with one another.

Repository definition includes:
- Location where the repository can be reached (URL)
- Protocols that it supports
- Credentials needed to access it
- Any necessary protocol-specific configuration

In the most basic form, a <Term t="Repository" id="repository"/> can simply be a location where the dataset files are hosted over one of the file or object-based data [transfer protocols](/odf/spec/exchange/transfer-protocols). The owner of a dataset will have push privileges to this location, while other participants can pull data from it.

An advanced repository can support more functionality like:
- Push data API for publishers
- Subscription API for consumers
- Query API for making use of repository's compute resources and reducing the amount of transferred data

See also:
- [Transfer Protocols](/odf/spec/exchange/transfer-protocols)


## Resource
A managed object of a <Term t="Node" id="node"/> that has an identity and whose desired state is described declaratively in a <Term t="Manifest" id="manifest"/>, e.g. `Dataset`, `SecretSet`, `Flow`, or `User`. Resources form the control plane of the system - controllers continuously reconcile the actual state with the desired state, materializing resources into <Term t="Entities" id="entity"/> in the data plane.

A resource manifest consists of:
- `$schema` - URI of the JSON schema that identifies the resource type
- `headers` - identity and ownership information, labels, and annotations
- `spec` - the desired state
- `status` - the current state and progress of reconciliation, maintained by the node

A resource is identified by its type, owning <Term t="Account" id="account"/>, and name, and is assigned a stable ID by the node upon creation.

See also:
- [Resource Framework](/odf/spec/automation/resource-framework)


## Retractions and Corrections
Errors in source data are inevitable and require a mechanism for correcting them. Unlike databases, where one could issue `DELETE` or `UPDATE` queries, ODF's core data model is an immutable append-only stream, and thus requires a different mechanism.

Retractions and corrections are explicit events that can appear in <Term t="Root" id="root-dataset"/> datasets to signify that some previous event was published in error, or to correct some of its fields. They are differentiated from regular events by the special <Term t="Operation Type" id="operation-type"/> field.

Retractions and corrections can also naturally occur in <Term t="Derivative" id="derivative-dataset"/> datasets in cases when a stream processing operation encounters late data (data arriving past the current <Term t="Watermark" id="watermark"/>). In such cases streaming transformation may publish corrections or retractions for previously produced result records that were influenced by the late events.

Retractions and corrections model is fundamental to making data processing **maximally autonomous**.

See also:
- [Common data schema](/odf/spec/datasets/data-model#common-data-schema)
- [Representation of retractions and corrections](/odf/spec/datasets/data-model#representation-of-retractions-and-corrections)


## Schema
Schema describes the shape of the <Term t="data" id="data"/> by associating names and data types to columns that data is composed of. Schema can change over time and its changes are tracked in the <Term t="Metadata Chain" id="metadata-chain"/>.

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
- [Schema Format](/odf/spec/datasets/data-schema#schema-format)
- [Schema Evolution](/odf/spec/datasets/data-model#schema-evolution)


## Time
The system applies the idea of [bitemporal data modelling](https://en.wikipedia.org/wiki/Bitemporal_Modeling) to the event streams. It differentiates two kinds of time:
- <Term t="System time" id="system-time"/> - tells us when some event was observed by the system
- <Term t="Event time" id="event-time"/> - tells when some event occurred from the perspective of the outside world

Every record in the system has exactly one system time associated with it upon the ingestion but can have zero to many event times.


### System Time
System time gives us a reference point for when something has occurred from the perspective of the system.

<Term t="Projecting" id="projection"/> the data onto the system time axis answers the question: *"what did the system know at the time T?"*, meaning that such projections effectively freeze data in time, providing the natural way to achieve **reproducibility**.

For all intents and purposes system time is treated as **ordered monotonically non-decreasing value** that lets us establish a *before-after* relationship between certain events. Note, however, that *before-after* relationship is only meaningful for data within one <Term t="Dataset" id="dataset"/> and its upstream dependencies. System time cannot be used to establish an exact *before-after* relationship between the events of the independent datasets.


### Event Time
Event time tells us when something happened from the outside world's perspective. This time, therefore, is usually the most useful one for querying and joining data.

There are no restrictions on the event time in the system - there can be many event times associated with any record, and unlike system time, event times don't have to be monotonic. This allows the system to support many kinds and varieties of event time use, like:
- Post-dated events and predictions - with event time set into the future
- Back-dated events and corrections - with event time set into the past

Depending on the type of transformations these restrictions may be more strict, e.g. joining datasets based on event time may require it to be quasi-monotonic increasing to know when the join operation can be considered complete (see <Term t="Watermarks" id="watermark"/>).

See also:
* <Term t="Projections" id="projection"/>
* <Term t="Watermarks" id="watermark"/>
* [Streaming 101 by Tyler Akidau](https://www.oreilly.com/radar/the-world-beyond-batch-streaming-101/)
* [The Dataflow Model  by Tyler Akidau et al](https://static.googleusercontent.com/media/research.google.com/en//pubs/archive/43864.pdf)


## Validation
Validation is the process of checking that an object conforms to the rules it must follow - e.g. that a <Term t="Metadata Chain" id="metadata-chain"/> satisfies its consistency rules, that a file matches the <Term t="Hash" id="hash"/> under which it is referenced, or that data follows its <Term t="Schema" id="schema"/>.

Validation answers the question *"is this object intact and well-formed?"*. It is cheap, performed locally, and does not depend on any other data, so it is usually done every time an object is received or read.

Not to be confused with <Term t="Verification" id="verification"/>, which establishes whether a claim about how data was produced is true.

See also:
- [Metadata Chain: Validation](/odf/spec/datasets/metadata-chain#validation)
- [Data & Checkpoint Hashing: Validation and Verification](/odf/spec/datasets/data-and-checkpoint-hashing#validation-and-verification)
- [Transfer Protocols: Validation of Transferred Data](/odf/spec/exchange/transfer-protocols#validation-of-transferred-data)


## Verifiability
In the scope of this specification, verifiability of data means the ability to establish:
- The ultimate source(s) of data:
  - Which <Term t="Root Datasets" id="root-dataset"/> the data is coming from
  - Who these datasets belong to (ownership)
  - And which actor has added the specific records (accountability)
- The transformations performed to create this data:
  - The graph of <Term t="Derivative Datasets" id="derivative-dataset"/> upstream to the one being verified
  - Authorship of those datasets (accountability)
- And finally, that the data in fact corresponds to performing declared transformations on the source data.

In other words, having root datasets `A`, `B` and a derivative dataset `C = f(A, B)`:
- The data in `A` (and similarly in `B`) is verifiable if:
  - <Term t="Metadata Chain" id="metadata-chain"/> of `A` is valid
    - Metadata block hashes are valid, forming a valid chain
    - Blocks point to <Term t="Data Slices" id="data-slice"/> and <Term t="Checkpoints" id="checkpoint"/> with valid hashes
- The data in `C` is verifiable if:
  - <Term t="Metadata Chain" id="metadata-chain"/> of `C` is valid
  - Data in `C` corresponds to applying `f(A, B)` according to all transformation steps declared in the <Term t="Metadata Chain" id="metadata-chain"/>.

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


## Verification
Verification is the process of confirming that a claim about how data came to be is true - e.g. that data of a <Term t="Derivative Dataset" id="derivative-dataset"/> is in fact the result of applying the declared transformations to its inputs, or that a query result corresponds to specific states of the queried datasets.

Verification answers the question *"is this claim true?"*. It can be performed by reproducing the computation or by checking proofs of verifiable computing, may require significant resources and access to other data, and can happen asynchronously and be delegated to other parties. Verification relies on <Term t="Validation" id="validation"/> of all objects involved.

Verification is the means of achieving <Term t="Verifiability" id="verifiability"/>.

See also:
- [Overview: Verification](/odf/spec/overview#verification)
- [Processing Model: Verification](/odf/spec/transformations/processing-model#verification)
- [Verifiable Batch Queries](/odf/spec/exchange/verifiable-batch-queries)


## Watermark
A watermark defines the point in <Term t="Event Time" id="event-time"/> for which with a high probability we've already observed all preceding events.

<Diagram src="/images/odf/specs/glossary/watermarks_in_stream.svg" alt="Diagram: Watermarks in the Stream"/>

When performing time-based windowed operation, aggregations, or joins it is important to know when a certain time window can be considered closed. Watermark tells the system "You most likely will not get event with time less than `T` anymore".

In the <Term t="Root Dataset" id="root-dataset"/> events can still arrive even after their time interval has been already been closed by the watermark. Such events are considered "late" and it's up to the individual <Term t="Queries" id="query"/> to decide how to handle them. They can be simply ignored, emitted into a side output, or still considered by emitting the "correction" event into the output.

Watermarks in the system are defined per every <Term t="Metadata Block" id="metadata-chain"/>. By default, the <Term t="Root Dataset" id="root-dataset"/> will assign the watermark to the maximum observed <Term t="Event Time" id="event-time"/> in the <Term t="Data Slice" id="data-slice"/>. You can and should override this behavior if you expect events to arrive out-of-order to some degree, e.g. offsetting the watermark by `1 day` prior to last seen event.

<Diagram src="/images/odf/specs/glossary/watermarks_vs_time.svg" alt="Diagram: Watermarks in Time Domains"/>

Watermarks can also be set based on the <Term t="System Time" id="system-time"/> manually or semi-automatically. This is valuable for the slow moving <Term t="Datasets" id="dataset"/> where it's normal not to see any events in days or even months. Setting the watermark explicitly allows all computations based on such stream to proceed, knowing that there were no events for that time period, where otherwise the output would be stalled assuming the <Term t="Dataset" id="dataset"/> was not updated for a while and old data can still arrive.

# Kamu

## Dataset Snapshot
A <Term t="manifest"/> with <Schema t="DatasetSnapshot"/> schema.

## Workspace
A workspace in the context of [Kamu CLI](/cli) is a directory that contains a hidden `.kamu` sub-directory where `kamu` stores local copies of datasets and configuration, including connection parameters to remote ODF repositories.

## Kamu Node
[Kamu Node](/node) is a set of [Kubernetes](https://kubernetes.io/) applications that can be installed in a distributed environment to operate data pipelines, verify computations done by other parties, and execute queries on co-located data. It is a horizontally-scalable **back-end implementation** of ODF protocol. Operating a node is the primary way to contribute compute resources to the ODF network.

## Oracle
[Blockchain Oracles](https://en.wikipedia.org/wiki/Blockchain_oracle) provide information from the outside-world sources to the on-chain [smart contracts](https://en.wikipedia.org/wiki/Smart_contract). The need for oracles arises because in typical blockchain implementations nodes cannot call any external APIs, therefore are limited to operate only on the information that is stored on chain.

Working in combination with ODF smart contracts, [Kamu Node](/node) implements an ODF oracle provider component that allows requesting data from the ODF network and supplying it to the smart contracts through a blockchain transaction.

Using ODF network oracle, smart contracts gain the ability to:
- access outside-world data through ODF nodes
- execute very complex and resource-intensive data queries off-chain, for significant cost savings
- get results along with the <Term t="provenance"/> and reproducibility information.

The last property makes ODF oracle really stand compared to the alternatives. Typical oracles act as intermediaries between the calling smart contract and some external API and thus have to employ complex consensus schemes to agree on what the actual result looks like and exclude MITM attacks. The more independent parties vote one the result - the more reliable it will be. But this also balloons the costs, as consensus needs to be established per every request. Therefore, users have to chose between reliability and costs and unfortunately often chose the latter. ODF, by design, is itself reproducible and verifiable - when requesting data from one ODF oracle provider you get full provenance information that can be used to **dispute and verify** the result at any time after it has been given. This allows ODF to function as the first of a kind "optimistic" oracle - one that can supply results very fast and cheaply, while allowing anyone to verify them asynchronously and engage a dispute resolution mechanism if foul play is suspected.
