---
Title: Verifiable Queries
description:
weight: 40
categories: []
aliases:
---

## Motivation
When you query data in `kamu`, we create an unbreakable **cryptographic commitment** that allows you to hold every party in the data supply chain accountable for veracity of the result.

This accountability should persist long after the response is provided, so that participants can process data fast in “optimistic” fashion, and can **verify and dispute the results later**.

This mechanism is foundational to **automatic dispute resolution** mechanism of the ODF network that can financially penalize malicious activity.

## Commitment Properties
- **Hiding** - Commitment should not reveal any information about the operation.
- **Binding** - It should be impossible to change any inputs or outputs of the operation without invalidating the commitment.
- **Succinct** - Commitment itself should be small enough to cheaply store on-chain. The process of disputing the operation results should not require storing and transferring the actual data.
- **Deterministic** - Same query should result in the same commitment as long as the query itself is deterministic.
- **Reproducible** - Given all the same inputs of the operation a third party should be able to repeat the query, arrive at the same results, and be able to successfully validate them against the original commitment.
- **Non-repudiable** - A prover cannot dispute performing the operation. There exists a mechanism that ties its identity to the provided commitment. This mechanism may be separate from the commitment itself to keep the latter pure zero-knowledge
- **Composable** - It should be possible to split computation into several steps and compose their commitments into one final commitment. When joining two datasets from different owners the entire execution may be split into sub-plans that are executed by different nodes belonging to different parties. In the event of a dispute, it should be possible to assign responsibility to the specific party and not just stop at the party that performed the final result aggregation.
- **Multi-protocol** - Ideally the commitment structure can be reused without significant alterations across multiple protocols like REST, Blockchain Oracle, FlightSQL, Kafka egress, WebSockets etc.

## Structured Recursive Commitments
Let's explore how the commitment scheme works using a [REST batch query API]({{<relref "rest-api">}}):

```python
POST /query
Host: node.demo.kamu.dev

{
  "query": "select * from foo",
  "queryDialect": "SqlDataFusion",
  "dataFormat": "JsonAoS",
  "schemaFormat": "ArrowJson",
  "include": ["input", "schema", "proof"]
}
```

```python
200 OK

{
  # Input section that can be used to fully reproduce the result of operation
  "input": {
    "query": "select * from foo",
    "queryDialect": "SqlDataFusion",
    "dataFormat": "JsonAoS",
    "schemaFormat": "ArrowJson",
    "datasets": [{
      "id": "did:odf:fed0..ee02",
      "alias": "foo",
      "blockHash": "f162..3e0b",
    }]
  },

  # The result
  "output": {
    "data": [
      {"foo": 1, "bar": "A"},
      {"foo": 2, "bar": "B"}
    ],
    "dataFormat": "JsonAoS",
    "schema": {...},
    "schemaFormat": "ArrowJson",
  },

  # Information about processing performed by other nodes as part of this operation
  # that are identical in structure to the top-level response (recursive)
  "subQueries": [{
    "input": {...},
    "subQueries": [...],
    "commitment": {...},
    "proof": {...},
  }]

  # Succinct commitment
  "commitment": {
    # Input hash: multihash(canonicalize(input))
    "inputHash": "f162..3e0b",

    # Output hash: multihash(canonicalize(output))
    "outputHash": "f162..baaf",

    # Sub-queries hash: multihash(canonicalize(subQueries))
    "subQueriesHash": "f162..8dae",
  }

  # Signature block
  "proof": {
    "type": "Ed25519Signature2020",

    # DID (public key) of the node performing the computation
    "verificationMethod": "did:key:fed0..3e41",

    # Signature: multibase(sign(canonicalize(commitment)))
    "proofValue": "u3MvG...ouQk"
  }
}
```

**Note:** Technically the commitment block is redundant and the caller could compute all hashes themselves. In fact they have to do so to validate the response (see below). We include this block purely to:
- Protect clients from implementing hashing in a way that is not consistent with the specification
- Provide more information during the validation and dispute stages to isolate inconsistencies to specific parts.

