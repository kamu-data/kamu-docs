---
Title: Ingesting Data
description: Getting raw / source / root data into the system. Understanding the process of publishing data and the properties of root datasets.
weight: 30
bookCollapseSection: true
categories: []
---

Ingestion is the process by which external data is added into Open Data Fabric's {{<term "root datasets" "root-dataset">}}. Below we will describe why this process is necessary and how it works.

## Motivation
When interacting with data on the web we usually cannot make any assumptions about guarantees that its publisher provides:
- Just by looking at the data we cannot tell if it is **mutable** or preserves **history of changes**
- We often can't tell where it **originates** from and who can be held **accountable** for its **validity**
- We can't be sure that it's sufficiently **replicated**, so that if the server that hosts it today disappears tomorrow - all our data science projects will not be left **non-reproducible**.

Data on the web is in a state of a *constant churn* where data is often updated in destructive ways and even important medical datasets disappear over night. Any guarantees do exist are hidden behind many layers of service agreements, yet still provide us no strong assurance that they won't be violated (on purpose or by accident). This is why step #1 of every data science project is to **copy and version** the data.

[Open Data Fabric]({{<relref "spec">}}) was created to **avoid excessive copying and harmful versioning** of data, and instead embed these guarantees into the data format itself, making them **impossible to violate**.

Ingestion step is about getting the external data from this *"churning world"* into strict ledgers of {{<term "root datasets" "root-dataset">}}, where properties like clear ownership, reproducibility, accountability, and complete historical account can be guaranteed and made explicit.

## Sources
There are two types of ingestion sources:
- **Push sources** - for cases when external actor actively sends data into a dataset. This is suitable e.g. for IoT devices that periodically write data, business processes that can report events directly into ODF dataset, or for ingesting data from streaming data APIs and event queues like [Apache Kafka](https://kafka.apache.org/).
- **Polling source** - for cases when external data is stored somewhere in bulk and we want to synchronize its state with ODF dataset periodically. This is suitable e.g. for datasets that exist as files on the web or for reading data from bulk APIs.

## Phases
Ingestion process has several well-defined phases:
<div align="center">
{{ <image filename="/images/cli/ingest/ingest.png" alt="Ingest flow"> }}
</div>

These phases are directly reflected in the {{<schema "SetPollingSource">}} event:
- `fetch` - specifies how to download the data from some external source (e.g. HTTP/FTP) and how to cache it efficiently
- `prepare` (optional) - specifies how to prepare raw binary data for reading (e.g. extracting an archive or converting between formats)
- `read` - specifies how to read the data into structured form (e.g. as CSV or Parquet)
- `preprocess` (optional) - allows to shape the structured data with queries (e.g. to parse and convert types into best suited form wit SQL)
- `merge` - specifies how to **combine the read data with the history of previously seen data** (this step is extremely important as it performs "ledgerization" / "historization" of the evolving state of data - see [Merge Strategies]({{<relref "merge-strategies">}}) section for explanation).

{{<tip>}}
If you are confused about what `SetPollingSource` event is - please refer to [First Steps]({{<relref "first-steps">}}) section that explains dataset creation.
{{</tip>}}

The phases of push ingest are defined by the {{<schema "AddPushSource">}} event and are very similar, except for omitting `fetch` and `prepare` steps.

For more information refer to [Polling Sources]({{<relref "polling-source">}}) and [Push Sources]({{<relref "push-source">}}) sections.

## Further Reading
- For more information about defining data sources refer to [Polling Sources]({{<relref "polling-source">}}) and [Push Sources]({{<relref "push-source">}}) sections.
- For examples of dealing with various types of data refer to [Input Formats]({{<relref "input-formats">}}) section.
- For detailed explanation of "ledgerization" process see [Merge Strategies]({{<relref "merge-strategies">}}) section.
- For more inspiration on creating {{<term "root datasets" "root-dataset">}} see [Examples]({{<relref "examples">}}) and [`kamu-contrib`](https://github.com/kamu-data/kamu-contrib/) repo.