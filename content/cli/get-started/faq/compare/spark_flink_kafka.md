---
draft: false
Title: Spark, Flink, Kafka Streaming
description: Kamu vs. Spark, Flink, Kafka Streaming
weight: 10
alwaysopen: false
categories: []
aliases:
---

`kamu` does not compete with enterprise data processing technologies - it uses them internally and builds on top:

- It specifies how data should be stored
  - *e.g. making sure that data is never modified or deleted*
- Provides stable references to data for reproducibility
- Specifies how data & metadata are shared
- Tracks every processing step executed
  - *so that a person on another side of the world who downloaded your dataset could understand exactly where every single piece of data came from*
- Handles dataset evolution
  - *so that you could update your processing steps over time without breaking other people's downstream pipelines that depend on your data*
- And much more...

So Spark and Flink to `kamu` are just building blocks, while `kamu` is a higher level and opinionated system.
