---
Title: Architecture
description:
weight: 10
underConstruction: false
categories: []
aliases:
---

[Kamu Node]({{<relref "node">}}) is a Kubernetes-native set of applications designed to be easily installable on-premise and in private cloud.

This diagram shows a complete deployment of [Kamu Node]({{<relref "node">}}) and [Kamu Web Platform]({{<relref "platform">}}):

{{<image
    filename="/images/node/node-platform-deployment-components.svg" 
    alt="Kamu Node and Platform deployment components">}}

## Dataset Storage
ODF datasets are always safely stored in the storage of your choice, separate from the rest of the system. Multiple [storage systems]({{<relref "node/deploy/storage">}}) are supported.

{{<term "Root" "root-dataset">}} and {{<term "derivative" "derivative-dataset">}} datasets can be stored separately, so that only root datasets were (geo-)replicated to safeguard them from catastrophic loss of data. The property that derivative datasets [can be fully reconstructed]({{<ref "spec#derivative-data-transience">}}) from metadata can enable significant cost savings.

## Operational Storage
This set of storage systems is needed for operating the node and web platform.

**Node data:**
- **Metadata** - used for efficient access to metadata chains of datasets without making too many queries to dataset storage
- **Flows & Tasks** - stores the configuration, execution state, and history of various operations performed by the node (ingesting data, derivative transforms, data queries)
- **Monitoring** - stores traces and metrics for monitoring the health of the deployment

**Web platform data:**
- **Auth** - stores user and organization accounts, permissions, and linked cryptographic keys
- **Governance** - stores issues, discussions, comments, attachments and other information associated with datasets

## Node

### Data Processing Layer
To perform data-intensive operations on datasets the node maintains a **pool of engines** of needed type and version (see also [Supported Engines]({{<relref "supported-engines">}})). Acting as a [Kubernetes controller](https://kubernetes.io/docs/concepts/architecture/controller/) the **Engine Provisioner** decides when to start and stop individual **engine pods** based on demand, configuration, and available capacity in the cluster.

Unlike many streaming data processing engines Kamu Node does not keep pipelines in memory, running all the time. Slow-moving pipelines get suspended into checkpoints and spawned only when needed. This allows Kamu Node to use even very limited resources to switch between many thousands of concurrent pipelines based on defined priorities.

The current demand for data processing is managed by the **Task Scheduler** that understands which datasets need to be updated, prioritizes individual tasks, and hands them over to executors.

Another interesting aspect is that multiple different versions of the same engine type can be used at the same time to ensure reproducibility of derivative data.

### API Layer
These services are the "brain" of the node. They serve API requests as well as decide when to perform various processing and maintenance tasks on datasets and pipelines.

Data-intensive operations like push ingest and SQL queries are handled by the **Data Gateway** component that exposes data under a wide variety of protocols for reading and writing.

All other kinds of requests are handled by the pool of **API Server** components that provide access to all functionality of the node via GraphQL and REST APIs.

Services communicate with one-another via **Event Bus** component.

The **Oracle Provider** is an optional component of the API layer that can supply data to various blockchains. See {{<term "Oracle">}} for explanation of its function. Provider has to be configured with the address(es) of the blockchain nodes to get requests from, the address of the API server to use for executing queries, and the wallet key for executing transactions that carry data into smart contracts.

## Web Platform
[Kamu Web Platform]({{<relref "platform">}}) is a browser application that is served to the browser as a set of static files. The **Web Server** pods are stateless and linearly scalable. Since application files change infrequently, they can be fronted by a CDN to optimize loading times and decrease the traffic to the deployment.

Web platform application running in a browser communicates with **API Server** via GraphQL protocol.

Optionally, other front-end applications like [Jupyter Hub](https://z2jh.jupyter.org/) and [Apache Superset](https://superset.apache.org/) can be deployed to provide data science and business intelligence capabilities on top of Kamu Node. We often include them in our deployment examples to show how to connect them to Kamu.
