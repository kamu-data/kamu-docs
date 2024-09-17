---
Title: REST API
description:
categories: []
aliases:
---

**🚧 This page is under construction 🚧**

Kamu Node provides powerful REST APIs for querying and ingesting data.

If you are considering to build applications on top of Kamu Node - also consider using [GraphQL API]({{<relref "gql-api">}}).

We are working to provide full **OpenAPI specification** for our REST API - please check back soon!

For accessing individual components of the datasets (blocks, references, data slices) you can use [ODF protocol]({{<relref "odf-protocol">}}).


## Reading Data
To get dataset information like description, schema, etc. use `/metadata` endpoint:
```
https://node.demo.kamu.dev/kamu/com.cryptocompare.ohlcv.eth-usd/metadata?include=attachments,info,license,refs,schema,seed,vocab
```

To get sample data from any dataset use `/tail` endpoint:
```
https://node.demo.kamu.dev/kamu/com.cryptocompare.ohlcv.eth-usd/tail?limit=10
```

To execute arbitrary SQL that can access multiple datasets at once use `/query` endpoint:
```
https://node.demo.kamu.dev/query?query=select+1&skip=0&limit=10&include=input,schema
```

The `/query` endpoint also supports `POST` requests for finer control:

Example request body:
```json
{
    "query": "select event_time, from_symbol, to_symbol, close from \"kamu/com.cryptocompare.ohlcv.eth-usd\"",
    "limit": 3,
    "queryDialect": "SqlDataFusion",
    "dataFormat": "JsonAoa",
    "schemaFormat": "ArrowJson"
}
```

Example response:
```json
{
    "output": {
        "data": [
            ["2024-09-02T21:50:00Z", "eth", "usd", 2537.07],
            ["2024-09-02T21:51:00Z", "eth", "usd", 2541.37],
            ["2024-09-02T21:52:00Z", "eth", "usd", 2542.66]
        ],
        "dataFormat": "JsonAoa",
        "schema": {"fields": ["..."]},
        "schemaFormat": "ArrowJson"
    }
}
```

## Cryptographic Proofs
[Cryptographic proofs]({{<ref "node/commitments">}}) can be also requested to hold the node **forever accountable** for the provided result.

Example request body:
```json
{
    "query": "select event_time, from_symbol, to_symbol, close from \"kamu/com.cryptocompare.ohlcv.eth-usd\"",
    "limit": 3,
    "queryDialect": "SqlDataFusion",
    "dataFormat": "JsonAoA",
    "schemaFormat": "ArrowJson",
    "include": ["proof"]
}
```

Example response:
```json
{
    "input": {
        "query": "select event_time, from_symbol, to_symbol, close from \"kamu/com.cryptocompare.ohlcv.eth-usd\"",
        "queryDialect": "SqlDataFusion",
        "dataFormat": "JsonAoa",
        "include": ["Input", "Proof", "Schema"],
        "schemaFormat": "ArrowJson",
        "datasets": [{
            "id": "did:odf:fed0119d20360650afd3d412c6b11529778b784c697559c0107d37ee5da61465726c4",
            "alias": "kamu/com.cryptocompare.ohlcv.eth-usd",
            "blockHash": "f1620708557a44c88d23c83f2b915abc10a41cc38d2a278e851e5dc6bb02b7e1f9a1a"
        }],
        "skip": 0,
        "limit": 3
    },
    "output": {
        "data": [
            ["2024-09-02T21:50:00Z", "eth", "usd", 2537.07],
            ["2024-09-02T21:51:00Z", "eth", "usd", 2541.37],
            ["2024-09-02T21:52:00Z", "eth", "usd", 2542.66]
        ],
        "dataFormat": "JsonAoa",
        "schema": {"fields": ["..."]},
        "schemaFormat": "ArrowJson"
    },
    "subQueries": [],
    "commitment": {
        "inputHash": "f1620e23f7d8cdde7504eadb86f3cdf34b3b1a7d71f10fe5b54b528dd803387422efc",
        "outputHash": "f1620e91f4d3fa26bc4ca0c49d681c8b630550239b64d3cbcfd7c6c2d6ff45998b088",
        "subQueriesHash": "f1620ca4510738395af1429224dd785675309c344b2b549632e20275c69b15ed1d210"
    },
    "proof": {
        "type": "Ed25519Signature2020",
        "verificationMethod": "did:key:z6MkkhJQPHpA41mTPLFgBeygnjeeADUSwuGDoF9pbGQsfwZp",
        "proofValue": "uJfY3_g03WbmqlQG8TL-WUxKYU8ZoJaP14MzOzbnJedNiu7jpoKnCTNnDI3TYuaXv89vKlirlGs-5AN06mBseCg"
    }
}
```

