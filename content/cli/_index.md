---
Title: Kamu CLI
description:
weight: 20
topLevelElement: true
topLevelProject: true
alwaysopen: false
categories: ["CLI"]
aliases:
---

<div align="center">

{{<image filename="/images/kamu-logo-slogan.png" alt="Kamu logo" width="50%">}}

[Repository] | [Demo] | [Tutorials] | [Examples] | [FAQ] | [Chat]


[![Release](https://img.shields.io/github/v/release/kamu-data/kamu-cli?include_prereleases&logo=rust&logoColor=orange&style=for-the-badge)](https://github.com/kamu-data/kamu-cli/releases/latest)
[![CI](https://img.shields.io/github/actions/workflow/status/kamu-data/kamu-cli/build.yaml?logo=githubactions&label=CI&logoColor=white&style=for-the-badge&branch=master)](https://github.com/kamu-data/kamu-cli/actions)
[![Chat](https://shields.io/discord/898726370199359498?style=for-the-badge&logo=discord&label=Discord)](https://discord.gg/nU6TXRQNXC)

</p>
</div>

## About
`kamu` *(pronounced [kæmˈuː](https://en.wikipedia.org/wiki/Albert_Camus))* is a command-line tool for management and verifiable processing of structured data.

It's a green-field project that aims to enable **global collaboration on data** on the same scale as seen today in software.

You can think of `kamu` as:
- ***Local-first data lakehouse*** - a free alternative to Databricks / Snowflake / Microsoft Fabric that can run on your laptop without any accounts, and scale to a large on-prem cluster
- ***Kubernetes for data pipelines*** - an *infrastructure-as-code* framework for building ETL pipelines using [wide range of open-source SQL engines](https://docs.kamu.dev/cli/supported-engines/)
- ***Git for data*** - a tamper-proof ledger that handles data ownership and preserves full history of changes to source data
- ***Blockchain for data*** - a verifiable computing system for transforming data and recording fine-grain provenance and lineage
- ***Peer-to-peer data network*** - a set of [open data formats and protocols](https://github.com/open-data-fabric/open-data-fabric/) for:
  - Non-custodial data sharing
  - Federated querying of global data as if one giant database
  - Processing pipelines that can span across multiple organizations.


### Featured Video
<div align="center">
<a href="https://www.youtube.com/watch?v=M7DyV-QUZbk&list=PLV91cS45lwVG20Hicztbv7hsjN6x69MJk"><img alt="Kamu: Unified On/Off-Chain Analytics Tutorial" src="https://img.youtube.com/vi/M7DyV-QUZbk/0.jpg" width="50%"/></a>
</div>


## Quick Start
Use the installer script _(Linux / MacOSX / WSL2)_:
```sh
curl -s "https://get.kamu.dev" | sh
```

* Watch [introductory videos](https://www.youtube.com/watch?v=oUTiWW6W78A&list=PLV91cS45lwVG20Hicztbv7hsjN6x69MJk) to see `kamu` in action
* Follow the ["Getting Started"]({{<ref "get-started">}}) guide through an online demo and installation instructions.


## How it Works

### Ingest from any source
`kamu` works well with popular data extractors like Debezium and provides [many built-in sources]({{<ref "/cli/ingest">}}) ranging from polling data on the web to MQTT broker and blockchain logs.

<div align="center">
{{<image filename="/images/cli/index/pull-multi.gif" alt="Ingesting data" width="65%">}}
</div>


### Track tamper-proof history
Data is stored in [Open Data Fabric]({{<ref "/odf">}}) (ODF) format - an open **Web3-native format** inspired by Apache Iceberg and Delta.

In addition to "table" abstraction on top of Parquet files, ODF provides:
- Cryptographic integrity and commitments
- Stable references
- Decentralized identity, ownership, attribution, and permissions (based on [W3C DIDs](https://www.w3.org/TR/did-core/))
- Rich extensible metadata (e.g. licenses, attachments, semantics)
- Compatibility with decentralized storages like [IPFS](https://ipfs.tech)

Unlike Iceberg and Delta that encourage continuous loss of history through Change-Data-Capture, ODF format is **history-preserving**. It encourages working with data in the [event form](https://www.kamu.dev/blog/a-brief-history-of-time-in-data-modelling-olap-systems/), and dealing with inaccuracies through [explicit retractions and corrections]({{<ref "retractions-corrections">}}).


### Explore, query, document
`kamu` offers a wide range of [integrations]({{<ref "integrations">}}), including:
- Embedded SQL shell for quick EDA
- Integrated Jupyter notebooks for ML/AI
- Embedded Web UI with SQL editor and metadata explorer
- Apache Superset and many other BI solutions

<div align="center">
{{<image filename="/images/cli/first-steps/sql.gif" alt="SQL Shell" width="65%">}}

{{<image filename="/images/cli/first-steps/notebook-005.png" alt="Integrated Jupyter notebook" width="65%">}}
</div>


### Build enterprise-grade ETL pipelines
Data in `kamu` can only be [transformed through code]({{<ref "transform">}}). An SQL query that cleans one dataset or combines two via JOIN can be used to create a **derivative dataset**.

`kamu` doesn't implement data processing itself - it integrates [many popular data engines](https://docs.kamu.dev/cli/supported-engines/) *(Flink, Spark, DataFusion...)* as plugins, so you can build an ETL flow that uses the strengths of different engines at different steps of the pipeline:

<div align="center">
{{<image filename="/images/cli/first-steps/kamu-ui.png" alt="Complex ETL pipeline in Kamu Web UI" width="65%">}}
</div>


### Get near real-time consistent results
All derivative datasets use **stream processing** that results in some [revolutionary qualities](https://www.kamu.dev/blog/end-of-batch-era/):
- Input data is only read once, minimizing the traffic
- Configurable balance between low-latency and high-consistency
- High autonomy - once pipeline is written it can run and deliver fresh data forever with little to no maintenance. 


### Share datasets with others
ODF datasets can be shared via any [conventional](https://docs.kamu.dev/cli/collab/repositories/) (S3, GCS, Azure) and [decentralized]({{<ref "ipfs">}}) (IPFS) storage and easily replicated. Sharing a large dataset is simple as:

```sh
kamu push covid19.case-details "s3://datasets.example.com/covid19.case-details/"
```

Because dataset **identity is an inseparable part of the metadata** - dataset can be copied, but everyone on the network will know who the owner is.


### Reuse verifiable data
`kamu` will store the transformation code in the dataset metadata and ensure that it's **deterministic and reproducible**. This is a form of **verifiable computing**.

You can send a dataset to someone else and they can confirm that the data they see in fact corresponds to the inputs and code:

```sh
# Download the dataset
kamu pull "s3://datasets.example.com/covid19.case-details/"

# Attempt to verify the transformations
kamu verify --recursive covid19.case-details
```

Verifiability allows you to [establish trust]({{<ref "validity">}}) in data processed by someone you don't even know and detect if they act maliciously.

Verifiable trust allows people to **reuse and collaborate** on data on a global scale, similarly to open-source software.


### Query world's data as one big database
Through federation, data in different locations can be queried as if it was in one big data lakehouse - `kamu` will take care of how to compute results most optimally, potentially delegating parts of the processing to other nodes.

Every query result is accompanied by a **cryptographic commitment** that you can use to reproduce the same query days or even months later.


### Start small and scale progressively
`kamu` offers unparalleled flexibility of deployment options:
- You can build, test, and debug your data projects and pipelines on a laptop
- Incorporate online storage for larger volumes, but keep processing it locally
- When you need real-time processing and 24/7 querying you can run the same pipelines with [`kamu-node`]({{<ref "/node">}}) as a small server
- A node can be deployed in Kubernetes and scale to a large cluster.


### Get data to and from blockchains
Using `kamu` you can easily [read on-chain data]({{<ref "blockchain-source">}}) to run analytics on smart contracts, and provide data to blockchains via novel [Open Data Fabric oracle]({{<ref "oracle">}}).



## Use Cases

In general, `kamu` is a great fit for cases where data is exchanged between several independent parties, and for (low to moderate frequency & volume) mission-critical data where high degree of trustworthiness and protection from malicious actors is required.

{{< tabs tabTotal="5" tabID="1" tabName1="Open Data" tabName2="Science & Research" tabName3="Data-driven Journalism" tabName4="Business core data" tabName5="Personal analytics">}} 

{{< tab tabNum="1" >}}
To share data **outside of your organization** today you have limited options:

- You can publish it on some open data portal, but lose ownership and control of your data
- You can deploy and operate some open-source data portal (like CKAN or Dataverse), but you probably have neither time nor money to do so
- You can self-host it as a CSV file on some simple HTTP/FTP server, but then you are making it extremely hard for others to discover and use your data

Let's acknowledge that for organizations that produce the most valuable data (governments, hospitals, NGOs), publishing data is **not part of their business**. They typically don't have the incentives, expertise, and resources to be good publishers.

This is why the goal of `kamu` is to make data publishing **cheap and effortless**:
- It invisibly guides publishers towards best data management practices (preserving history, making data reproducible and verifiable)
- Adds as little friction as exporting data to CSV
- Lets you host your data on any storage (S3, IPFS, GCS, FTP etc.)
- Maintain full control and ownership of your data

As opposed to just the download counter you get on most data portals, `kamu` brings publishers closer to the communities allowing them to see who and how uses their data. You no longer send data into "the ether", but create a **closed feedback loop** with your consumers.
{{< /tab >}}

{{< tab tabNum="2" >}}
One of the driving forces behind `kamu`'s design was the [ongoing reproducibility crisis](https://www.nature.com/articles/533452a) in science, which we believe to a large extent is caused by our poor data management practices.

After incidents like [The Surgisphere scandal](https://www.the-scientist.com/features/the-surgisphere-scandal-what-went-wrong--67955) the sentiment in research is changing from assuming that all research is done in good faith, to considering any research unreliable until proven otherwise.

Data portals like Dataverse, Dryad, Figshare, and Zenodo are helping reproducibility by **archiving data**, but this approach:
- Results in hundreds of millions of poorly systematized datasets
- Tends to produce the research based on stale and long-outdated data
- Creates lineage and provenance trail that is very manual and hard to trace (through published papers)

In `kamu` we believe that the majority of valuable data (weather, census, health records, financial core data) **flows continuously**, and most of the interesting insights lie around the latest data, so we designed it to bring **reproducibility and verifiability to near real-time data**.

When using `kamu`:

- Your data projects are **100% reproducible** using a built-in stable references mechanism
- Your results can be reproduced and **verified by others in minutes**
- All the data prep work (that often accounts for [80% of time of a data scientist](https://www.forbes.com/sites/gilpress/2016/03/23/data-preparation-most-time-consuming-least-enjoyable-data-science-task-survey-says/?sh=348d5f876f63)) can be shared and **reused** by others
- Your data projects will **continue to function** long after you've moved on, so the work done years ago can continue to produce valuable insights with minimal maintenance on your part
- Continuously flowing datasets are much **easier to systematize** than the exponentially growing number of snapshots
{{< /tab >}}

{{< tab tabNum="3" >}}
Data-driven journalism is on the rise and has proven to be extremely effective. In the world of misinformation and extremely polarized opinions data provides us an anchoring point to discuss complex problems and analyze cause and effect. Data itself is non-partisan and has no secret agenda, and arguments around different interpretations of data are infinitely more productive than ones based on gut feelings.

Unfortunately, too often data has issues that undermine its trustworthiness. And even if the data is correct, it's very easy to pose a question about its sources that will take too long to answer - the data will be dismissed, and the gut feelings will step in.

This is why `kamu`'s goal is to make data **verifiably trustworthy** and make answering **provenance** questions a **matter of seconds**. Only when data cannot be easily dismissed we will start to pay proper attention to it.

And once we agree that source data can be trusted, we can build analyses and **real-time dashboards** that keep track of complex issues like corruption, inequality, climate, epidemics, refugee crises, etc.

`kamu` prevents good research from going stale the moment it's published!
{{< /tab >}}

{{< tab tabNum="4" >}}
`kamu` aims to be the most reliable data management solution that provides recent data while maintaining the **highest degree of accountability** and **tamper-proof provenance**, without you having to put all data in some central database. 

We're developing it with financial and pharmaceutical use cases in mind, where **audit and compliance could be fully automated** through our system.

Note that we currently focus on mission-critical data and `kamu` is not well suited for IoT or other high-frequency and high-volume cases, but can be a good fit for insights produced from such data that influence your company's decisions and strategy.
{{< /tab >}}

{{< tab tabNum="5" >}}
Being data geeks, we use `kamu` for data-driven decision-making even in our personal lives. 

Actually, our largest data pipelines so far were created for personal finance:
- to collect and harmonize data from multiple bank accounts
- convert currencies
- analyze stocks trading data. 

We also scrape a lot of websites to make smarter purchasing decisions. `kamu` lets us keep all this data up-to-date with an **absolute minimal effort**.
{{< /tab >}}

{{< /tabs >}}

## Features

`kamu` connects **publishers** and **consumers** of data through a decentralized network and lets people **collaborate** on extracting insight from data. It offers many perks for everyone who participates in this first-of-a-kind data supply chain:

{{< tabs tabTotal="4" tabID="2" tabName1="For Data Publishers" tabName2="For Data Scientists" tabName3="For Data Consumers" tabName4="For Data Exploration">}} 

{{< tab tabNum="1" >}}
- Easily **share your data** with the world **without moving it** anywhere
- Retain full **ownership and control** of your data
- Close the feedback loop and **see who and how uses your data**
- Provide **real-time**, **verifiable and reproducible** data that follows the best data management practices
{{< /tab >}}

{{< tab tabNum="2" >}}
- **Ingest any existing dataset** from the web
- Always **stay up-to-date** by pulling latest updates from the data sources with just one command
- Use **stable data references** to make your data projects fully reproducible
- **Collaborate** on cleaning and improving data of existing datasets
- Create derivative datasets by transforming, enriching, and summarizing data others have published
- **Write query once and run it forever** - our pipelines require nearly zero maintenance
- Built-in support for **GIS data**
- **Share** your results with others in a fully reproducible and reusable form
{{< /tab >}}

{{< tab tabNum="3" >}}
- **Download** a dataset from a shared repository
- **Verify** that all data comes from trusted sources using 100% accurate **lineage**
- **Audit** the chain of transformations this data went through
- **Validate** that downloaded was not tampered with a single command
- **Trust** your data by knowing where every single bit of information came from with our **fine grain provenance**
{{< /tab >}}

{{< tab tabNum="4" >}}
- Explore data and run **ad-hoc SQL queries**
- Launch a **Jupyter notebook** with one command
- Join, filter, and shape your data using SQL
- Visualize the result using your favorite library
- Explore complex pipelines in Web UI
{{< /tab >}}

{{< /tabs >}}


## Community

If you like what we're doing - support us by [starring the repo](https://github.com/kamu-data/kamu-cli), this helps us a lot!

For the list of our community resource and guides on how to contribute [start here]({{<ref "community">}}).


[Repository]: https://github.com/kamu-data/kamu-cli
[Demo]: {{<ref "demo">}}
[Tutorials]: {{<ref "get-started/learning-materials">}}
[Examples]: {{<ref "examples">}}
[FAQ]: {{<ref "faq">}}
[Chat]: https://discord.gg/nU6TXRQNXC
