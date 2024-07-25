---
Title: REST API
description:
categories: []
aliases:
---

**🚧 This page is under construction 🚧**

Kamu Node provides limited data query API for ingesting and extracting data.

If you are considering to build applications on top of Kamu Node - please consider using [GraphQL API]({{<relref "gql-api">}}) instead.



## Reading Data
To get sample data from any dataset use `/tail` endpoint:
```
https://node.demo.kamu.dev/kamu/com.cryptocompare.ohlcv.eth-usd/tail?limit=10
```

To execute arbitrary SQL that can access multiple datasets at once use `/query` endpoint:
```
https://node.demo.kamu.dev/query?query=select+1&skip=0&limit=10
```

The `/query` endpoint also supports `POST` requests for fine control:

Example request body:
```json
{
  "query": "select offset, city, population from populations order by offset desc",
  "dataFormat": "JsonAoA",
  "aliases": [{
    "alias": "populations",
    "id": "did:odf:fed01df230b49615d175307d580c33d6fda61fc7b9aec91df0f5c1a5ebe3b8cbfee02"
  }]
}
```

Example response:
```json
{
    "data": [
        [1, "B", 200], 
        [0, "A", 100]
    ],
    "schema": "...",
    "resultHash": "f9680c001200b3483eecc3d5c6b50ee6b8cba11b51c08f89ea1f53d3a334c743199f5fe656e",
    "state": {
        "inputs": [{
            "id": "did:odf:fed01df230b49615d175307d580c33d6fda61fc7b9aec91df0f5c1a5ebe3b8cbfee02",
            "blockHash": "f16204cec6245fadfbf0663b0e9e9a01c73268cc13e29087b33ce3454af08eb4d3e0b",
        }]
    }
}
```

We are working to provide full **OpenAPI specification** for our REST API - please check back later!

For accessing individual components of the datasets you can use [ODF protocol]({{<relref "odf-protocol">}}).

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
