---
Title: Generic ADBC Client
description: Connecting client applications via ADBC protocol.
weight: 10010
categories: []
aliases:
---

To connect any client that supports [Apache Arrow ADBC protocol](https://arrow.apache.org/adbc/current/index.html) follow these simple steps:
1. Run `kamu` Flight SQL server in a desired workspace:
    ```bash
    kamu sql server --flight-sql --address 127.0.0.1 --port 50050
    ```
2. [Follow the steps](https://arrow.apache.org/adbc/current/index.html) for your specific language and environment to connect your ADBC client to FlightSQL server
3. Use `kamu` as login and password
