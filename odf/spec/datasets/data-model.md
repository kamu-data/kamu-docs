---
# !!! THIS FILE IS AUTO-GENERATED - DO NOT MODIFY MANUALLY !!!
title: "Data Model"
---

import {Diagram, Term, Schema, YouTube, YouTubeList} from '/components/common.jsx'

**Domain**: Datasets
**Depends on**: [Data Schema](/odf/spec/datasets/data-schema)
**RFCs**: [RFC-001](/odf/rfcs/001-record-offsets), [RFC-015](/odf/rfcs/015-unified-changelog-stream-schema)


## Abstract

This spec defines how data of a dataset is represented in memory and at rest, the system columns that all data in ODF carries to support the bitemporal event model, the changelog representation of retractions and corrections, and the rules according to which a dataset's schema is allowed to evolve over time.


## In-memory and On-disk Formats
We differentiate two data formats by their purpose:
- **In-memory format** - used when passing data around between the subsystems (e.g. when <Term t="Coordinator" id="coordinator"/> communicates with the <Term t="Engine" id="engine"/>).
- **On-disk format** - used for data at rest and by query engines when querying data from the entire dataset.

For our **in-memory format** we chose [Apache Arrow](https://arrow.apache.org/), as it is:
- Purposefully designed for minimal overhead interoperability between data processing systems
- Minimizes copying of data
- Hardware efficient
- Supports streaming

For our **on-disk format** we choose [Apache Parquet](https://parquet.apache.org/), as it is:
- Fast to decode into [Apache Arrow](https://arrow.apache.org/)
- Space and IO efficient thanks to the built-in compression
- Efficient for querying thanks to the columnar structure and built-in basic indexing

Data on disk is stored in the multiple "part" files. Once a part file is written it is immutable for the entire lifetime of the dataset.


## Common Data Schema
All data in the system is guaranteed to have the following columns:

|    Column     | Description                                                                                                                                                                                                                                                                                                                                       |
| :-----------: | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
|   `offset`    | <Term t="Offset" id="offset"/> is a sequential identifier of a row relative to the start of the dataset (first row has an offset of `0`)                                                                                                                                                                                                                       |
|     `op`      | <Term t="Operation Type" id="operation-type"/> is used to differentiate regular append events from retractions and corrections                                                                                                                                                                                                                                 |
| `system_time` | <Term t="System Time" id="system-time"/> denotes when an event first appeared in the dataset. This will be an ingestion time for events in the <Term t="Root Dataset" id="root-dataset"/> or transformation time in the <Term t="Derivative Dataset" id="derivative-dataset"/>                                                                                                           |
| `event_time`  | <Term t="Event Time" id="event-time"/> denotes when to our best knowledge an event has occurred in the real world. By default all temporal computations (windowing, aggregations, joins) are done in the event time space thus giving the user query an appearance of a regular flow of events even when data is backfilled or frequently arrives out-of-order |

Representation:

|    Column     |      Arrow Type      |                            Parquet Type                             | Recommended Parquet Encoding |
| :-----------: | :------------------: | :-----------------------------------------------------------------: | :--------------------------: |
|   `offset`    |       `uint64`       |                               `INT64`                               |    `DELTA_BINARY_PACKED`     |
|     `op`      |       `uint8`        |                               `INT32`                               |       `RLE_DICTIONARY`       |
| `system_time` | `timestamp(ms, UTC)` |           `INT64, TIMESTAMP(MILLIS, AdjustedToUTC=true)`            |      `PLAIN_DICTIONARY`      |
| `event_time`  | `timestamp(ms, UTC)` | `INT64, TIMESTAMP(MILLIS, AdjustedToUTC=true)`<br/>or `int32, DATE` |                              |


> **TODO:**
> - We are not allowing non-UTC-adjusted timestamps yet as Parquet does not offer a way to encode the timezone, meaning we need a reliable way to pass timezone information between different engines through some other means (e.g. Parquet metadata). Having naive/local timestamps without enforcing that they are accompanied by the specific timezone would be too error-prone.


## Representation of Retractions and Corrections
<Term t="Retractions and corrections" id="retractions-and-corrections"/> are differentiated from regular <Term t="Events" id="event"/> in the <Term t="Data Slice" id="data-slice"/> via special `op` column, carrying an <Term t="Operation Type" id="operation-type"/>.

Valid operation types are:

| Value | Operation name | Operation short code |
| :---: | :------------: | :------------------: |
|   0   |    `append`    |         `+A`         |
|   1   |   `retract`    |         `-R`         |
|   2   | `correct-from` |         `-C`         |
|   3   |  `correct-to`  |         `+C`         |

The `retract` and `correct-from` events must carry the same exact data fields (all fields excluding `offset`, `op`, and `system_time`) as the event that is being retracted.

The `correct-to` event carries the new values for the event being corrected. This event must immediately follow the `correct-from` event. This model allows data engines that operate on changelog / diff events that simultaneously carry both old and new values for event during a correction to reconstruct such events easily by sequentially reading the <Term t="Data Slice" id="data-slice"/>.

A pair of `correct-from` and `correct-to` events must belong to the same <Term t="Data Slice" id="data-slice"/> - they cannot span across slices.

The order of records in a dataset, as defined by their <Term t="Offsets" id="offset"/>, is significant: a retraction or correction always follows the event it applies to, and correction pairs must stay adjacent. Records therefore must not be reordered (e.g. sorted by <Term t="Event Time" id="event-time"/>) when they are processed or written, as that may produce an invalid stream.

Not every stream needs to use all operation types. The following are all valid subsets of this model:
- **Append-only stream** - contains only `append` events
- **Retract stream** - contains only `append` and `retract` events, where a change of a previously published event is represented as its retraction followed by an append of the new value
- **Changelog stream** - uses all operation types, differentiating retractions from corrections

See also:
- [RFC-015: Unified Changelog Stream Schema](/odf/rfcs/015-unified-changelog-stream-schema)


## Schema Evolution
<Term t="Dataset" id="dataset"/> <Term t="Schema" id="schema"/> may change when:
- A different <Term t="Ingestion" id="ingestion"/> process is specified in the <Term t="Root Dataset" id="root-dataset"/>
- A transformation <Term t="Query" id="query"/> of the <Term t="Derivative Dataset" id="derivative-dataset"/> is changed
- A <Term t="Schema" id="schema"/> of one of the inputs of the <Term t="Query" id="query"/> changes

In general, <Term t="Schema" id="schema"/> changes are restricted to only adding new columns. Removing and renaming columns or changing data types would break downstream data consumers and therefore not allowed. A migration procedure should be used instead when it's desired to introduce breaking changes in the <Term t="Schema" id="schema"/>.
