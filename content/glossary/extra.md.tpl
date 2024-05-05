---
# NOTE: This file is combined by the script with ODF terms into the final glossary
draft: true
---


# Kamu

## Dataset Snapshot
A {{<term "manifest">}} with {{<schema "DatasetSnapshot">}} schema.

## Workspace
A workspace in the context of [Kamu CLI]({{<relref "cli">}}) is a directory that contains a hidden `.kamu` sub-directory where `kamu` stores local copies of datasets and configuration, including connection parameters to remote ODF repositories.

## Node
[Kamu Node]({{<relref "node">}}) is a set of [Kubernetes](https://kubernetes.io/) applications that can be installed in a distributed environment to operate data pipelines, verify computations done by other parties, and execute queries on co-located data. It is a horizontally-scalable **back-end implementation** of ODF protocol. Operating a node is the primary way to contribute compute resources to the ODF network.

## Oracle
[Blockchain Oracles](https://en.wikipedia.org/wiki/Blockchain_oracle) provide information from the outside-world sources to the on-chain [smart contracts](https://en.wikipedia.org/wiki/Smart_contract). The need for oracles arises because in typical blockchain implementations nodes cannot call any external APIs, therefore are limited to operate only on the information that is stored on chain.

Working in combination with ODF smart contracts, [Kamu Node]({{<relref "node">}}) implements an ODF oracle provider component that allows requesting data from the ODF network and supplying it to the smart contracts through a blockchain transaction.

Using ODF network oracle, smart contracts gain the ability to:
- access outside-world data through ODF nodes
- execute very complex and resource-intensive data queries off-chain, for significant cost savings
- get results along with the {{<term "provenance">}} and reproducibility information.

The last property makes ODF oracle really stand compared to the alternatives. Typical oracles act as intermediaries between the calling smart contract and some external API and thus have to employ complex consensus schemes to agree on what the actual result looks like and exclude MITM attacks. The more independent parties vote one the result - the more reliable it will be. But this also balloons the costs, as consensus needs to be established per every request. Therefore, users have to chose between reliability and costs and unfortunately often chose the latter. ODF, by design, is itself reproducible and verifiable - when requesting data from one ODF oracle provider you get full provenance information that can be used to **dispute and verify** the result at any time after it has been given. This allows ODF to function as the first of a kind "optimistic" oracle - one that can supply results very fast and cheaply, while allowing anyone to verify them asynchronously and engage a dispute resolution mechanism if foul play is suspected.
