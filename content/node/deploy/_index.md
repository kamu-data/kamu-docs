---
Title: Deployment Manual
description:
weight: 20
underConstruction: false
categories: []
aliases:
---

## Helm Charts
Latest Helm charts can be found in the [ArtifactHub](https://artifacthub.io/packages/search?org=kamu).


## Recommended Tools
- [`sops`](https://github.com/mozilla/sops) - for editing secrets files
- [`helm`](https://helm.sh/) with the following plugins
  - For secrets management:
    ```
    helm plugin install https://github.com/jkroepke/helm-secrets
    ```
  - For diffing the state:
    ```
    helm plugin install https://github.com/databus23/helm-diff
    ```
- [`helmfile`](https://helmfile.readthedocs.io) - a `helm` whapper for structuring environment configuration
- (optional) [`minikube`](https://minikube.sigs.k8s.io/docs/) - if planning to run a local k8s cluster
- [`kubectl`](https://kubernetes.io/docs/reference/kubectl/) - for interacting with Kubernetes cluster
  - [`kubectl krew`](https://krew.sigs.k8s.io/) - plugin manager
  - [`kubectl minio`](https://min.io/docs/minio/kubernetes/upstream/reference/kubectl-minio-plugin.html) operator plugin (install via `krew`)
- (optional) [`k9s`](https://k9scli.io/) - for fancy TUI of Kubernetes cluster

Before you begin you should configure `kubectl` to be able to access the target k8s cluster.


## Local Deployment with Minikube
WIP: We are working on extracting our deployment examples into a separate repository. Please check back later!