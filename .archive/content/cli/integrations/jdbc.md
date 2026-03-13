---
Title: Generic JDBC Client
description: Connecting client applications via JDBC protocol.
categories: []
aliases:
---

To connect any client that supports JDBC protocol follow these simple steps:
1. Downlaod the latest [Flight SQL JDBC Driver](https://central.sonatype.com/artifact/org.apache.arrow/flight-sql-jdbc-driver)
2. Install the driver following the instructions of your specific client application
3. Run `kamu` Flight SQL server in a desired workspace:
    ```bash
    kamu sql server --engine datafusion --address 127.0.0.1 --port 50050
    # or
    kamu sql server --engine spark --address 127.0.0.1 --port 50050
    ```
4. Connect the client using URL:
   ```bash
   jdbc:arrow-flight-sql://127.0.0.1:50050?useEncryption=false
   ```
5. Use `anonymous` as login and password or provide an access token to authenticate

An example is [available here](https://github.com/kamu-data/kamu-cli/blob/master/examples/flight-sql/python/client_jdbc.py) using Python.