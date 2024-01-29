---
Title: Protocols
description:
weight: 40
underConstruction: false
categories: []
aliases:
---

Kamu Node supports multiple network protocols for managing metadata, bulk uploads/downloads of datasets, and querying data.

## GraphQL
[GraphQL](https://graphql.org/) is our primary API for interacting with the node. [Kamu Web Platform]({{<relref "platform">}}) uses it extensively.

Here you can find the latest [GraphQL API schema](https://github.com/kamu-data/kamu-cli/blob/master/resources/schema.gql).

When you run the `api-server` node component you can open its HTTP interface in the browser and get access to the [GraphQL Playground](https://www.apollographql.com/docs/apollo-server/v2/testing/graphql-playground/).


## HTTP REST
{{<warning>}}
WIP: We are working on generating our REST API docs. Please check back later!
{{</warning>}}


## ODF
The `api-server` fully implements:
- [ODF Simple Transfer Protocol]({{<relref "spec#simple-transfer-protocol">}}) (HTTP / REST)
- [ODF Smart Transfer Protocol]({{<relref "spec#smart-transfer-protocol">}}) (HTTP + Websocket)

These protocols provide the most efficient way to download and upload datasets. Thanks to native support of pre-signed URLs they avoid proxying large chunks of data through the API server and instead can direct uploads and downloads directly to your storage system, ensuring best performance and optimal use of bandwidth.


## Flight SQL
[Arrow Flight SQL](https://arrow.apache.org/docs/format/FlightSql.html) is a protocol for interacting with SQL databases using the Arrow in-memory format. It is column-oriented, compact, and extremely performant compared to legacy protocols such as [JDBC](https://en.wikipedia.org/wiki/Java_Database_Connectivity) and [ODBC](https://en.wikipedia.org/wiki/Open_Database_Connectivity).

See [Integrations With Other Systems]({{<relref "integrations">}}) section for instructions on how to connect external tools to you node via Flight SQL protocol.