A client that gets a proof in response should perform [a few basic steps]({{<ref "node/commitments#response-validation">}}) to validate the proof integrity. For example making sure that the DID in `proof.verificationMethod` actually corresponds to the node you're querying data from and that the signature in `proof.proofValue` is actually valid. Only after this you can use this proof to hold the node accountable for the result.

A proof can be stored long-term and then disputed at a later point using your own node or a 3rd party node you can trust via the `/verify` endpoint.

Example request:
```json
{
    "input": {
        "query": "select event_time, from_symbol, to_symbol, close from \"kamu/com.cryptocompare.ohlcv.eth-usd\"",
        "queryDialect": "SqlDataFusion",
        "dataFormat": "JsonAoa",
        "include": ["Input", "Proof", "Schema"],
        "schemaFormat": "ArrowJson",
        "datasets": [{
            "id": "did:odf:fed0119d20360650afd3d412c6b11529778b784c697559c0107d37ee5da61465726c4",
            "alias": "kamu/com.cryptocompare.ohlcv.eth-usd",
            "blockHash": "f1620708557a44c88d23c83f2b915abc10a41cc38d2a278e851e5dc6bb02b7e1f9a1a"
        }],
        "skip": 0,
        "limit": 3
    },
    "subQueries": [],
    "commitment": {
        "inputHash": "f1620e23f7d8cdde7504eadb86f3cdf34b3b1a7d71f10fe5b54b528dd803387422efc",
        "outputHash": "f1620e91f4d3fa26bc4ca0c49d681c8b630550239b64d3cbcfd7c6c2d6ff45998b088",
        "subQueriesHash": "f1620ca4510738395af1429224dd785675309c344b2b549632e20275c69b15ed1d210"
    },
    "proof": {
        "type": "Ed25519Signature2020",
        "verificationMethod": "did:key:z6MkkhJQPHpA41mTPLFgBeygnjeeADUSwuGDoF9pbGQsfwZp",
        "proofValue": "uJfY3_g03WbmqlQG8TL-WUxKYU8ZoJaP14MzOzbnJedNiu7jpoKnCTNnDI3TYuaXv89vKlirlGs-5AN06mBseCg"
    }
}
```

Example response:
```json
{
    "ok": false,
    "error": {
        "kind": "VerificationFailed::OutputMismatch",
        "actual_hash": "f162..c12a",
        "expected_hash": "f162..2a2d",
        "message": "Query was reproduced but resulted in output hash different from expected.
                    This means that the output was either falsified, or the query
                    reproducibility was not guaranteed by the system.",
    }
}
```


See [commitments documentation]() for details.


## Ingesting Data
Example using `curl`:
```sh
echo '[{"foo": "bar"}]' | curl -v -X POST \
    'https://api.demo.kamu.dev/account/my-dataset/ingest' \
    -H 'Authorization: Bearer <access-token>' \
    -H 'Content-Type: application/json'
```

Example using `xh`:
```sh
echo '[{"foo": "bar"}]' | xh -v POST \
    'https://node.demo.kamu.dev/account/my-dataset/ingest' \
    'Authorization: Bearer <access-token>' \
    'Content-Type: application/json'
```

Content types correspond directly to [supported input formats]({{<ref "cli/ingest/input-formats">}}):

| Media Type                       | Example                                                                                                                                                                                                                    |
| -------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `text/csv`                       | <pre>2020-01-01T00:01:00Z,-123.12,49.28</br>2020-01-01T00:02:00Z,-123.13,49.29</pre>                                                                                                                                       |
| `application/json`               | <pre>[{</br>  "event_time": "2020-01-01T00:01:00Z",</br>  "long": -123.12,</br>  "lat": 49.28</br>}, {</br>  "event_time": "2020-01-01T00:02:00Z",</br>  "long": -123.13,</br>  "lat": 49.29</br>}]</pre>                  |
| `application/x-ndjson`           | <pre>{"event_time": "2020-01-01", "long": -123.12, "lat": 49.28}</br>{"event_time": "2020-01-01", "long": -123.13, "lat": 49.29}</pre>                                                                                     |
| `application/geo+json`           | <pre>{</br>  "type": "FeatureCollection",</br>  "features": [</br>    {"type": "Feature", "geometry": {...}, "properties": {...}},</br>    {"type": "Feature", "geometry": {...}, "properties": {...}}</br>  ]</br>}</pre> |
| `application/x-ndgeojson`        | <pre>{"type": "Feature", "geometry": {...}, "properties": {...}}</br>{"type": "Feature", "geometry": {...}, "properties": {...}}</pre>                                                                                     |
| `application/vnd.apache.parquet` | <pre>`<binary data>`</pre>                                                                                                                                                                                                 |
| `application/vnd.esri.shapefile` | <pre>`<binary data>`</pre>                                                                                                                                                                                                 |
