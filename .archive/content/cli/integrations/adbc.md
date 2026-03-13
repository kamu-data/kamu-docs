---
Title: Generic ADBC Client
description: Connecting client applications via ADBC protocol.
categories: []
aliases:
---

To connect any client that supports [Apache Arrow ADBC protocol](https://arrow.apache.org/adbc/current/index.html) follow these simple steps:
1. Run `kamu` Flight SQL server in a desired workspace:
    ```bash
    kamu sql server --address 127.0.0.1 --port 50050
    ```
2. [Follow the steps](https://arrow.apache.org/adbc/current/index.html) for your specific language and environment to connect your ADBC client to FlightSQL server
3. Use `anonymous` as login and password for anonymous connection (if allowed by the node) or authenticate using a personal access token

An example is [available here](https://github.com/kamu-data/kamu-cli/blob/master/examples/flight-sql/python/client_flightsql_adbc.py) using Python.
