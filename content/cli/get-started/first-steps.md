---
Title: First Steps
description: A quick rundown of the key features to get a feel for the tool
weight: 25
categories: []
aliases:
---

For a quick overview of key functionality you can also view this tutorial:
{{<youtube-list PLV91cS45lwVG20Hicztbv7hsjN6x69MJk>}}

This tutorial will give you a high-level tour of `kamu` and show you how it works through examples.

We assume that you have already followed the [installation steps]({{<ref "installation">}}) and have `kamu` tool ready.

{{<info>}}
**Not ready to install just yet?**

Try `kamu` in this [self-serve demo]({{<ref "self-serve-demo">}}) without needing to install anything.
{{</info>}}

Don't forget to set up **shell completions** - they make `kamu` a lot more fun to use!


## Using the help command
When you execute `kamu` or `kamu -h` - the help message about all top-level commands will be displayed.

To get help on individual commands type:
```bash
kamu <command> -h
```

This will usually contain a detailed description of what command does along with usage examples.

Note that some command also have sub-commands, e.g. `kamu repo {add,list,...}`, same help pattern applies to those as well:
```bash
kamu repo add -h
```

## Getting data in

Throughout this tutorial we will be using the [Modified Zip Code Areas](https://data.cityofnewyork.us/Health/Modified-Zip-Code-Tabulation-Areas-MODZCTA-/pri4-ifjk) dataset from New York Open Data Portal.

### Initializing the workspace
To work with `kamu` you first need a **workspace** - this is where kamu will store the important information about datasets and the cached data. Let's create one:

{{<image filename="/images/cli/first-steps/init.gif" alt="kamu init">}}

```bash
mkdir my_workspace
cd my_workspace
kamu init
```

A workspace is just a directory with `.kamu` folder where all sorts of data and metadata are stored.

As you'd expect the workspace is currently empty:
```bash
kamu list
```

### Adding a dataset
One of the design principles of `kamu` is to always know exactly where any piece of data came from, so it never simply copies data - instead we create links to an external data (we'll get into the details of that later). For now let's create such link.

{{<image filename="/images/cli/first-steps/pull.gif" alt="kamu pull">}}

Datasets that ingest external data in `kamu` are called **root** datasets. To create one, we will use a `DatasetSnapshot` manifest from the [kamu-contrib repo](https://github.com/kamu-data/kamu-contrib/blob/master/us.cityofnewyork.data/zipcode-boundaries.yaml) which looks like this:

```yaml
kind: DatasetSnapshot
version: 1
content:
  name: us.cityofnewyork.data.zipcode-boundaries
  kind: Root
  metadata:
    - kind: SetPollingSource
      fetch:
        kind: Url
        # Dataset home: https://data.cityofnewyork.us/Health/Modified-Zip-Code-Tabulation-Areas-MODZCTA-/pri4-ifjk
        url: https://data.cityofnewyork.us/api/geospatial/pri4-ifjk?date=20240115&accessType=DOWNLOAD&method=export&format=Shapefile
      read:
        kind: EsriShapefile
      merge:
        kind: Snapshot
        primaryKey:
          # Modified ZIP Code Tabulation Area (ZCTA)
          # See for explanation: https://nychealth.github.io/covid-maps/modzcta-geo/about.html
          - modzcta

```

A `DatasetSnapshot` manifest contains a `name` of the dataset, its `kind` (`Root` or `Derivative`) and a series of `metadata` events that define dataset's desired state. 

In this example we only have one such event - `SetPollingSource`, which describes how `kamu` can ingest external data by performing following operations:
- `fetch` - downloading the data from some external source (e.g. HTTP/FTP)
- `prepare` (optional) - steps for preparing data for ingestion (e.g. extracting an archive or converting between formats)
- `read` - reading the data into a structured form
- `preprocess` (optional) - shaping the structured data and converting types into best suited form using query engines
- `merge` - merging the new data from the source with the **history of previously seen data**

You can find more information about the ingest types and stages in [ingest documentation]({{<ref "ingest">}}).

{{<tip>}}
To create your own dataset manifests use `kamu new` command - it outputs a well-annotated template that you can customize for your needs.
{{</tip>}}

Note that the data file we are ingesting is in ESRI Shapefile format, which is a common format for geo-spatial data, so we are using a special `EsriShapefile` reader in our dataset manifest.

You can either copy this file content or add it directly to workspace from URL like so:

```bash
$ kamu add https://raw.githubusercontent.com/kamu-data/kamu-contrib/master/us.cityofnewyork.data/zipcode-boundaries.yaml
```

At this point no data was yet loaded from the source:
```bash
$ kamu list
┌──────────────────────────────────────────┬──────┬────────┬─────────┬──────┐
│                   Name                   │ Kind │ Pulled │ Records │ Size │
├──────────────────────────────────────────┼──────┼────────┼─────────┼──────┤
│ us.cityofnewyork.data.zipcode-boundaries │ Root │   -    │       - │    - │
└──────────────────────────────────────────┴──────┴────────┴─────────┴──────┘
```

To fetch it run:

```bash
kamu pull --all
```

At this point the source data will be downloaded, decompressed, parsed into the structured form, preprocessed and saved locally.

Note that when you `pull` a dataset, only the new records that `kamu` haven't previously seen will be added. In fact `kamu` preserves the complete history of all data - this is what enables you to have stable references to data, lets you "time travel", and establish from where and how certain data was obtained (provenance). We will discuss this in depth in further tutorials.

For now it suffices to say that all data is tracked by `kamu` in a series of blocks. The `Committed new block X` message you've seen during the `pull` tells us that the new data block was appended. You can inspect these blocks using `log` command:

```bash
$ kamu log us.cityofnewyork.data.zipcode-boundaries
```


## Exploring data
Since you might not have worked with this dataset before you'd want to explore it first.

For this `kamu` provides many tools (from basic to advanced):
* `tail` command
* SQL shell
* Jupyter notebooks integration
* Web UI


### Tail command
To quickly preview few last events of any dataset use `tail` command:

```bash
$ kamu tail us.cityofnewyork.data.zipcode-boundaries
```


### SQL shell
SQL is the _lingua franca_ of the data science and `kamu` uses it extensively. So naturally it provides you a simple way to run ad-hoc queries on data.

{{<image filename="/images/cli/first-steps/sql.gif" alt="kamu sql">}}

Following comand will drop you into the SQL shell:
```bash
kamu sql
```

Under the hood it starts [Apache Spark](https://spark.apache.org/), so its [powerful SQL](https://spark.apache.org/docs/latest/sql-ref.html) engine is now available to you.

All datasets in your workspace should be available to you as tables:

```sql
show tables;
```

You can use `describe` to inspect the dataset's schema:

```sql
describe `us.cityofnewyork.data.zipcode-boundaries`;
```

> Note the extra back ticks needed to treat the dataset ID containing dots as a table name.

For brevity you can create aliases as:

```sql
create temp view zipcodes as (select * from `us.cityofnewyork.data.zipcode-boundaries`);
```

And of course you can run queries against any dataset:

```sql
select * from zipcodes order by pop_est desc limit 5;
```

Use `Ctrl+D` to exit the SQL shell.

SQL is a widely supported language, so `kamu` can be used in conjunction with many other tools that support it, such as Tableau and Power BI. See [integrations]({{<ref "integrations">}}) for details.

The `kamu sql` is a very powerful command that you can use both interactively or for scripting. We encourage you to explore more of its options through `kamu sql --help`.


### Notebooks
Kamu also connects the power of Apache Spark with the [Jupyter Notebook](https://jupyter.org/) server. You can get started by running:

```bash
kamu notebook -e MAPBOX_ACCESS_TOKEN=<your mapbox token>
```

{{<note>}}
Above we also tell `kamu` to pass the [MapBox](https://www.mapbox.com/) access token as `MAPBOX_ACCESS_TOKEN` environment variable into Jupyter, which we will use for plotting. If you don't have a MapBox token - simply run `kamu notebook`.
{{</note>}}

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

The dataframe is automatically exposed in the SQL engine too, and you can run SQL queries using `%%sql` annotation. You can copy and try some queries from [this existing notebook](https://github.com/kamu-data/kamu-contrib/blob/master/us.cityofnewyork.data/zipcode-boundaries.density.ipynb).

{{<image filename="/images/cli/first-steps/notebook-002.png" alt="kamu notebook 002">}}

Thanks to the [sparkmagic](https://github.com/jupyter-incubator/sparkmagic) library you also get some simple instant visualizations for results of your queries.

{{<image filename="/images/cli/first-steps/notebook-003.png" alt="kamu notebook 003">}}

After you are done joining, filtering, and shaping the data via SQL or PySpark - you can choose to get it out into the Jupyter notebook kernel by adding `-o population_density` flag. This will transfer the results of the query into the notebook as [Pandas](https://pandas.pydata.org/) dataframe, which you can further process and visualize:

{{<image filename="/images/cli/first-steps/notebook-004.png" alt="kamu notebook 004">}}

Example of visualizing population density data as a *choropleth* chart using [mapboxgl](https://github.com/mapbox/mapboxgl-jupyter) library:

{{<image filename="/images/cli/first-steps/notebook-005.png" alt="kamu notebook 005">}}

You can find this as well as many other notebooks in [kamu-contrib](https://github.com/kamu-data/kamu-contrib) repo.


### Web UI
All the above and more is also available to you via embedded Web UI which you can launch by running:

```bash
kamu ui
```

Web UI is especially useful once you start developing complex stream processing pipelines, to explore them more visually:

{{<image filename="/images/cli/first-steps/kamu-ui.png" alt="Kamu Web UI">}}

## Conclusion
We hope this quick overview inspires you to give `kamu` a try! 

Don't get distracted by the pretty notebooks and UIs though - we covered only the tip of the iceberg. The true power of `kamu` lies in how it manages data, letting you to reliably track it, transform it, and share results with your peers in an easily **reproducible an verifiable** way. 


Please continue to the [self-serve demo]({{<ref "self-serve-demo">}}) for some hands-on walkthroughs and tutorials, and check out our other [learning materials]({{<ref "learning-materials">}}).
