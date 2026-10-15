---
# !!! THIS FILE IS AUTO-GENERATED - DO NOT MODIFY MANUALLY !!!
title: "Identity"
---

import {Diagram, Term, Schema, YouTube, YouTubeList} from '/components/common.jsx'

**Domain**: Datasets
**Depends on**: [Metadata Chain](/odf/spec/datasets/metadata-chain)
**RFCs**: [RFC-003](/odf/rfcs/003-content-addressability), [RFC-007](/odf/rfcs/007-simple-transfer-protocol), [RFC-012](/odf/rfcs/012-recommend-base16-encoding)


## Abstract

This spec defines how <Term t="Datasets" id="dataset"/> are identified. It defines the `did:odf` [DID](https://www.w3.org/TR/did-core/) method used to create globally unique dataset identifiers that are tied to a cryptographic key pair and require no central authority, and the human-friendly aliases and references used to refer to datasets within and across <Term t="Repositories" id="repository"/>.


## Overview
The identity of a dataset consists of:
- [Unique identifiers](#unique-identifiers) - used to unambiguously identify datasets on the network, e.g. when referencing one dataset as an input of another.
- [Aliases and references](#aliases-and-references) - used for human-friendly naming.


## Unique Identifiers
ODF is designed to be compatible with [content-addressable storage](https://en.wikipedia.org/wiki/Content-addressable_storage). When stored in such storage, all parts of a <Term t="Dataset" id="dataset"/> can be accessed by having only a hash of the last <Term t="MetadataBlock" id="metadata-chain"/>.

As <Term t="Dataset" id="dataset"/> grows, however, a reference to a single <Term t="MetadataBlock" id="metadata-chain"/> will only provide access to a subset of its history. To refer to a <Term t="Dataset" id="dataset"/> as a whole a different identifier is needed that can be resolved into a hash of the latest block. Such identifiers must be globally unique, issuable with no central authority, and tied to a proof of ownership over a dataset.

ODF follows the [W3C DID Identity Scheme](https://w3c.github.io/did-core/) using a custom `did:odf` method. This method is based closely on [`did:key` method](https://w3c-ccg.github.io/did-method-key/) that derives the unique identity from a public key of a cryptographic key pair.

Example:

<pre>
did:odf:fed012126262ba49e1ba8392c26f7a39e1ba8d756c7469786d3365200c68402ff65dc
</pre>

The identifier is formed by:
- Generating a cryptographic key pair (e.g. using `ed25519` algorithm)
- Taking the public key part
- Prepending an appropriate [multicodec](https://github.com/multiformats/multicodec) value to identify the algorithm (e.g. `ed25519-pub`)
- Encoding data with [multibase](https://github.com/multiformats/multibase) encoding using `base16` scheme

Or in pseudocode:

<pre>
did-odf-format := 'did:odf:' + MULTIBASE(
  base16,
  MULTICODEC(
    public_key_type,
    public_key_bytes,
  )
)
</pre>

The resulting DID is stored in the first <Term t="MetadataBlock" id="metadata-chain"/> in the chain of every <Term t="Dataset" id="dataset"/>, called <Schema t="Seed" id="seed"/> (see [Metadata Chain](/odf/spec/datasets/metadata-chain#core-events)).

Tying the identity of a dataset to a cryptographic key pair provides a way to create unique identity in a fully decentralized way. The corresponding private key can be used to prove ownership and control over a <Term t="Dataset" id="dataset"/> and to delegate access.

> Note that the only difference between `did:odf` and `did:key` method is the encoding scheme. ODF uses `base16` instead of `base58btc` for reasons explained in the [Hash Representation](/odf/spec/datasets/metadata-chain#hash-representation) section. Because conversion between the two encodings is trivial, ODF is compatible with authorization frameworks that work with `did:key` method. We expect that in future the `did:key` spec will be extended to allow `base16` encoding too, further minimizing the difference.


## Aliases and References
Formats described below provide human-friendly ways to refer to a certain dataset. Note that they are only meaningful within the boundaries of a <Term t="Repository" id="repository"/>. Unlike [Dataset IDs](#unique-identifiers) they are not collision-free and mutable.

Depending on the context we differentiate the following types of references:
- **Local Format** - used to refer to a dataset within a local workspace (can be single- and multi-tenant)
- **Remote Format** - used to refer to a dataset located in a known <Term t="Repository" id="repository"/> provider.

As you will see in the examples below, we recommend (but not require) using the [reverse domain name notation](https://en.wikipedia.org/wiki/Reverse_domain_name_notation) for <Term t="Dataset" id="dataset"/> names.

Examples:
<pre>
// Dataset ID
did:odf:fed012126262ba49e1ba8392c26f7a39e1ba8d756c7469786d3365200c68402ff65dc

// Local Format - DatasetName is highlighted
<b>property.parcel-polygons</b>
<b>cities</b>
<b>admin0.countries.10m</b>

// Local Multi-tenant Format - AccountName is highlighted
<b>statcan.gc.ca</b>/census.2016.population
<b>ny-newyork</b>/public-safety.ems-incident-dispatch

// Remote Format - RepoName is highlighted
<b>statcan.gc.ca</b>/census.2016.population
<b>us.cityofnewyork</b>/public-safety.ems-incident-dispatch
<b>data.gov</b>/ny-newyork/public-safety.ems-incident-dispatch

// Remote Url Format
https://opendata.ca/odf/census-2016-population/
ipfs://bafkreie3hfshd4ikinnbio3kewo2hvj6doh5jp3p23iwk2evgo2un5g7km/
</pre>

Note that name components such as `DatasetName`, `AccountName`, `RepoName` are case-insensitive, i.e. names `ny-newyork` and `NY-NewYork` are considered identical during lookups and uniqueness checks within the repository.


### Grammar
Full [PEG](https://en.wikipedia.org/wiki/Parsing_expression_grammar) grammar:
```peg
DatasetRefAny = 
  DatasetRefRemote /
  DatasetRef

DatasetRef = 
  DatasetId /
  DatasetAlias

DatasetRefRemote =
  (RepoName "/")? DatasetId /
  DatasetAliasRemote /
  Url

DatasetAlias = 
  (AccountName "/")? DatasetName

DatasetAliasRemote = 
  RepoName "/" (AccountName "/")? DatasetName

DatasetId = "did:odf:" Multibase
DatasetName = Hostname
AccountName = Hostname
RepoName = Hostname

Hostname = Subdomain ("." Subdomain)*
Subdomain = [a-zA-Z0-9]+ ("-" [a-zA-Z0-9]+)*

Multibase = [a-zA-Z0-9+/=]+
Url = Scheme "://" [^\n]+
Scheme = [a-zA-Z0-9]+ ("+" [a-zA-Z0-9]+)*
```

Remote references in the URL format point directly to the location of a dataset (e.g. a directory served over HTTP or stored in IPFS), where the scheme selects the transfer protocol (see [Transfer Protocols](/odf/spec/exchange/transfer-protocols)).


## References in Metadata
Datasets can refer to other datasets in their <Term t="Metadata Chain" id="metadata-chain"/>, e.g. a <Term t="Derivative Dataset" id="derivative-dataset"/> specifies its inputs in the `SetTransform` event (<Schema t="TransformInput" id="transforminput"/>). Such references:
- Can be specified using any form of local or remote reference when the dataset is defined
- Must be resolved into a dataset ID by the time the block is accepted into the chain, to guarantee reproducibility, as aliases can change over time
- Carry a separate `alias` under which the input is available in queries, decoupling queries from the names of input datasets


## Identity of Dataset Resources
The `Dataset` <Term t="resource" id="resource"/> that describes the desired state of a dataset on a <Term t="Node" id="node"/> has its own identity that is separate from the identity of the dataset itself (see [Resource Framework: Resources and Entities](/odf/spec/automation/resource-framework#resources-and-entities)):
- The resource `id` identifies the resource within one node, while the `did` identifies the dataset on the global network. When a dataset is replicated between nodes, every node has its own `Dataset` resource with a different `id` but the same `did`.
- In resource manifests, datasets are referred to using [resource references](/odf/spec/automation/resource-framework#references) (e.g. `Dataset:acme/sensor-temp`), which can also identify the dataset by its `did`.
