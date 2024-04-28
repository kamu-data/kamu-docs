---
# NOTE: This file is combined by the script with ODF terms into the final glossary
draft: true
---


# Kamu

## Workspace
A workspace in the context of [Kamu CLI]({{<relref "cli">}}) is a directory that contains a hidden `.kamu` sub-directory where `kamu` stores local copies of datasets and configuration, including connection parameters to remote ODF repositories.

## Node
[Kamu Node]({{<relref "node">}}) is a set of [Kubernetes](https://kubernetes.io/) applications that can be installed in a distributed environment to operate data pipelines, verify computations done by other parties, and execute queries on co-located data. It is a horizontally-scalable **back-end implementation** of ODF protocol. Operating a node is the primary way to contribute compute resources to the ODF network.

## Dataset Snapshot
A {{<term "manifest">}} with {{<schema "DatasetSnapshot">}} schema 