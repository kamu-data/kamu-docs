---
# !!! THIS FILE IS AUTO-GENERATED - DO NOT MODIFY MANUALLY !!!
title: "Logical Structure"
---

import {Diagram, Term, Schema, YouTube, YouTubeList} from '/components/common.jsx'

**Domain**: Datasets
**Depends on**: -
**RFCs**: -


## Abstract

This document introduces the general structure of an ODF <Term t="Dataset" id="dataset"/> - the main unit of data exchange in the system. It explains the components a dataset consists of, the two kinds of datasets, and how datasets evolve over time, serving as an entry point into the specs of the Datasets domain.


## Dataset Structure
ODF operates on data expressed as immutable events (see [Nature of Data](/odf/spec/overview#nature-of-data)). A <Term t="Dataset" id="dataset"/> is a combination of:
- **Identity** - a globally unique identifier tied to a cryptographic key pair, and human-friendly aliases (see [Identity](/odf/spec/datasets/identity))
- **Data** - a potentially infinite stream of events, stored as a sequence of data slices (see [Data Model](/odf/spec/datasets/data-model))
- **Metadata Chain** - an append-only log of blocks that captures the entire history of the dataset (see [Metadata Chain](/odf/spec/datasets/metadata-chain))
- **Checkpoints** - engine-specific state used to resume stream processing (see [Processing Model](/odf/spec/transformations/processing-model#checkpoints))

<Diagram src="/images/odf/specs/datasets/logical-structure/dataset.svg" alt="Diagram: Dataset/Data"/>

All components of a dataset except the block references are immutable and content-addressed, so having only a hash of the last metadata block one can discover and verify all of them (see [Storage Layout](/odf/spec/datasets/storage-layout)).


### Data and Data Slices
<Term t="Data" id="data"/> is a set of <Term t="Events" id="event"/>. Since events are immutable, data can only grow over time. Conceptually it's best to think of data as a full log of a potentially infinite event stream.

Data never appears in the system alone, as we would not be able to tell where it came from and whether it can be trusted - it always appears as part of a dataset.

Data arrives into the system in arbitrarily large sets of events called <Term t="Data Slices" id="data-slice"/>. Every slice is a continuous part of data with the same <Term t="Schema" id="schema"/>, defined by its interval of <Term t="Offsets" id="offset"/>, and is stored as a separate data part file.

<Diagram src="/images/odf/specs/datasets/logical-structure/metadata.svg" alt="Diagram: Data Slices and Metadata"/>

All records carry the system columns of the common data schema, including the offset, the <Term t="Operation Type" id="operation-type"/>, the <Term t="System Time" id="system-time"/>, and the <Term t="Event Time" id="event-time"/> (see [Data Model](/odf/spec/datasets/data-model)). The logical structure of data is described using the ODF schema format (see [Data Schema](/odf/spec/datasets/data-schema)).


### Metadata
Metadata plays an essential role in ODF (see [Essential Role of Metadata](/odf/spec/overview#essential-role-of-metadata)) - it contains every aspect of where the data came from, how it was transformed, and everything that ever influenced how data looks like throughout its entire lifetime.

Every data slice and checkpoint added to the dataset is recorded in a block of the [Metadata Chain](/odf/spec/datasets/metadata-chain) together with its [hash](/odf/spec/datasets/data-and-checkpoint-hashing), linking data and metadata cryptographically.


### Root and Derivative Datasets
Depending on where the data comes from, datasets can be of two kinds:
- <Term t="Root Datasets" id="root-dataset"/> - the points of entry of external data into the system, populated via [Ingestion](/odf/spec/datasets/ingestion)
- <Term t="Derivative Datasets" id="derivative-dataset"/> - created by transforming and combining one or multiple existing datasets using deterministic queries (see [Processing Model](/odf/spec/transformations/processing-model))

Datasets connected through transformations form a graph, where data of every derivative dataset can be traced back to the root datasets it was derived from.

<Diagram src="/images/odf/specs/datasets/logical-structure/dataset_graph.svg" alt="Diagram: Dataset Graph"/>


## Evolution of Data
As the nature of businesses change, as new requirements arrive, as defects are detected and fixed - it's not a matter of *if* but *when* the time comes to make changes to the data. Calling data a potentially infinite stream would not make much sense without providing a way to improve and evolve it over time. Having to create a new dataset every time you need to change the schema or update the transformation would jeopardize the timeliness requirement, as the entire chain of transformations would have to be rebuilt from scratch after every such change.

Our design goals are, therefore:
- To seamlessly support all backward-compatible data schema changes
- To support the evolution of transformations over time
- To provide a way to correct past mistakes in data

While for simplicity we previously considered derivative datasets to be only defined by one transformation query, in fact it can comprise multiple queries that were active during different periods of time. The metadata keeps track of which parts of inputs were processed by which query and which parts of output were produced as the result, ensuring reproducibility. This is captured by the [Metadata Chain](/odf/spec/datasets/metadata-chain) - **almost anything that defines a dataset can change over time**.


## Datasets Specs

| Spec | Description |
| --- | --- |
| [Identity](/odf/spec/datasets/identity) | `did:odf` identifiers, aliases, and references |
| [Data Model](/odf/spec/datasets/data-model) | Event model, system columns, retractions and corrections, schema evolution |
| [Data Schema](/odf/spec/datasets/data-schema) | Logical schema format of data |
| [Metadata Chain](/odf/spec/datasets/metadata-chain) | Blocks, events, consistency rules, and block hashing |
| [Data & Checkpoint Hashing](/odf/spec/datasets/data-and-checkpoint-hashing) | Physical and logical hashing of data and checkpoints |
| [Storage Layout](/odf/spec/datasets/storage-layout) | Layout of dataset components in file systems, object stores, and content-addressable storage |
| [Ingestion](/odf/spec/datasets/ingestion) | Sources, ingestion phases, and merge strategies of root datasets |
