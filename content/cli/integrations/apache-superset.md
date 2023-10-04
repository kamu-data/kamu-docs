---
Title: Apache Superset
description: Connecting Apache Superset to Kamu via Flight SQL.
weight: 5
categories: []
aliases:
---

[Apache Superset](https://superset.apache.org/) is an modern open-source data exploration and visualization platform. It can be connected to `kamu` via native Flight SQL protocol using Python client.

In this setup:
- `kamu` runs a Flight SQL server - a high-performance protocol for data transfer
- In the `Superset` environment we install an additional `flightsql-dbapi` Python package
- `Superset` uses generic database API provided by `SQLAlchemy` framework
- `flightsql-dbapi` package provides custom engine implementation for `SQLAlchemy` that translates all `Superset`'s queries into Flight SQL protocol

To connect `Superset` to `kamu` follow these simple steps:
1. Start with being able to run `Superset` locally using `docker-compose` (see [this official guide](https://superset.apache.org/docs/installation/installing-superset-using-docker-compose/))
   - Rest of the guide assumes that you are launching superset in "non-dev" mode using:
     ```bash
     docker-compose -f docker-compose-non-dev.yml up
     ```
2. Install [flightsql-dbapi](https://github.com/influxdata/flightsql-dbapi) Python package into `Superset` container:
   - Stop and clean up the environment:
     ```bash
     docker-compose -f docker-compose-non-dev.yml down
     ```
   - Create `<superset repo>/docker/requirements-local.txt` file (as per [this guide](https://superset.apache.org/docs/databases/docker-add-drivers/)) with the following contents:
     ```
     # At the time of this writing Superset used arrow version with a critical to us bug
     pyarrow==13.0.0
     flightsql-dbapi==0.2.1
     ```
3. (Optional) Specify your MabBox API Token in `<superset repo>/docker/.env-non-dev`
4. Run `kamu` Flight SQL server in a desired workspace:
   ```bash
   kamu sql server --flight-sql --address 0.0.0.0 --port 50050
   ```
5. Start `Superset` via `docker-compose` again
6. Create a new database connection in `Superset`
   - Use `"Other"` database kind
   - As URL specify:
     ```bash
     datafusion+flightsql://kamu:kamu@<hostname or IP>:50050?insecure=True
     ```
