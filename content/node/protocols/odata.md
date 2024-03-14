---
Title: OData
description:
weight: 10
categories: []
aliases:
---

**🚧 This page is under construction 🚧**

Kamu Node has an experimental support for [OData](https://www.odata.org/) protocol.

Endpoints include:
```
/odata/{account}/  - Service root
/odata/{account}/$metadata  - Metadata
/odata/{account}/{dataset}  - Collections
```

Examples:
```
https://node.demo.kamu.dev/odf/kamu/com.cryptocompare.ohlcv.eth-usd?$orderby=offset&$top=5
```

Current limitations:
- Only a subset of OData v3.0 spec is supported
- Only supports `atom` format in responses
- Collection resource supports following parameters
  - `$select`
  - `$orderby`
  - `$skip`
  - `$top`
