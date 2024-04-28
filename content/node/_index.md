---
Title: Kamu Node
description:
weight: 30
bookCollapseSection: true
topLevelElement: true
topLevelProject: true
alwaysopen: false
categories: []
aliases:
---

<div align="center">

{{ <image filename="/images/kamu-logo-slogan.png" alt="Kamu logo" width="50%"> }}

[![Repository](https://img.shields.io/github/v/tag/kamu-data/kamu-node?include_prereleases&logo=github&logoColor=white&label=Repository&style=for-the-badge)](https://github.com/kamu-data/kamu-node/)
[![Release](https://img.shields.io/github/v/release/kamu-data/kamu-node?include_prereleases&logo=rust&logoColor=orange&style=for-the-badge)](https://github.com/kamu-data/kamu-node/releases/latest)
[![CI](https://img.shields.io/github/actions/workflow/status/kamu-data/kamu-node/build.yaml?logo=githubactions&label=CI&logoColor=white&style=for-the-badge&branch=master)](https://github.com/kamu-data/kamu-node/actions)
[![Chat](https://shields.io/discord/898726370199359498?style=for-the-badge&logo=discord&label=Discord)](https://discord.gg/nU6TXRQNXC)


</p>
</div>

## About

Kamu Compute Node is a set of [Kubernetes](https://kubernetes.io/)-native applications that can be deployed in any cloud or on-prem to:

- Operate the stream processing pipelines for a certain set of data flows
- Continuously verify datasets that you are interested it to catch malicious behavior
- Execute queries on co-located data

Nodes are the building pieces of the [Open Data Fabric](https://docs.kamu.dev/odf/) and the primary way of contributing resources to the network. Unlike blockchain nodes that maintain a single ledger, Kamu nodes can form loosely connected clusters based on vested interests of their operators in certain data pipelines.

If you are new to ODF - we recommend you to start with [Kamu CLI](https://github.com/kamu-data/kamu-cli/) instead for a gradual introduction. You should consider Kamu Node when you want to:
- Build a horizontally-scalable data lake for your data
- Need a decentralized infrastructure for sharing data with your partners or globally without intermediaries
- Want to continuously operate ODF data pipelines or verify data
