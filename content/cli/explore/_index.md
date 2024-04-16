---
Title: Exploring Data
description: Viewing data and performing basic exploratory data analysis.
weight: 50
alwaysopen: false
categories: []
---

While `kamu` focuses primarily on the problem of data management, you often may want to do some basic data exploration before exporting data for further use in your data science projects, so we decided to provide a few simple exploration tools for you to assess the state of data without leaving the comfort of one tool.

## Tail Command
Use [`kamu tail`]({{<relref "cli-reference#kamu-tail">}}) command to quickly view a sample of last events in a dataset:

```bash
kamu tail ca.bccdc.covid19.case-details
```

## Inspect Command Group
A set of [`kamu inspect *`]({{<relref "cli-reference#kamu-inspect">}}) commands allows you to explore metadata and lineage of datasets. For example to display the lineage of a certain dataset in a browser use:

```bash
kamu inspect lineage ca.covid19.daily-cases -b
```

{{<image filename="/images/cli/first-steps/lineage.png" alt="kamu sql">}}

## SQL Console
[`kamu sql`]({{<relref "cli-reference#kamu-sql">}}) command group provides a simple way to run ad-hoc queries and explore data using SQL language.

{{<image filename="/images/cli/first-steps/sql.gif" alt="kamu sql">}}

Following command will drop you into the SQL shell:
```bash
kamu sql
```

By default this command uses the [Apache Datafusion](https://arrow.apache.org/datafusion/) engine, so its [powerful SQL](https://arrow.apache.org/datafusion/user-guide/sql/index.html) is now available to you.

{{<tip>}}
You can also select other engines, e.g. [Apache Spark](https://spark.apache.org/)!
{{</tip>}}

All datasets in your workspace should be available to you as tables:

```sql
show tables;
```

You can use `describe` to inspect the dataset's schema:

```sql
describe "us.cityofnewyork.data.zipcode-boundaries";
```

{{<note>}}
The extra quotes needed to treat the dataset name containing dots as a table name.
{{</note>}}

And of course you can run queries against any dataset:

```sql
select
  *
from "us.cityofnewyork.data.zipcode-boundaries"
order by pop_est desc
limit 5;
```

Use `Ctrl+D` to exit the SQL shell.

SQL is a widely supported language, so `kamu` can be used in conjunction with many other tools that support it, such as Tableau and Power BI. See [integrations]({{<ref "integrations">}}) for details.

The `kamu sql` is a very powerful command that you can use both interactively or for scripting. We encourage you to explore more of its options through `kamu sql --help`.


## Jupyter Notebooks
Kamu also connects the power of [Apache Spark](https://spark.apache.org/) with the [Jupyter Notebook](https://jupyter.org/) server. You can get started by running:

```bash
kamu notebook
```

{{<tip>}}
You can use `-e ENV_VAR` option to pass additional environment variable into the notebook server. This can be very useful for different access and security tokens needed by different visualization APIs.
{{</tip>}}

Executing this should open your default browser with a Jupyter running in it.

From here let's create a `PySpark` notebook. We start our notebook by loading `kamu` extension:

```
%load_ext kamu
```

After this the `import_dataset` command becomes available and we can load the dataset and alias it by doing:

```
%import_dataset us.cityofnewyork.data.zipcode-boundaries --alias zipcodes
```

{{<image filename="/images/cli/first-steps/notebook-001.png" alt="kamu notebook 001">}}

This will take a few seconds as in the background it creates Apache Spark session, and it is Spark that loads the dataset into what it calls a "dataframe".

You can then start using the `zipcodes` dataframe in the exact same way you would in an interactive `spark-shell`.

{{<note>}}
A few very important things to understand here:
- Spark and Jupyter are running in separate processes
- The commands you execute in the notebook are executed "remotely" and the results are transferred back
- This means that it doesn't really matter if your data is located on your machine or somewhere else - the notebook will work the same
{{</note>}}

The dataframe is automatically exposed in the SQL engine too, and you can run SQL queries using `%%sql` annotation:

{{<image filename="/images/cli/first-steps/notebook-002.png" alt="kamu notebook 002">}}

Thanks to the [sparkmagic](https://github.com/jupyter-incubator/sparkmagic) library you also get some simple instant visualizations for results of your queries.

{{<image filename="/images/cli/first-steps/notebook-003.png" alt="kamu notebook 003">}}

After you are done joining, filtering, and shaping the data you can choose to get it out of the Spark into the Jupyter notebook kernel using `%%sql -o alias` command

{{<image filename="/images/cli/first-steps/notebook-004.png" alt="kamu notebook 004">}}

Now that you have the data in Jupyter - you can use any of your favorite tools and libraries to further process it or visualize it.

## Web UI
And finally, `kamu` comes with embedded Web UI that you can use to explore your pipelines and run SQL queries on data from the comfort of your browser:

{{<image filename="/images/cli/first-steps/kamu-ui.png" alt="Kamu Web UI">}}

You can launch it by running:

```bash
kamu ui
```
