---
Title: DBeaver
description: Connecting DBeaver via JDBC protocol.
weight: 10
categories: []
aliases:
---

[DBeaver](https://dbeaver.io/) is a great free database exploration tool. It can be connected to `kamu` using a JDBC driver.

In this setup:
- `kamu` runs an [Arrow Flight SQL](https://arrow.apache.org/docs/format/FlightSql.html) server - a high-performance protocol for data transfer
- `DBeaver` loads a special JDBC driver - a Java software module that implements an abstract database interface
- JDBC driver translates `DBeaver`'s commands into efficient Flight SQL calls in `kamu`

To connect `DBeaver` to `kamu` follow these simple steps:
1. Downlaod the latest [Flight SQL JDBC Driver](https://central.sonatype.com/artifact/org.apache.arrow/flight-sql-jdbc-driver)
2. Add a new database driver in `DBeaver` by following [these steps](https://dbeaver.com/docs/dbeaver/Database-drivers/)
   - For class name use:
        ```
        org.apache.arrow.driver.jdbc.ArrowFlightJdbcDriver
        ```
   - For URL template use:
        ```
        jdbc:arrow-flight-sql://{host}:{port}
        ```
   - In libraries add the driver's `.jar` file you just downloaded
3. Run `kamu` Flight SQL server in a desired workspace:
    ```bash
    kamu sql server --flight-sql --address 127.0.0.1 --port 50050
    ```
4. Create a new connection in `DBeaver` using the driver you created:
   - Specify host and port, e.g. `127.0.0.1:50050`
   - Use `"kamu"` as username and password
   - In `Driver properties` tab add user property:
     ```bash
     useEncryption=false
     ```

