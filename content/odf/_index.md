---
Title: Open Data Fabric
description:
weight: 10
bookCollapseSection: true
topLevelElement: true
topLevelProject: true
alwaysopen: false
categories: []
aliases:
---

<div align="center">

{{ <image filename="/images/odf-logo.png" alt="Open Data Fabric logo" width="50%"> }}

<p><strong>Open protocol for decentralized exchange and transformation of data</strong></p>

[Repository](https://github.com/kamu-data/open-data-fabric) |
[Reference Implementation]({{<ref "cli">}}) |
[Original Whitepaper](https://arxiv.org/abs/2111.06364) |
[Chat](https://discord.gg/nU6TXRQNXC)

[![Spec](https://img.shields.io/github/v/tag/open-data-fabric/open-data-fabric?include_prereleases&logo=gitbook&logoColor=white&label=Spec&style=for-the-badge)](https://github.com/open-data-fabric/open-data-fabric/blob/master/open-data-fabric.md)
[![Metadata Reference](https://img.shields.io/static/v1?label={}&message=Schemas&color=blue&style=for-the-badge)](./open-data-fabric.md#reference-information)
[![Chat](https://shields.io/discord/898726370199359498?style=for-the-badge&logo=discord&label=Discord)](https://discord.gg/nU6TXRQNXC)

</p>
</div>

{{<info>}}
While we are in the process of automating our documentation pipeline please refer to the [GitHub Repository](https://github.com/kamu-data/open-data-fabric) for the latest version of the protocol specification.
{{</info>}}


## Introduction

**Open Data Fabric** is an open protocol specification for decentralized exchange and transformation of semi-structured data, that aims to holistically address many shortcomings of the modern data management systems and workflows.

The goal of this specification is to develop a method of data exchange that would:
- Enable worldwide collaboration around data cleaning, enrichment, and derivation
- Create an environment of verifiable trust between participants without the need for a central authority
- Enable high degree of data reuse, making quality data more readily available
- Improve liquidity of data by speeding up the data propagation times from publishers to consumers
- Create a feedback loop between data consumers and publishers, allowing them to collaborate on better data availability, recency, and design

{{ <image filename="/images/odf/dataset_graph.png" alt="Dataset Graph"> }}

`ODF` protocol is a **Web 3.0 technology** that powers a distributed structured data supply chain for providing timely, high-quality, and verifiable data for data science, smart contracts, web and applications.

<div align="center">
{{ <image filename="/images/odf/distributed_world.png" alt="Web 3.0" width="50%"> }}
</div>

### Introductory materials
- [Original Whitepaper (July 2020)](https://arxiv.org/abs/2111.06364)
- [Kamu Blog: Introducing Open Data Fabric](https://www.kamu.dev/blog/introducing-odf/)
- [Talk: Open Data Fabric for Research Data Management](https://www.youtube.com/watch?v=Ivh-YDDmRf8)
- [PyData Global 2021 Talk: Time: The most misunderstood dimension in data modelling](https://www.youtube.com/watch?v=XxKnTusccUM)
- [Data+AI Summit 2020 Talk: Building a Distributed Collaborative Data Pipeline](https://databricks.com/session_eu20/building-a-distributed-collaborative-data-pipeline-with-apache-spark)

More tutorials and articles can be found in [kamu-cli documentation]({{<ref "learning-materials">}}).

## Current State

The specification is currently in the **EXPERIMENTAL** stage and welcomes feedback.

## Implementations

`Coordinator` implementations:
- [kamu-cli](https://github.com/kamu-data/kamu-cli/) - data management tool that serves as the reference implementation.

`Engine` implementations:
- [kamu-engine-spark](https://github.com/kamu-data/kamu-engine-spark) - engine based on Apache Spark.
- [kamu-engine-flink](https://github.com/kamu-data/kamu-engine-flink) - engine based on Apache Flink.

## History

The specification was originally developed by [Kamu](https://kamu.dev) as part of the [kamu-cli](https://github.com/kamu-data/kamu-cli/) data management tool. While developing it, we quickly realized that the very essence of what we're trying to build - a collaborative open data processing pipeline based on verifiable trust - requires full transparency and openness on our part. We strongly believe in the potential of our ideas to bring data management to the next level, to provide better quality data faster to the people who need it to innovate, fight diseases, build better businesses, and make informed political decisions. Therefore, we saw it as our duty to share these ideas with the community and make the system as inclusive as possible for the existing technologies and future innovations, and work together to build momentum needed to achieve such radical change.

## Contributing

If you like what we're doing - support us by [starring the repo](https://github.com/kamu-data/kamu-cli), this helps us a lot!

For the list of our community resource and guides on how to contribute [start here]({{<ref "community">}}).
