---
Title: Welcome
description: Welcome to Kamu, the creators of Open Data Fabric protocol
weight: -10
topLevelElement: true
categories: []
aliases:
---

Hi, and welcome to Kamu!

Our documentation is organized around 4 closely related projects:

- [**Open Data Fabric**]({{<relref "odf">}}) (ODF) - is an **open protocol specification** for decentralized sharing and verifiable multi-party processing of data. Originally developed by Kamu, the spec is now an independent open-source project separately governed in [this repository](https://github.com/open-data-fabric/open-data-fabric/). It is included on this website purely for convenience of cross-referencing with the rest of documentation.
- [**Kamu CLI**]({{<relref "cli">}}) - is a powerful **command line tool** that implements ODF protocol. You can run it on any device to build data pipelines, ingest and explore data, and interact with other nodes on ODF network.
- [**Kamu Node**]({{<relref "node">}}) - is a scalable **back-end implementation** of ODF. It's a set of [Kubernetes](https://kubernetes.io/) applications that can be installed in a distributed environment to operate data pipelines, verify computations done by other parties, and execute queries on co-located data. Operating a node is a way to contribute compute resources to the network.
- [**Kamu Web Platform**]({{<relref "platform">}}) - this is a **front-end application** that acts as a window into the decentralized ODF network. Think of it as [Etherscan](https://etherscan.io/) for ODF or [GitHub](https://github.com) for data pipelines. It can be used in multiple setups: from exploring your local Kamu CLI workspace, to managing your distributed Kamu Node deployment, and to interacting with remote nodes in the global ODF network.

**If you are new to the project** we recommend you to [start with Kamu CLI tool]({{<relref "cli/get-started">}}) to learn the basics of ODF in the comfort of your laptop.