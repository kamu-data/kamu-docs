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
ODF datasets are always safely stored in the storage of your choice, separated from the rest of the system. Multiple [storage systems]({{<relref "node/deploy/storage">}}) are supported.

{{<term "Root" "root-dataset">}} and {{<term "derivative" "derivative-dataset">}} can be stored separately, so that only root datasets were (geo-)replicated to safeguard them from catastrophic loss of data. The property that derivative datasets [can be fully reconstructed]({{<ref "spec#derivative-data-transience">}}) from metadata can enable significant cost savings.

## Operational Storage
This set of storage systems is needed for operating the node and web platform.

#### Node data
- **Metadata** (PostgreSQL) - used for efficient access to metadata chains of datasets without making too many queries to dataset storage
- **Flows & Tasks** (PostgreSQL) - stores the configuration, execution state, and history of various operations performed by the node (ingesting data, derivative transforms, data queries)
- **Monitoring** - stores traces and metrics for monitoring the health of the deployment

#### Web platform data
- **Auth** (PostgreSQL) - stores user and organization accounts, permissions, and linked cryptographic keys
- **Governance** (PostgreSQL) - stores issues, discussions, comments, attachments and other information associated with datasets

## Data Processing
To perform data-intensive operations on datasets the node maintains a **pool of engines** of needed type and version (see also [Supported Engines]({{<relref "supported-engines">}})). Acting as a [Kubernetes controller](https://kubernetes.io/docs/concepts/architecture/controller/) the **Engine Provisioner** decides when to start and stop individual **engine pods** based on demand, configuration, and available capacity in the cluster.

The current demand for data processing is managed by the **Task Scheduler** that prioritizes individual tasks and hands them over to executors.

## Back-End Services
These services are the "brain" of the node. They serve API requests as well as decide when to perform various processing and maintenance tasks on datasets and pipelines.

Data-intensive operations like push ingest and SQL queries are handled by the **Data Gateway** component that exposes data under a wide variety of protocols for reading and writing.

All other kinds of requests are handled by the pool of **API Server** components that provide access to all functionality of the node via GraphQL and REST APIs.

Services communicate with one-another via **Event Bus** component.

## Front-End Services
[Kamu Web Platform]({{<relref "platform">}}) is a browser application that is served to the browser as a set of static files. The **Web Server** pods are stateless and linearly scalable. Since application files change infrequently, they can be fronted by a CDN to optimize loading times and decrease the traffic to the deployment.

Web platform application running in a browser communicates with **API Server** via GraphQL protocol.

Optionally, other front-end applications like [Jupyter Hub](https://z2jh.jupyter.org/) and [Apache Superset](https://superset.apache.org/) can be deployed to provide data science and business intelligence capabilities on top of Kamu Node. We often include them in our deployment examples to show how to connect them to Kamu.
