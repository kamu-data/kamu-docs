---
draft: false
Title: How Kamu compares to X
description: Comparisons between Kamu and other projects
weight: 40
alwaysopen: true
categories: []
aliases:
---

# Apache Iceberg, Delta Lake

Apache Iceberg and Delta formats in modern data lakes serve the purpose of creating a logical representation of **data table** that abstracts the physical layout of data on disk.

Their features include:
- **Mutability** (with atomic updates and read consistency)
- Limited "time travel" (between snapshots)
- Automatic snapshot pruning
- Compactions (merging small data files for query efficiency)
- Evolution of schemas and partitions

In `kamu` [ODF datasets]({{<ref "odf">}}) serve a similar purpose as a logical representation of **data stream** (a ledger of events).

The greatest distinction is that these ledgers are **append-only**:
- New data can only be added to the end
- Unlike Iceberg, Delta and other formats created around Change-Data-Capture, ODF streams preserve **complete and unaltered history** of data (for reproducibility and verifiability)
- Old records can only be affected by issuing explicit **corrections or retractions**
- Data and metadata is cryptographically secured and signed

While Iceberg and Delta only work with conventional file systems and object storages (e.g. HDFS, S3), ODF datasets were designed to also work efficiently with **content-addressable storage** like IPFS and Arweave.

The **rich metadata** of ODF streams is designed to carry much more information such as:
- Applied transformation for lineage and provenance of derivative data
- License changes, semantics, governance information...
- Attachments (data manuals, examples) etc.

So while Iceberg and Delta fill the purpose of table abstractions in the enterprise data lakes, ODF dataset is a **Web3-native** dynamic structured data format and a building block for **multi-party exchange and transformation of data**.


# Spark, Flink, Kafka Streaming

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


# Snowflake

| [Snowflake](https://www.snowflake.com/)                                                                                                                                                         | [Kamu](https://kamu.dev)                                                                                                                                                                                                        |
| ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Is a robust data platform and enterprise data warehouse                                                                                                                                         | Is a novel data sharing and collaborative processing solution                                                                                                                                                                   |
| **Centralized**, cloud-only, and based on **proprietary** technology                                                                                                                            | **Decentralized** network with open protocol and code that scales from laptop to cluster, can span from edge to on-prem to multi-cloud                                                                                          |
| Best for **internal** data management                                                                                                                                                           | Best for **cross-organizational** data exchange and collaboration                                                                                                                                                               |
| Works with **cloud storage** (S3, Azure, etc.)                                                                                                                                                  | Works with both **cloud** and **content-addressabe storage** (IPFS, Arweave)                                                                                                                                                    |
| Uses **batch processing** where recurrent data pipelines are expensive to execute, typically run only once a day, and are non-composable due to consistency issues when processing dynamic data | Uses novel **stream processing** that enables near **real-time latencies** and for many workflows can be 1000x **more efficient** than batch, and provides unparalleled **consistency** and **composability** to data pipelines |
| Data is non-verifiable and has no provenance                                                                                                                                                    | Data is 100% reproducible, verifiable, and with built-in provenance                                                                                                                                                             |
| Data can be shared on Snowflake Marketplace but this ties you to Snowflake products                                                                                                             | Data can be shared in a decentralized network **without intermediaries** and using **open protocols**                                                                                                                           |
| On Snowflake Marketplace you can only be a publisher or a consumer of data                                                                                                                      | Enables **infinitely composable** collaboration on data where parties can clean and combine data into higher-level data products while proving that they are not adding malicious data                                          |
| Only off-chain data, limited to **company-size silos**                                                                                                                                          | Seamlessly integrates **on and off-chain data**, and can provide data to blockchain as an **optimistic oracle**                                                                                                                 |


# Ceramic Network
TBD


# Ocean Network
TBD


# Dune Analytics
TBD


# The Graph
TBD


# Chainlink
TBD


# Space And Time
TBD


# JSON APIs
TBD


# Blockchains
TBD
