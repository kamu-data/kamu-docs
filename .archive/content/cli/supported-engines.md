---
Title: Supported Data Engines
description: Describes strengths and development state of different engines supported by kamu
weight: 20
categories: []
aliases:
---

All data processing in `kamu` is done by a set of plug-in {{<term "engines">}}. This allows us to integrate many mature data processing frameworks, use them to transform data, while `kamu` coordinates all the advanced aspects of processing, tracks {{<term "provenance">}}, ensures {{<term "verifiability">}}, etc.

{{<note>}}
The opinions below relate to ODF adapters implemented using the described engine, not the engines themselves. Engines featured here all have very different designs, making them more suitable for some tasks than others. Information below is intended as a rough guidance for engine choice within ODF and should be taken with a big grain of salt.
{{</note>}}

## Known Engine Implementations

| Name         |                              Technology                               |                                                                      Query Dialect                                                                       |                                                           Links                                                            | Notes                                                                                                                                                                                                                                                                                                                                                      |
| ------------ | :-------------------------------------------------------------------: | :------------------------------------------------------------------------------------------------------------------------------------------------------: | :------------------------------------------------------------------------------------------------------------------------: | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `spark`      |               [Apache Spark](https://spark.apache.org/)               | [Spark Streaming SQL](https://spark.apache.org/docs/latest/sql-ref.html) with [Sedona GIS Extensions](https://sedona.apache.org/1.5.0/api/sql/Overview/) |      [Repository](https://github.com/kamu-data/kamu-engine-spark)<br/>[Image](https://ghcr.io/kamu-data/engine-spark)      | Spark is used in `kamu-cli` for all data ingestion and is default (but not only) engine for SQL shell. Spark is also used in combination with Livy to query data from embedded Jupyter Notebooks. It's currently the only engine that supports **GIS data** via Apache Sedona integration.                                                                 |
| `flink`      |               [Apache Flink](https://flink.apache.org/)               |                     [Flink Streaming SQL](https://ci.apache.org/projects/flink/flink-docs-master/docs/dev/table/sql/gettingstarted/)                     |      [Repository](https://github.com/kamu-data/kamu-engine-flink)<br/>[Image](https://ghcr.io/kamu-data/engine-flink)      | Flink has most mature support for stream processing, like stream-to-stream and stream-to-table joins, windowed aggregations, watermarks etc. It's thus the recommended engine for most derivative datasets.                                                                                                                                                |
| `datafusion` | [Apache Arrow DataFusion](https://github.com/apache/arrow-datafusion) |                                     [DataFusion SQL](https://arrow.apache.org/datafusion/user-guide/sql/index.html)                                      | [Repository](https://github.com/kamu-data/kamu-engine-datafusion)<br/>[Image](https://ghcr.io/kamu-data/engine-datafusion) | An extremely fast and low-footprint **batch processing** engine. DataFusion is also embedded into `kamu-cli` and is used for data ingestion, ad-hoc SQL queries, and SQL console. Despite being a batch-only engine it can still be used in pipelines for simple map/filter/union operations where temporal semantics is not needed.                       |
| `risingwave` |      [RisingWave](https://github.com/risingwavelabs/risingwave)       |                                        [RisingWave SQL](https://docs.risingwave.com/docs/current/sql-references/)                                        | [Repository](https://github.com/kamu-data/kamu-engine-risingwave)<br/>[Image](https://ghcr.io/kamu-data/engine-risingwave) | Experimental stream process engine. There are [ongoing attempts](https://github.com/apache/arrow-datafusion/issues/4285) to add stream processing functionality. DataFusion is also embedded into `kamu-cli` and is used for executing ad-hoc SQL queries. We are aiming to make data ingest functionality use DataFusion for most cases instead of Spark. |

### Schema Support

| Feature      | kamu  | Spark | Flink | DataFusion | RisingWave |
| ------------ | :---: | :---: | :---: | :--------: | :--------: |
| Basic types  |   ✔️   |   ✔️   |   ✔️   |     ✔️      |     ✔️      |
| Decimal type |   ✔️   |   ✔️   |  ✔️**  |     ✔️      |     ✔️      |
| Nested types |  ✔️*   |   ✔️   |   ❌   |    ❔***    |    ❔***    |
| GIS types    |  ✔️*   |   ✔️   |   ❌   |     ❌      |     ❌      |

✔️* - There is currently no way to express nested and GIS data types when declaring root dataset schemas, but you still can use them through pre-processing queries

✔️** - Apache Flink has known issues with Decimal type and currently relies on our patches that have not been upstreamed yet, so stability is not guaranteed [FLINK-17804](https://issues.apache.org/jira/browse/FLINK-17804).

❔ - Engine capability exists but requires more integration testing


### Operation Types

Note that ODF always operates in {{<term "event time">}}, this all temporal aggregations and joins have to be supported by the engine in event-time processing mode.

| Feature                       | Spark | Flink | DataFusion | RisingWave |
| ----------------------------- | :---: | :---: | :--------: | :--------: |
| Filter                        |   ✔️   |   ✔️   |     ✅      |     ✅      |
| Map                           |   ✔️   |   ✔️   |     ✅      |     ✅      |
| Aggregation: Window functions |   ❌   |   ✔️   |     ❌      |     ✅      |
| Aggregation: Tumbling windows |   ❌   |   ✔️   |     ❌      |     ✅      |
| Aggregation: Top-N            |   ❌   |   ❔   |     ❌      |     ✅      |
| Join: Windowed                |   ❌   |   ✔️   |     ❌      |     ❔      |
| Join: Temporal Table          |   ❌   |   ✔️   |     ❌      |     ❔      |
| GIS extensions                |   ✅   |   ❌   |     ❌      |     ❌      |

✔️ - supported<br>
✅ - supported and recommended<br>
❌ - not supported<br>
❔ - engine capability exists but requires more integration testing