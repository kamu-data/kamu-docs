---
Title: OData
description:
categories: []
aliases:
---

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

You can find more endpoint information in [OpenAPI documentation](/node/api/rest/).

See documentation of our [datafusion-odata](https://github.com/kamu-data/datafusion-odata/) library for the list of limitations.
