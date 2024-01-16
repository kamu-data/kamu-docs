---
Title: Supported Data Engines
description: Describes strengths and development state of different engines supported by kamu
weight: 20
categories: []
aliases:
---

All data processing in `kamu` is done by a set of plug-in engines. This allows us to integrate many mature data processing frameworks, while having `kamu` coordinate all processing to track provenance and ensure verifiability.

## Known Engine Implementations

| Name         |                              Technology                               |                                                                      Query Dialect                                                                       |                                                           Links                                                            | Notes                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| ------------ | :-------------------------------------------------------------------: | :------------------------------------------------------------------------------------------------------------------------------------------------------: | :------------------------------------------------------------------------------------------------------------------------: | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `spark`      |               [Apache Spark](https://spark.apache.org/)               | [Spark Streaming SQL](https://spark.apache.org/docs/latest/sql-ref.html) with [Sedona GIS Extensions](https://sedona.apache.org/1.5.0/api/sql/Overview/) |      [Repository](https://github.com/kamu-data/kamu-engine-spark)<br/>[Image](https://ghcr.io/kamu-data/engine-spark)      | Spark is used in `kamu-cli` for all data ingestion and is default (but not only) engine for SQL shell. Spark is also used in combination with Livy to query data from embedded Jupyter Notebooks. It's currently the only engine that supports **GIS data** via Apache Sedona integration.                                                                                                                                                                |
| `flink`      |               [Apache Flink](https://flink.apache.org/)               |                     [Flink Streaming SQL](https://ci.apache.org/projects/flink/flink-docs-master/docs/dev/table/sql/gettingstarted/)                     |      [Repository](https://github.com/kamu-data/kamu-engine-flink)<br/>[Image](https://ghcr.io/kamu-data/engine-flink)      | Flink has most mature support for stream processing, like stream-to-stream and stream-to-table joins, windowed aggregations, watermarks etc. It's thus the recommended engine for most derivative datasets.                                                                                                                                                                                                                                               |
| `datafusion` | [Apache Arrow DataFusion](https://github.com/apache/arrow-datafusion) |                                               [DataFusion SQL](https://github.com/apache/arrow-datafusion)                                               | [Repository](https://github.com/kamu-data/kamu-engine-datafusion)<br/>[Image](https://ghcr.io/kamu-data/engine-datafusion) | Experimental engine that has limited functionality (due to being batch-oriented), but is **extremely fast** and **low-footprint**. There are [ongoing attempts](https://github.com/apache/arrow-datafusion/issues/4285) to add stream processing functionality. DataFusion is also embedded into `kamu-cli` and is used for executing ad-hoc SQL queries. We are aiming to make data ingest functionality use DataFusion for most cases instead of Spark. |

### Schema Support

| Feature      | kamu  | Spark | Flink | DataFusion |
| ------------ | :---: | :---: | :---: | :--------: |
| Basic types  |   ✔️   |   ✔️   |   ✔️   |     ✔️      |
| Decimal type |   ✔️   |   ✔️   |  ✔️**  |     ✔️      |
| Nested types |  ✔️*   |   ✔️   |   ❌   |     ❌      |
| GIS types    |  ✔️*   |   ✔️   |   ❌   |     ❌      |

`*` There is currently no way to express nested and GIS data types when declaring root dataset schemas, but you still can use them through pre-processing queries

`**` Apache Flink has known issues with Decimal type and currently relies on our patches that have not been upstreamed yet, so stability is not guaranteed [FLINK-17804](https://issues.apache.org/jira/browse/FLINK-17804).


### Operation Types

| Feature                           | Spark | Flink | DataFusion |
| --------------------------------- | :---: | :---: | :--------: |
| Filter                            |   ✔️   |   ✔️   |     ✔️      |
| Map                               |   ✔️   |   ✔️   |     ✔️      |
| Aggregations                      |  ❌*   |   ✔️   |     ❌      |
| Stream-to-Stream Joins            |  ❌*   |   ✔️   |     ❌      |
| Projection / Temporal Table Joins |  ❌*   |   ✔️   |     ❌      |
| GIS extensions                    |   ✔️   |   ❌   |     ❌      |

`*` Spark Engine is capable of stream processing but temporarily we have to use it in the batch processing mode, so only row-level operations like map and filter are currently usable, as those do not require correct stream processing and watermark semantics.