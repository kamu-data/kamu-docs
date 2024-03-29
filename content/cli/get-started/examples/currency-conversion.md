---
Title: Currency Conversion
description:
weight: 0
categories: []
aliases:
  - /cli/learn/examples/currency-conversion
---

**Topics covered:**
- Temporal table joins

## Summary
Currency conversion is a great example of a problem that cannot be solved without considering the time dimension. As exchange rates vary significantly every day using an average rate for a certain period is a gross oversimplification of a problem that can give very inaccurate results. This example shows how `kamu` and streaming SQL can be used to join your overseas trading account data with an exchange rate stream to bring your calculations to the common currency denominator.

## Steps

### Getting Started
To follow this example checkout `kamu-cli` repository and navigate into [examples/currency_conversion](https://github.com/kamu-data/kamu-cli/tree/master/examples/currency_conversion) sub-directory.

Create a temporary kamu {{<term "workspace">}} in that folder using:

```sh
kamu init
```

You can either follow the example steps below or fast-track through it by running:

```sh
kamu add --recursive .
kamu pull --all
```

### Root Datasets
We will be using two root datasets:
- `ca.bankofcanada.exchange-rates.daily` - contains daily exchange rates between `USD` and `CAD`.
- `my.trading.transactions` - contains a transaction ledger from a fake trading account similar to what you'd get in data export from your trading platform.

The `my.trading.transactions` is sourcing its data from a file located in `data/` sub-directory, while the exchange rates are obtained from an external source - the [Bank of Canada historical exchange rates](https://www.bankofcanada.ca/rates/exchange/) dataset.

Let's add the {{<term "root datasets" "root-dataset">}} and ingest data:

```sh
kamu add ca.bankofcanada.exchange-rates.daily.yaml my.trading.transactions.yaml
kamu pull --all
```

You can verify the result using `tail` command or the SQL shell:

```bash
kamu tail ca.bankofcanada.exchange-rates.daily
```

Or explore the dataset via SQL shell:

```bash
kamu sql
```

```sql
select * from "ca.bankofcanada.exchange-rates.daily" limit 5;
```

```sql
+-------------+------------+---------------+-----------------+--------------+
| system_time |    date    | currency_base | currency_target |     rate     |
+-------------+------------+---------------+-----------------+--------------+
|     ...     | 1999-01-04 |      USD      |       CAD       | 1.5271863602 |
|     ...     | 1999-01-05 |      USD      |       CAD       | 1.5237489398 |
|     ...     | 1999-01-06 |      USD      |       CAD       | 1.5082176616 |
|     ...     | 1999-01-07 |      USD      |       CAD       | 1.5132393398 |
|     ...     | 1999-01-08 |      USD      |       CAD       | 1.5132515653 |
+-------------+------------+---------------+-----------------+--------------+
```

Remember, that after adding a dataset from a `yaml` file `kamu` creates an internal representation of it in the {{<term "workspace">}} `.kamu` directory, so **to make any changes** to the dataset you will need to **re-add** the dataset again after changing the `yaml` file.

```sh
kamu delete my.trading.transactions
# <Make changes to the yaml file>
kamu add my.trading.transactions.yaml

# Alternatively
kamu add --replace my.trading.transactions.yaml
```

### Converting transaction values into CAD
If you look at `my.trading.transactions` dataset - it contains the trading activity of a US account, so all prices and settlement amounts there are listed in US Dollars (`USD`). But let's imagine that you live in Canada and all of your other accounts and your credit cards are all in Canadian Dollars (`CAD`). It would be a lot easier for you to monitor your financials if they were in one currency.

If you analyze your financials on a quarterly or yearly basis you might've dealt with this problem by looking up an **average exchange rate** for a certain time period and used it in your calculations. This is of course an **oversimplification** that may give **misleading** results - your transactions are most likely not distributed uniformly throughout the time period, and if you live in a country with volatile economy or trading crypto - the exchange rate may fluctuate significantly.

Ideally we would like to take **every single transaction** and convert the price using the exchange rate for the corresponding date. Thankfully, `kamu` can make this process very easy using the **temporal table joins**.

Temporal table joins (see this [great explanation in Apache Flink's blog](https://flink.apache.org/2019/05/14/temporal-tables.html)) take one of the streams and represent it as a three-dimensional table. When joining to such a table you need to pass in the time argument to tell join to consider the version of the table that would exist at that point in time.

Let's have a look at the `my.trading.transactions.cad` dataset:

```yaml
kind: DatasetSnapshot
version: 1
content:
  name: my.trading.transactions.cad
  kind: Derivative
  metadata:
    - kind: SetTransform
      inputs:
        - datasetRef: ca.bankofcanada.exchange-rates.daily
        - datasetRef: my.trading.transactions
      transform:
        kind: Sql
        engine: flink
        temporalTables:
          - name: ca.bankofcanada.exchange-rates.daily
            primaryKey:
              - currency_base
        query: |
          SELECT
            tr.`event_time`,
            tr.`symbol`,
            tr.`quantity`,
            tr.`price` as `price_usd`,
            tr.`price` * exc.`rate` as `price_cad`,
            tr.`settlement` as `settlement_usd`,
            tr.`settlement` * exc.`rate` as `settlement_cad`
          FROM `my.trading.transactions` as tr
          LEFT JOIN `ca.bankofcanada.exchange-rates.daily` FOR SYSTEM_TIME AS OF tr.`event_time` as exc
          ON tr.`currency` = exc.`currency_base` AND exc.`currency_target` = 'CAD'
```
{{<note>}}
The excessive use of back ticks is currently caused by the SQL parser used by Apache Flink which is overly sensitive to reserved words - this should improve in future versions.
{{</note>}}

Using the `temporalTables` section we instruct the Flink engine to use `ca.bankofcanada.exchange-rates.daily` event stream to create a temporal table of the same name.

Here's how this three-dimensional table would look like when sliced at different points in time:

```sql
ca.bankofcanada.exchange-rates.daily:

@ 1999-01-04
+---------------+-----------------+--------------+
| currency_base | currency_target |     rate     |
+---------------+-----------------+--------------+
|      USD      |       CAD       | 1.5271863602 |
+---------------+-----------------+--------------+

@ 1999-01-05
+---------------+-----------------+--------------+
| currency_base | currency_target |     rate     |
+---------------+-----------------+--------------+
|      USD      |       CAD       | 1.5237489398 |
+---------------+-----------------+--------------+

@ 1999-01-06
+---------------+-----------------+--------------+
| currency_base | currency_target |     rate     |
+---------------+-----------------+--------------+
|      USD      |       CAD       | 1.5082176616 |
+---------------+-----------------+--------------+
```

It basically remembers the last observed value of every column grouped by the provided `primaryKey` (`currency_base` in our case).

The `LEFT JOIN ca.bankofcanada.exchange-rates.daily FOR SYSTEM_TIME AS OF tr.event_time` part can be interpreted as us taking every transaction event from `my.trading.transactions`, indexing the temporal table `ca.bankofcanada.exchange-rates.daily` at this event's `event_time` and then joining the same event with the resulting (now ordinary two-dimensional) table.

{{<note>}}
Note that `SYSTEM_TIME AS OF` syntax is a relic of SQL:2011 standard and should not be confused with Kamu's `system_time` column. The actual join is performed in the **{{<term "event time space" "event-time">}}**. You can learn more about temporal event time joins in [Flink documentation](https://nightlies.apache.org/flink/flink-docs-release-1.16/docs/dev/table/sql/queries/joins/#temporal-joins).
{{</note>}}

With theory out of the way, it's time to give this a try:

```sh
kamu add my.trading.transactions.cad.yaml
kamu pull my.trading.transactions.cad
```

The results should be:

```bash
kamu tail my.trading.transactions.cad
```
```sql
+-------------+------------+--------+----------+-----------+---------------------+
| system_time | event_time | symbol | quantity | price_usd |      price_cad      |
+-------------+------------+--------+----------+-----------+---------------------+
|     ...     | 2016-01-04 | SPY    | 1        | 201.0200  | 279.85643605283600  |
|     ...     | 2016-02-01 | SPY    | 1        | 193.6500  | 271.38399945165000  |
|     ...     | 2016-03-01 | SPY    | 1        | 198.1100  | 267.84574042498800  |
|     ...     | 2016-04-01 | SPY    | 1        | 206.9200  | 269.58244227661600  |
|     ...     | 2016-05-02 | SPY    | 1        | 207.9700  | 260.35607413671100  |
+-------------+------------+--------+----------+-----------+---------------------+
```

The best thing about this is that *you may never have to touch this SQL query again*. Each time you run `kamu pull` in the future the latest transaction data will be ingested along with latest exchange rates, producing new transactions with converted prices. This is the "write once - run forever" philosophy of `kamu` that combines best propagation times with the accuracy of solving temporal problems without taking any shortcuts.

Once you master this example - make sure to check out the [Stock Market Trading example]({{<ref "stock-trading">}}) that introduces another really important mechanism related to temporal joins - the **{{<term "watermark">}}**.