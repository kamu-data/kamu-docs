---
Title: Generic JDBC Client
description: Connecting client applications via JDBC protocol.
weight: 10020
categories: []
aliases:
---

To connect any client that supports JDBC protocol follow these simple steps:
1. Downlaod the latest [Flight SQL JDBC Driver](https://central.sonatype.com/artifact/org.apache.arrow/flight-sql-jdbc-driver)
2. Install the driver following the instructions of your specific client application
3. Run `kamu` Flight SQL server in a desired workspace:
    ```bash
    kamu sql server --flight-sql --address 127.0.0.1 --port 50050
    ```
4. Connect the client using URL:
   ```bash
   jdbc:arrow-flight-sql://127.0.0.1:50050?useEncryption=false
   ```
5. Use `kamu` as login and password
