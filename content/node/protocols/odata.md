---
Title: OData
description:
categories: []
aliases:
---

**🚧 This page is under construction 🚧**

Kamu Node has an experimental support for [OData](https://www.odata.org/) protocol.

The endpoints structured with one OData service root per every account:
```
/odata/{account}/
/odata/{account}/$metadata
```

Every dataset in the account has a corresponding collection endpoint:
```
/odata/{account}/{dataset}
```

Examples:
```
https://node.demo.kamu.dev/odata/kamu/
https://node.demo.kamu.dev/odata/kamu/$metadata
https://node.demo.kamu.dev/odata/kamu/co.alphavantage.tickers.daily.spy
https://node.demo.kamu.dev/odata/kamu/co.alphavantage.tickers.daily.spy?$select=offset,close&$orderby=offset+asc&$top=10
```

Current limitations:
- Only a subset of OData v3.0 spec is supported
- Only supports `atom` format in responses
- Collection resource supports following parameters
  - `$select`
  - `$orderby`
  - `$skip`
  - `$top`
