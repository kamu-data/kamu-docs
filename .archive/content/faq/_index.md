---
Title: FAQ
description: Frequently asked questions
topLevelElement: true
weight: 100
alwaysopen: false
categories: []
aliases:
  - /cli/get-started/faq/
---

## How Kamu is different from X?

We have [entire section]({{<ref "compare">}}) dedicated to direct comparisons.


## Can I create derivative datasets with Pandas or other data processing library?

`kamu`'s goal is to be as inclusive of different ways to process data as possible, but also **uphold certain key properties** of data pipelines like autonomy, low latency, and reproducibility. 

Pandas and most other libraries do **batch processing**, so they are not suited for processing data that flows continuously. Using them would be inefficient, non-reproducible, and error prone, as batch paradigm does not handle late and out-of-order data, and other types of temporal problems we see in data constantly (see our [learning materials]({{<ref "learning-materials">}}) on the topic of streaming vs. batch). 

Also Pandas and similar libraries are imperative and their code is hard to analyze - this complicates our goal of achieving **fine-grain provenance**. So we're currently biased towards processing engines that use Streaming SQL, but will be glad to discuss extending support to other frameworks.
