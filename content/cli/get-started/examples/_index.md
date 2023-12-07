---
Title: Examples
description: Sample data projects executed with kamu
weight: 50
categories: []
aliases:
  - /cli/learn/examples
---

## Guided Examples

| Name                                                        |    Level     |                              Topics                               |
| ----------------------------------------------------------- | :----------: | :---------------------------------------------------------------: |
| [Self-serve Demo]({{<relref "self-serve-demo">}})           |   Beginner   |                                                                   |
| [Currency Conversion]({{<relref "currency-conversion">}})   |   Beginner   |                       temporal-table joins                        |
| [COVID-19 Daily Cases]({{<relref "covid19">}})              |   Beginner   |          harmonization, unions, aggregations, notebooks           |
| [Housing Prices]({{<relref "housing-prices">}})             |   Beginner   |           GIS data, GIS functions, GIS joins, notebooks           |
| [Stock Market Trading]({{<relref "stock-trading">}})        | Intermediate |     aggregations, temporal-table joins, watermarks, notebooks     |
| [Overdue Order Shipments]({{<relref "overdue-shipments">}}) | Intermediate |                stream-to-stream joins, watermarks                 |
| [Web3 Data]({{<relref "web3-data">}})                       | Intermediate | repositories, temporal-table joins, stream processing, watermarks |

To work with examples we recommend you to clone the [kamu-cli repo](https://github.com/kamu-data/kamu-cli) and use directories in `examples/` as your workspaces.

For instance:

```bash
git clone https://github.com/kamu-data/kamu-cli.git
cd kamu-cli/examples/currency_conversion

kamu init
kamu add . -r
kamu pull --all
```

## Need More Examples?

The wild variety of formats and ways to model data used by the data publishers today often makes ingesting data a challenge. When you work with the data that is already in the ODF network you feel like a productive data scientist, but until publishers start using this format directly we'll have to continue wasting time on dull tasks like parsing CSVs, inferring schemas, and cleaning data.

To give you more examples on how to deal with **different ingest scenarios** we've created an experimental repository where we publish Root Dataset manifests for a variety of Open Data sources.

*Stuck on parsing a yet another variety of timestamps? Or confused on how to change projection of the GIS data when reading ESRI file?* 

Then check out [kamu-contrib repo](https://github.com/kamu-data/kamu-contrib).
