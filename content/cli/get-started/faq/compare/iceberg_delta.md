---
draft: false
Title: Apache Iceberg & Delta Lake
description: Kamu vs. Apache Iceberg & Delta Lake
weight: 10
alwaysopen: false
categories: []
aliases:
---

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
