---
Title: Artifacts
description:
weight: 20
underConstruction: false
categories: []
aliases:
---

All components of Kamu Node are provided as [OCI container images](https://opencontainers.org/) and [Helm charts](https://helm.sh/).

We are limiting the **official support** to these types of artifacts as the most widespread and interoperable distribution models for Kubernetes applications. Other types of distributions may be supported by the community.


## Helm Charts
Latest Helm charts can be found in the [ArtifactHub](https://artifacthub.io/packages/search?org=kamu):
- [**`kamu-api-server`**](https://artifacthub.io/packages/helm/kamu/kamu-api-server)
- [**`kamu-web-ui`**](https://artifacthub.io/packages/helm/kamu/kamu-web-ui)

You can use ArtifactHub to explore the configuration parameters schema for each chart as well as the default values.


## Helm Repository
To use our charts with Helm you will need to add our repository:
```sh
helm repo add kamu https://kamu-data.github.io/helm-charts
helm repo update
```


## Source Code
Latest source code of all charts can be found in [`kamu-data/helm-charts`](https://github.com/kamu-data/helm-charts) GitHub repository.
