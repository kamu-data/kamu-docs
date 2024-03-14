---
Title: REST API
description:
weight: 20
categories: []
aliases:
---

**🚧 This page is under construction 🚧**

Kamu Node provides limited data query API for ingesting and extracting data.

If you are considering to build applications on top of Kamu Node - please consider using [GraphQL API]({{<relref "gql-api">}}) instead.

Reading data:
```
https://node.demo.kamu.dev/query?query=select+1&skip=0&limit=10
https://node.demo.kamu.dev/kamu/com.cryptocompare.ohlcv.eth-usd/tail?limit=10
```

Ingesting data:
```sh
echo '{"foo": "bar"}' | xh POST 'https://node.demo.kamu.dev/kamu/com.cryptocompare.ohlcv.eth-usd/ingest' "Content-Type: application/json"
```

For accessing individual components of the datasets you can use [ODF protocol]({{<relref "odf-protocol">}}).