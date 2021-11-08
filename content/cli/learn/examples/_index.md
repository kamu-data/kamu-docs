---
Title: Examples
description:
weight: 20
categories: []
aliases:
---

| Name                                                        |    Level     |                          Topics                           |
| ----------------------------------------------------------- | :----------: | :-------------------------------------------------------: |
| [Self-serve Demo]({{<relref "self-serve-demo">}})           |   Beginner   |         datasets, repositories, data verification         |
| [Currency Conversion]({{<relref "currency-conversion">}})   |   Beginner   |                   temporal-table joins                    |
| [COVID-19 Daily Cases]({{<relref "covid19">}})              |   Beginner   |      harmonization, unions, aggregations, notebooks       |
| [Housing Prices]({{<relref "housing-prices">}})             |   Beginner   |       GIS data, GIS functions, GIS joins, notebooks       |
| [Stock Market Trading]({{<relref "stock-trading">}})        | Intermediate | aggregations, temporal-table joins, watermarks, notebooks |
| [Overdue Order Shipments]({{<relref "overdue-shipments">}}) | Intermediate |            stream-to-stream joins, watermarks             |

To work with examples we recommend you to clone this repo and use directories in `examples/` as your workspaces. 

For instance:

```bash
git clone https://github.com/kamu-data/kamu-cli.git
cd kamu-cli/examples/currency_conversion

kamu init
kamu add . -r
kamu pull --all
```
