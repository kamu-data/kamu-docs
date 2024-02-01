---
Title: Kamu Web Platform
description:
weight: 40
topLevelElement: true
topLevelProject: true
alwaysopen: false
categories: []
aliases:
---

<div align="center">

{{<image filename="/images/kamu-logo-slogan.png" alt="Kamu logo" width="50%">}}

[![Repository](https://img.shields.io/github/v/tag/kamu-data/kamu-web-ui?include_prereleases&logo=github&logoColor=white&label=Repository&style=for-the-badge)](https://github.com/kamu-data/kamu-web-ui/)
[![Release](https://img.shields.io/github/v/release/kamu-data/kamu-web-ui?include_prereleases&logo=rust&logoColor=orange&style=for-the-badge)](https://github.com/kamu-data/kamu-web-ui/releases/latest)
[![CI](https://img.shields.io/github/actions/workflow/status/kamu-data/kamu-web-ui/build.yaml?logo=githubactions&label=CI&logoColor=white&style=for-the-badge&branch=master)](https://github.com/kamu-data/kamu-web-ui/actions)
[![Chat](https://shields.io/discord/898726370199359498?style=for-the-badge&logo=discord&label=Discord)](https://discord.gg/nU6TXRQNXC)


</p>
</div>

## About

Kamu Web Platform is a **front-end application** that acts as a window into the decentralized [Open Data Fabric]({{<relref "odf">}}) (ODF) network.

{{<image filename="/images/platform/kamu-web-ui-screenshot-cloud.png" alt="Kamu Platform screenshots">}}

Think of it as [Etherscan](https://etherscan.io/) for ODF or [GitHub](https://github.com) for data pipelines. It can be used in multiple setups:
- On a laptop to explore and build pipelines together with [Kamu CLI]({{<relref "cli">}})
- Deployed as a private cloud or on-premise data platform in combination with [Kamu Node]({{<relref "node">}})
- As a window into the global ODF network to interact with millions of decentralized data sources and supply chains.

## Get Started
By far the simplest way to try it out is using [Kamu CLI]({{<relref "cli">}}) - simply [install]({{<relref "installation">}}) it and run this command in your {{<term "workspace">}}:

```sh
kamu ui
```

## Helm Chart
You can deploy Kamu Web platform into a [Kubernetes](https://kubernetes.io/) cluster using [Helm](https://helm.sh/) and our latest chart from [ArtifactHub](https://artifacthub.io/packages/search?org=kamu).

See [deployment manual]({{<relref "deploy">}}) on how to deploy the Web Platform alongside [Kamu Node]({{<relref "node">}}).
