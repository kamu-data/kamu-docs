---
title: About
---

<div align="center">

<img src="/images/kamu-logo-slogan.png" alt="Kamu logo" width="50%"/>

<div class="badges">
  <a href="https://github.com/kamu-data/kamu-node/">
    <img
      src="https://img.shields.io/static/v1?logo=github&logoColor=white&label=&message=Repository&color=gray&style=for-the-badge"
      noZoom/>
  </a>
  <a href="https://github.com/kamu-data/kamu-node/releases/latest">
    <img 
      src="https://img.shields.io/github/v/release/kamu-data/kamu-node?include_prereleases&logo=rust&logoColor=orange&style=for-the-badge"
      noZoom/>
  </a>
  <a href="https://github.com/kamu-data/kamu-node/actions">
    <img 
      src="https://img.shields.io/github/actions/workflow/status/kamu-data/kamu-node/build.yaml?logo=githubactions&label=CI&logoColor=white&style=for-the-badge&branch=master"
      noZoom/>
  </a>
  <a href="https://discord.gg/nU6TXRQNXC">
    <img src="https://shields.io/discord/898726370199359498?style=for-the-badge&logo=discord&label=Discord" noZoom/>
  </a>
  <a href="/api/rest">
    <img src="https://img.shields.io/static/v1?logo=openapiinitiative&logoColor=6BFF39&label=&message=REST%20API&color=gray&style=for-the-badge" noZoom/>
  </a>
  <a href="/api/graphql">
    <img src="https://img.shields.io/static/v1?logo=graphql&logoColor=F133A8&label=&message=GraphQL%20API&color=gray&style=for-the-badge" noZoom/>
  </a>
</div>

</div>

## About

Kamu Compute Node is a set of [Kubernetes](https://kubernetes.io/)-native applications that can be deployed in any cloud or on-prem to:

- Operate the stream processing pipelines for a certain set of data flows
- Continuously ingest external data into signed root datasets
- Continuously verify a configured set of pipelines to catch malicious behavior
- Execute queries on co-located data and provide data via variety of protocols
- Provide data to smart contracts via multi-chain ODF Oracle mechanism

Nodes are the building pieces of the [Open Data Fabric](/odf) and the primary way of contributing resources to the network. Unlike blockchain nodes that maintain a single ledger, Kamu nodes can form loosely connected clusters based on vested interests of their operators in certain data pipelines.

If you are new to ODF - we recommend you to start with [Kamu CLI](/cli) for a gradual introduction.

You should consider Kamu Node when you want to:
- Build a horizontally-scalable lakehouse for your data
- Need a decentralized infrastructure for sharing data with your partners or globally without intermediaries
- Want to continuously operate ODF data pipelines or verify data
- Need a rich set of [data APIs](/node/protocols/)
- Want to provide data to [ODF blockchain oracle](/node/protocols/oracle)
