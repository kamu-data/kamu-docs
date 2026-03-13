---
Title: ODF
description:
categories: []
aliases:
---

**🚧 This page is under construction 🚧**

Kamu Node implements both Simple and Smart Transfer Protocols according to the [ODF Specification]({{<relref "spec">}}).

[Simple Transfer Protocol]({{<relref "spec#simple-transfer-protocol">}}) (HTTP / REST) can be used for data access via HTTP in constrained environments.

[Smart Transfer Protocol]({{<relref "spec#smart-transfer-protocol">}}) (HTTP + Websocket) provides the most efficient way to download and upload datasets. Thanks to native support of pre-signed URLs they avoid proxying large chunks of data through the API server and instead can direct uploads and downloads directly to your storage system. Built-in metadata compression also ensures best performance and optimal use of bandwidth for datasets with very large histories.

You can see individual endpoints of ODF protocol in our [REST API documentation](/node/api/rest).
