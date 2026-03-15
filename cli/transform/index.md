---
title: Transforming Data
description: Cleaning, enriching, aggregating, and otherwise transforming data in the system. Properties of derivative datasets and stream processing. 
---

import {Term, Schema, YouTube, YouTubeList, Diagram} from '/components/common.jsx'

## Conceptual Model
Open Data Fabric clearly separates two types of data:
- **Source** - represented by <Term t="root datasets" id="root-dataset"/> this data comes directly from external systems, with party that owns the dataset having complete authority over the data and fully accountable for its veracity
- **Derivative** - represented by <Term t="derivative datasets" id="derivative-dataset"/> this data is produced by transforming and combining other datasets (root or derivative).

In simple terms, given two root datasets `A` and `B` the derivative dataset `C` can be though of as a [pure function](https://en.wikipedia.org/wiki/Pure_function):

```
C = f(A, B)
```

Unlike databases, or most data processing libraries you might've used ODF is not "batch", but **stream-oriented**. So `A`, `B` here are both potentially infinite [data streams](/spec#nature-of-data), and function `f()` is a [streaming (temporal) processing](/spec#stream-processing-model) operation that produces another stream as an output.

Stream processing composition works just like normal functional composition:

```
D = h(C) = h(f(A, B))
F = g(D, E) = g(h(f(A, B)), E)
```

This allows us to build **infinitely complex data processing pipelines** and supply chains in the form of a Directed Acyclic Graph (DAG):

<Diagram src="/images/cli/examples/reth-vs-snp500/pipeline.png" alt="Web3 data pipeline"/>

Functions being "pure" means that <Term t="derivative datasets" id="derivative-dataset"/> don't depend on any information outside of ODF - you cannot call arbitrary APIs or download files as part of such processing. 

While this may seem restrictive - this unlocks highly desirable properties like <Term t="reproducibility and verifiability" id="verifiability"/> of all computations and ability to automatically derive <Term t="provenance"/>.

<Info>
Imagine being able to erase all derivative data in the world and [reconstruct it in identical form](/spec#derivative-data-transience) just from source data. Derivative data in ODF sometimes feels like a superpower.
</Info>


## Creating Derivative Datasets
Derivative datasets are created by specifying the <Schema t="SetTransform"/> metadata event.

Example:

```yaml
kind: DatasetSnapshot
version: 1
content:
  name: my.trading.holdings
  kind: Derivative
  metadata:
    - kind: SetTransform
      # Using one dataset as an input
      inputs:
        - datasetRef: my.trading.transactions
      transform:
        # Using Apache Flink SQL engine to perform cumulative sum streaming aggregation
        kind: Sql
        engine: flink
        query: |
          SELECT
            event_time,
            symbol,
            quantity,
            price,
            settlement,
            sum(quantity) over(partition by symbol order by event_time rows unbounded preceding) as cum_quantity,
            sum(settlement) over(partition by symbol order by event_time rows unbounded preceding) as cum_balance
          FROM `my.trading.transactions`
```

This event is as simple as defining two things:
- `inputs` - data from which datasets will be used as input to this pipeline step
- `transform` - the transformation being performed.

Technically ODF supports [any data processing framework](/spec#engine). You will see a lot of Streaming SQL in our examples as we believe it currently offers best user experience when defining streaming transformations.

## Execution Model
When you use [`kamu pull`](/cli-reference#kamu-pull) on a derivative dataset the tool will:
1. Start the appropriate <Term t="query engine" id="engine"/>
2. Restore the state of computation from previous <Term t="checkpoint"/> (if any)
3. Feed the **previously unseen** data from all inputs
4. Write results into a new <Term t="data slice"/>
5. Suspend the computation state into a new <Term t="checkpoint"/>
6. Write a new <Term t="metadata block" id="metadata-chain"/>

Note that query engines **see input data only once**. When performing things like windowed aggregations the intermediate state of computations between the suspends is stored in <Term t="checkpoints" id="checkpoint"/>.

## Supported Operations
Some typical operations you can perform on datasets (in the order of increasing complexity) are:
- **Map** - performing computation on one record at a time
- **Filter** - deciding whether to include a record in the output based on some condition that considers only one record at a time
- **Aggregation** - combining values of multiple records together based on some grouping function (e.g. a time window)
- **Projection** - an aggregation aimed at reducing dimensionality of data
- **Stream-to-Stream Join** - combining several streams of data based on some predicate and a time window
- **Temporal Table Join** - joining a stream to a projection of another stream that represents "current state" of some evolving data based on the timestamp of individual records.

Please see [Examples](/examples) for detailed explanation of each of these classes of operations.

## Consistency
Modern stream processing frameworks should be more appropriately called *"temporal processing frameworks"* as they account for time of records and all kinds of time-related problems during the computations.

Transparently to the user streaming can handle situations like:
- Late arrivals and backfills
- Out-of-order arrivals
- Phase shift and differences in data arrival cadences when joining several streams

Unlike batch that has no notion of time, streaming is a **more complete processing model** that provides you complete **control over the tradeoff between consistency and latency**.

<Info>
Stream processing to batch is like what calculus is to algebra!
</Info>

See [Kamu Blog: The End of Batch Era](https://www.kamu.dev/blog/end-of-batch-era/) to learn more.


## Self-correcting Nature
While we mostly talk about data streams from perspective of observing new events and adding new records - there are many situations when events that were already published may be deemed incorrect and need to be **retracted or corrected**.

We [previously discussed](/merge-strategies#snapshot) retractions and corrections in the context of <Term t="merge strategies" id="merge-strategy"/>, but the most amazing thing about stream processing is that it **can automatically react to retractions and corrections in inputs** to issue appropriate retractions or corrections in the output.

This means that whenever a major issue is detected and fixed in some <Term t="root dataset"/> - these events can **automatically and rapidly propagate** through hundreds of data pipeline stages with no human involvement.

<Tip>
Imagine you publish a research paper based on some medical dataset. Few months passes and the hospital that published the dataset notices and corrects a major inconsistency in data. By linking your paper to a certain range within the source dataset you will be able to get an instant **notification** that your results may be no longer valid. And if your analysis is also stored as an ODF dataset - it can be **instantly updated** accounting for all corrections.
</Tip>

See [Retractions & Corrections](/retractions-corrections) section for a deeper look.
