---
Title: Tableau
description: Connecting Tableau via JDBC protocol.
weight: 70
categories: []
aliases:
---

[Tableau](https://www.tableau.com/) is a professional business intelligence tool. It can be connected to `kamu` using a JDBC driver.

In this setup:
- `kamu` runs an [Arrow Flight SQL](https://arrow.apache.org/docs/format/FlightSql.html) server - a high-performance protocol for data transfer
- `Tableau` loads a special JDBC driver - a Java software module that implements an abstract database interface
- JDBC driver translates `Tableau`'s commands into efficient Flight SQL calls in `kamu`

To connect `Tableau` to `kamu` follow these simple steps:
1. Downlaod the latest [Flight SQL JDBC Driver](https://central.sonatype.com/artifact/org.apache.arrow/flight-sql-jdbc-driver)
2. Install the driver into `Tableau` (see [official instructions](https://help.tableau.com/current/pro/desktop/en-us/examples_otherdatabases_jdbc.htm)) by copying the `.jar` file to:
   - Windows: `C:\Program Files\Tableau\Drivers`
   - Mac: `~/Library/Tableau/Drivers`
   - Linux: `/opt/tableau/tableau_driver/jdbc`
3. Run `kamu` Flight SQL server in a desired workspace:
    ```bash
    kamu sql server --flight-sql --address 127.0.0.1 --port 50050
    ```
4. Create a new connection in `Tableau` using `Other Databases (JDBC)` as a source:
   - Select `PostgreSQL` in the dialect selector
   - As URL specify:
        ```bash
        jdbc:arrow-flight-sql://127.0.0.1:50050?useEncryption=false
        ```
   - Use `"kamu"` as username and password
