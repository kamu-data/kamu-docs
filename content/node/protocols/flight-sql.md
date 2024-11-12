---
Title: FlightSQL
description:
categories: []
aliases:
---

[Arrow Flight SQL](https://arrow.apache.org/docs/format/FlightSql.html) is a protocol for interacting with SQL databases using the Arrow in-memory format. 

It is column-oriented, compact, and extremely performant compared to legacy protocols such as [JDBC](https://en.wikipedia.org/wiki/Java_Database_Connectivity) and [ODBC](https://en.wikipedia.org/wiki/Open_Database_Connectivity).

FlightSQL endpoint is typically exposed as:
```
datafusion+flightsql://kamu:kamu@<api-server hostname>:50050?insecure=True
```

Please refer to [Integrations]({{<relref "/cli/integrations">}}) page for some examples of FlightSQL protocol use.
