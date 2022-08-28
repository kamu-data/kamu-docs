---
Title: FAQ
description: Frequently asked questions
weight: 40
categories: []
aliases:
---

## How does kamu compare to Spark / Flink / Kafka Streams (or other enterprise data processing tech)?

`kamu` does not compete with enterprise data processing technologies - it builds on top of them:

- It specifies how data should be stored (e.g. making sure that data is never modified or deleted)
- Provides stable references to data for reproducibility
- Specifies how data & metadata are shared
- Tracks every processing step executed, so that a person on another side of the world who downloaded your dataset could understand exactly where every single piece of data came from
- Allows you to evolve your processing steps over time without breaking other people's pipelines that consume your data
- And much more...

So Spark and Flink to `kamu` is just a building block, while `kamu` is a higher level and opinionated tool.


## Can I create derivative datasets with Pandas (or other data procesing library)?

`kamu`'s goal is to be as inclusive of different ways to process data as possible, but also **uphold certain key properties** of data pipelines like autonomy, low latency, and reproducibility. 

Pandas and most other libraries do **batch processing**, so they are not suited for processing data that flows continuously. Using them would be inefficient, non-reproducible, and error prone, as batch paradigm does not handle late and out-of-order data, and other types of temporal problems we see in data constantly (see our [learning materials]({{<ref "learning-materials">}}) on the topic of streaming vs. batch). 

Also Pandas and similar libraries are imperative and their code is hard to analyze - this complicates our goal of achieving **fine-grain provenance**. So we're currently biased towards processing engines that use Streaming SQL, but will be glad to discuss extending support to other frameworks.