### JSON Hashing
This scheme involves hashing JSON objects. To exclude variations like whitespace characters and property order differences between JSON library implementations we need to convert it into canonical form as specified in [RFC 8785: JSON Canonicalization Scheme](https://datatracker.ietf.org/doc/html/rfc8785).

### Response Validation
Immediately upon receiving the response the caller must validate it to ensure that the commitment is not bogus and is disputable:
1. Verify that `proof.verificationMethod` DID belongs to the node you are requesting data from
2. Verify `commitment.outputHash` by re-computing the hash
3. Verify `commitment.inputHash` by re-computing the hash
4. Verify `commitment.subQueriesHash` by re-computing the hash
5. Verify the signature in proof.proofValue usings
   1. Message: `canonicalize(commitment)`
   2. Public key: `key_from_did(proof.verificationMethod)`
6. Repeat the steps 3-5 recursively for every entry in subQueries

### Storing Commitments
To be able to dispute the result in future, consumer should store the following fields:
- `input`
- `subQueries`
- `commitment`
- `proof`

These different parts can be also used separately for different purposes as they all provide different “layers” of verifiability:
- `input` - provides reproducibility
- `commitment` - seals the response against tampering
- `proof` - adds non-repudiation via signature
- `subQueries` - provide the above for multi-party computations

### Dispute Resolution
The procedure of resolving a dispute using a commitment via reproducibility is as follows:
1. Consumer submits a claim to the verifier by providing:
    - input
    - commitment
    - subQueries
    - proof
2. Verifier obtains the relevant input.datasets
3. Verifier validates the claim according to the same rules as described in Response Validation
   - If any check fails the claim is rejected as invalid
4. Verifier checks that all authority specified in subQueries are registered nodes
    - In an unregistered node is found the claim is accepted and the blame is assigned to the root authority for using a bogus node for computing part of the response
5. Verifier generates the logical query plan and checks that the plan is identical or equivalent to the plan composed from the subQueries
    - If plan does not correspond to the original query the claim is accepted and the blame is assigned to the root authority for providing a malicious query plan
6. In a bottom-up fashion Verifier repeats all the computation steps using input and compares hashes of outputs to those captured in commitment.outputHash
   - If a hash doesn’t match the claim is accepted and the blame is assigned to the corresponding authority for providing a malicious output data

Properties:
- **Hiding** - YES*
    - The hashes in the commitment block can be used as zero-knowledge commitments that do not reveal any information
    - The public part of the proof reveals only the identity of the node that performed the computation
- **Biding** - YES
- **Deterministic** - YES
    - Assuming canonical response format
- **Reproducible** - YES
    - The `input` field contains all the necessary info to reproduce the request
- **Non-repudiable** - YES
    - Through the identity and signature in the `proof`
- **Composable** - YES
    - Proof is recursive via `subQueries` field
- **Multi-protocol** - YES
    - A similar scheme can be implemented in other protocols.


## Commitments in ODF Oracle
For the explanation of oracle commitments see [ODF Oracle protocol documentation]({{<relref "oracle">}}).


## Zero-Knowledge Proofs
Currently ZKs are very limited in terms of data types and functions they can support. Supporting JOINs is especially problematic. We are working on introducing ZK proofs progressively, where possible for simpler queries, as an alternative to verification through signing and reproducibility.


## Alternatives
### HTTP Message Signatures
[RFC 9421: HTTP Message Signatures](https://datatracker.ietf.org/doc/rfc9421/) proposes a standard for signing HTTP requests and responses.
Under this scheme a query operation could look like this:

```python
POST /query
Host: node.demo.kamu.dev
Accept-Signature: sig=(@status, ...)

{
  "query": "select * from foo",
  "queryFormat": "SqlDataFusion",
  "aliases": [{"alias": "foo", "id": "did:odf:fed0..ee02"}],
  "dataFormat": "JsonAoS"
}
```

```python
200 OK
Signature-Input: (@status, ...)
Signature: sig=:...:

{
  "input": {
    "query": "select * from foo",
    "queryDialect": "SqlDataFusion",
    "datasets": [{"id": "did:odf:fed0..ee02", "alias": "foo", "blockHash": "f162..3e0b"}],
  },
  "output": {
    "dataFormat": "JsonAoS",
    "data": [
      {"foo": 1, "bar": "A"},
      {"foo": 2, "bar": "B"}
    ],
  }
}
```

In this case the commitment would consist of the entire HTTP response (excluding only some headers that are not part of the Signature-Input).
- **Hiding** - YES / NO
  - Depending on the algorithm, signature may reveal the public key of the signer and therefore the identity of a node that provided the response.
- **Biding** - YES
- **Succinct** - **NO**
  - The signature itself is small and constant in size, however to dispute the operation a client will have to hold on to the entire response data to show the validity of a signature before verifier attempts to reproduce the request - this would be impractical at scale
  - RFC specifies `Content-Digest` header that may be included into the signature instead of the entire payload, thus allowing not to store data, but this is insufficient due to other issues
- **Deterministic** - YES
  - Assuming stable / canonical response format
- **Reproducible** - YES
  - Note that the response would include the query and all other input parameters, so removing the output fields like data and schema gives us all the necessary inputs to reproduce the request
- **Non-repudiable** - YES
  - Through the signature
- **Composable** - **NO**
  - Including commitments from other nodes that performed parts of the request will require some different mechanism where HTTP signatures are included as parts of the JSON response
Nodes may not even use HTTP when communicating with one another and use FlightSQL instead.
- **Multi-protocol** - **NO**
  - This scheme is HTTP specific - other protocols will have to use other methods.
