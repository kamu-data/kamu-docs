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

The [ODF format]({{<ref "odf">}}) plays a similar role to Iceber/Delta in traditional lakehouse systems, but instead of representing a table, it representats a **historical ledger of events** - a combination of data and metadata that in detail describe the evolution of a dataset over time. Below we list some of its most notable aspects.

ODF ledgers are mostly **append-only**:
- Unlike Iceberg/Delta and similar formats created around Change-Data-Capture, ODF streams are intended to preserve **complete and unaltered history** of data for reproducibility, verifiability, and ultimate "time-travel" capabilities
- New data is added to the end, while previous records can be revised by issuing explicit [retractions and corrections]({{<ref "retractions-corrections">}})
- The format still offers non-destructive compaction for the sake of performance
- The historical data can be pruned, but such actions are also communicated in the format explicitly.

ODF format puts emphasis on [Event Sourcing](https://martinfowler.com/eaaDev/EventSourcing.html) - storing descriptive domain events instead of the "current state". CDC tables still can be expressed using ODF ledger as a changelog stream.

While Iceberg/Delta only work with conventional file systems and object storages (e.g. HDFS, S3), ODF datasets were designed to also work efficiently with **decentralized content-addressable storages** like IPFS and Arweave.

The **rich metadata** of ODF streams is designed to carry a lot more information, such as:
- Applied transformations, for **lineage and provenance** of derivative data
- License changes, semantics, governance information...
- Attachments (data readmes, charts, examples etc.)

ODF datasets also include several **cryptographic features**:
- Embedded global identity, allowing attribution
- Metadata ledger is cryptographically secured and signed, for tamper-proofness and accountability
- In the near future ODF will also support granular encryption, allowing to control access and permissions via key exchange. This will allow private data to be stored in open networks (e.g. IPFS, Filecoin) that do not offer any central point of control to enforce permissions.

So while Iceberg and Delta fill the purpose of table abstractions in enterprise data lakehouses, ODF dataset is a **Web3-native** ledgerized data format that we see as a building block for **multi-party exchange and collaborative processing of data**.


# Spark, Flink, Kafka Streaming
`kamu` does not replace or compete with enterprise data processing engines - it uses them as building blocks.

Think of `kamu` as *"Kubernetes for Data"*, where [multiple different engines]({{<ref "supported-engines">}}) are just plug-in components, integrated together into a single **verifiable data processing framework**.

While individual engines let you do almost anything with data, `kamu` is a lot more **opinionated**:
- It tries to enforce many data management best practices like avoiding history loss
- Provides stable references to data for reproducibility
- Specifies how data & metadata are shared/replicated over the network
- Tracks every processing step executed and records provenance
  - *so that a person on another side of the world who downloaded your dataset could understand exactly where every single piece of data came from*
- Handles dataset evolution
  - *so that you could update your processing steps over time without breaking other people's downstream pipelines that depend on your data*
- And much more...


# Snowflake
| Snowflake                                                                                                                                                                                       | Kamu                                                                                                                                                                                                                            |
| ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Is a robust data platform and enterprise data warehouse                                                                                                                                         | Is a Web3-native data sharing and collaborative processing solution                                                                                                                                                             |
| **Centralized**, cloud-only, and based on **proprietary** technology                                                                                                                            | **Decentralized** network with open protocol and code that scales from laptop to cluster, can span from edge to on-prem to multi-cloud                                                                                          |
| Best for **internal** data management                                                                                                                                                           | Best for **cross-organizational** data exchange and collaboration                                                                                                                                                               |
| Works with **cloud storage** (S3, Azure, etc.)                                                                                                                                                  | Works with both **cloud** and **content-addressabe storage** (IPFS, Arweave)                                                                                                                                                    |
| Uses **batch processing** where recurrent data pipelines are expensive to execute, typically run only once a day, and are non-composable due to consistency issues when processing dynamic data | Uses novel **stream processing** that enables near **real-time latencies** and for many workflows can be 1000x **more efficient** than batch, and provides unparalleled **consistency** and **composability** to data pipelines |
| Data is non-verifiable and has no provenance                                                                                                                                                    | Data is 100% reproducible, {{<term "verifiable" "verifiability">}}, and with built-in {{<term "provenance">}}                                                                                                                   |
| Data can be shared on Snowflake Marketplace but this ties you to Snowflake products                                                                                                             | Data can be shared in a decentralized network **without intermediaries** and using **open protocols**                                                                                                                           |
| On Snowflake Marketplace you can only be a publisher or a consumer of data                                                                                                                      | Enables **infinitely composable** collaboration on data where parties can clean and combine data into higher-level data products while proving that they are not adding malicious data                                          |
| Only off-chain data, limited to **company-size silos**                                                                                                                                          | Seamlessly integrates **on and off-chain data**, and can provide data to blockchain as an **optimistic oracle**                                                                                                                 |


# Databricks
Databricks provide an amazing set of technologies for enterprise data, however, many of the limitations described in the [Snowflake](#snowflake) section in regards to centralization still apply.

Unlike Databricks platform, `kamu` is:
- **Local-first** - a person can start using `kamu` with nothing but their laptop, without any accounts or any cloud infrastructure, while having access to the same features a platform provides
- **Streaming-frist** - we believe that modern stream processing is a [superior computational model](https://www.kamu.dev/blog/end-of-batch-era/) for automation and far less fragile than batch
- Based on **cryptographic ledgers and verifiable processing** - we build from ground up to ensure reproducibility, auditability, and accurate provenance of data
- **Decentralized** - we respect data ownership and sovereignty and want to enable the smallest organizations and individuals to store data on any inftastructure of their choice. Instead of creating monolyths we focus on enabling millions of small data publishers and processors work together efficiently in a global data economy
- **Collaborative** - built-in verifiability and auditability allows allows data exchange and processing to function across company boundaries, and provides a reliable foundation for multi-party data exchange and processing.


# Apache Airflow, Apache NiFi
These tools are "swiss army knives" of data processing. Their ultimate flexibility unfortunately also makes them easily misused, often resulting in [Rube Goldberg machines](https://en.wikipedia.org/wiki/Rube_Goldberg_machine) that are extremely convoluted and fragile.

Our goal with `kamu` is to provide a more opinionated data management framework that:
- Makes following best practices effortless
- Provides configurable tradeoffs between consistency and latency
- Can automatically react to (not-so-)special events like backfills, retractions, corrections
- Captures provenance thoughout the entire pipeline
- Can function across company boundaries
- And much more!

You can use these tools to prepare data for ingestion into `kamu`, but after that you should seriously consider the superior [stream processing computational model](https://www.kamu.dev/blog/end-of-batch-era/) for further proccessing.


# JSON REST APIs
| JSON REST                                                                                                                                                                                  | Kamu                                                                                 |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------ |
| No standard - diffrent auth mechanisms, data models, limits, pagination, error handling                                                                                                    | Simple and [open protocol]({{<ref "odf">}})                                          |
| JSON can have very significant overhead for large amounts of data                                                                                                                          | Uses Apache Arrow for the most efficient and compact encoding of structured data     |
| API has to be designed with specific use case in mind - this largely favors applications that have predictable access patterns rather than analytics that requires slicing and dicing data | Both application and analytics-friendly                                              |
| Lack of flexibility in queries often monivates users to immediately dump all data                                                                                                          | Avoids adverse incentive by providing convinient access                              |
| Have to be integrated on one-by-one basis - very time consuming and error prone                                                                                                            | Data is decentralized but can be accessed uniformly                                  |
| Need software developers to integrate and maintain - expensive                                                                                                                             | Data can be accessed easily by anyone, without software development skills           |
| Not reproducible or verifiabiable - impossible to prove that data came from a source                                                                                                       | 100% reproducible, verifiable, and allows holding data providers accountable         |
| Not composable - after data is altered you'd need to build a new API infrastructure to share it                                                                                            | Infinitely composable - improved/enriched data can be shared with the network easily |


# Blockchains
Although [ODF data format]({{<ref "odf">}}) is inspired by cryptographic ledgers used in blockchains, `kamu` is NOT a mesh connectivity network, it does NOT maintain a single ledger or run any kind of consensus between nodes.

Nodes in `kamu` talk to each other only to execute a query that touches data spread across them, or to run a streaming data processing task.

Network topology in `kamu` therefore corresponds directly to the data pipeline being executed. Data is replicated only between the nodes that explicitly want to replicate it, and processing tasks are dispatched to nodes that explicitly say they can perform them.

We designed `kamu` to work well with blockchains:
- Blockchain smart contracts can act as a OLTP (transactional) distributed services, delegating data storage and heavy computation tasks to `kamu`
- Smart contracts can request data from `kamu` via [ODF oracle]({{<ref "oracle">}})
- `kamu` can in turn [use data from blockchains]({{<ref "blockchain-source">}}) for processing and analytics.


# Ceramic Network
| Ceramic                                                                                                                                                                                                                                                                | Kamu                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Purpose: transactional data store for decentralized apps                                                                                                                                                                                                               | Purpose: historical data lakehouse, analytical querying, composable stream processing                                                                                                                                                                                                                                                                                                                                                                                              |
| Stores data using IPLD protocol and IPFS network                                                                                                                                                                                                                       | **Storage-agnostic**: supports cloud, on-prem, and decentralized storages. Decuopling the query engine from storage infrastructure has long been considered the best practice in data analytics that prevents vendor lock-in of data.                                                                                                                                                                                                                                              |
| Data model based on event streams as cryptographic ledgers. Uses **record-oriented** encoding of payloads (e.g. DAG-CBOR).                                                                                                                                             | Data model also based on event streams as cryptographic ledgers. Data is stored in **industry-standard analytical formats** (Parquet). Using **column-oriented** format allows maximally efficient storage of data, suitable for high-volume and high-frequency IoT use cases. Logical structure of the stream is inspired by **leading lakehouse formats** (Apache Iceberg, Delta) and is developed as an [open specification]({{<ref "odf">}}) by a consortium of companies.     |
| Custom data query API based on GrapghQL                                                                                                                                                                                                                                | SQL API for data access is backed by a wide range of world's **leading data processing engines** (e.g. Spark, Flink, Datafusion)                                                                                                                                                                                                                                                                                                                                                   |
| Custom storage and APIs require users to fully commit to the solution and re-architect their workflows around it                                                                                                                                                       | Multiple storage types and support for standard data protocols (e.g. JDBC, ODBC) provides a very gradual migration path that respects user's choices of infrastructure and is **compatible with all modern BI and data science tools** (Jupyter, Tableau, PowerBI, Google Collab etc.).                                                                                                                                                                                            |
| No built-in data transformation capabilities. Derivative data can only be created by extracting data from the system, transforming it, and writing it into a new stream. Transformed data therefore will be disjoint from its origin. The model is **non-composable**. | Data transformation is a core part of the system. Processing pipelines can be built using streaming SQL allowing to create higher-level datasets that clean, aggregate, enrich, and integrate data. Provenance of derivative data is preserved. Pipelines are **infinitely composable**. Using **verifiable processing** the validity of all data can be verified, allowing to build data pipelines that span arcoss multiple organizations in a global **trustless** environment. |


# Space And Time
| Space And Time                                                                                                                                                                                                                                                                                                                                                                                                                                                                        | Kamu                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Centralized data warehouse using Zero-Knowledge proofs                                                                                                                                                                                                                                                                                                                                                                                                                                | Decentralized data lakehouse, a Kubernetes-like framework for data management, and a multi-party collaborative data processing network                                                                                                                                                                                                                                                                                                            |
| Closed-source                                                                                                                                                                                                                                                                                                                                                                                                                                                                         | Open source and based on open formats and protocols                                                                                                                                                                                                                                                                                                                                                                                               |
| Cloud-only (Azure)                                                                                                                                                                                                                                                                                                                                                                                                                                                                    | Can be deployed anywhere from a laptop to on-premise and public/private clouds                                                                                                                                                                                                                                                                                                                                                                    |
| Batch query model only                                                                                                                                                                                                                                                                                                                                                                                                                                                                | Supports **batch** querying for analytics and **stream processing** for building low-latency, autonomous, and highly composable data processing pipelines.                                                                                                                                                                                                                                                                                        |
| Verifiable computing using **Zero-Knowledge proofs** allows computations to be performed on private data with a guarantee of correctness without revealing the data. At the time of writing ZK SQL implementation was limited to a few basic data types and operations and did not support `JOIN`s, making applicability very limited. Generating ZK proofs is a highly computationally-expensive task requiring specialized hardware with powerful GPUs limiting deployment options. | Verifiable computing via **reproducibility**. This is a simple and established model. Verifier needs to have access to source data to verify the computations, but privacy can be preserved by running computations in [TEEs](https://en.wikipedia.org/wiki/Trusted_execution_environment). Full range of batch and streaming SQL is supported including complex streaming `JOIN`s that are essential for integrating data from multiple sources. |
| Based on Apache Datafusion engine with custom extensions for ZK-proof generation                                                                                                                                                                                                                                                                                                                                                                                                      | Integrates a [wide range]({{<ref "supported-engines">}}) of major data processing engines                                                                                                                                                                                                                                                                                                                                                         |
| No built-in data transformation capabilities. Derivative data can only be created by extracting data from the system, transforming it, and writing it into a new table. Transformed data therefore will be disjoint from its origin. The model is **non-composable**.                                                                                                                                                                                                                 | Data transformation is a core part of the system. Processing pipelines can be built using streaming SQL allowing to create higher-level datasets that clean, aggregate, enrich, and integrate data. Provenance of derivative data is preserved. Pipelines are **infinitely composable**.                                                                                                                                                          |