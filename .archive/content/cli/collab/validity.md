---
Title: Validity of Data
description: Describes audit and verification procedures that can be used to ensure the data presented to you is trustworthy
weight: 50
alwaysopen: false
categories: []
aliases:
---

This topic is also covered in detail in this video:

{{% youtube hN_vpHYmwi0 %}}

With `kamu` sharing data becomes very easy, but with that problem out of the way you will soon start wondering "How can I trust the data I downloaded from someone else?". Let's first define what validity or trustworthiness of data means.

For a more technical description see {{<term "verifiability">}}.

### Validity of Root Data
Let's say you're about to use a root dataset containing historical weather information in your city. How can you be sure it's trustworthy?

Because source data is non-reproducible, its validity depends entirely on its publisher. Publisher is in full control of the data they present, which also means that measuring and processing errors and even malicious data can easily make its way into the root dataset. Make sure that your publishers have good reputation and prefer data that comes from well-established organizations (government or NGOs) that directly collect or operate the systems from which the data is gathered.

Aside from external audits, another way to improve confidence in data is to correlate it with data from other similar sources. In our example we could compare it with the data from a weather station in the neighboring city and look for anomalies.

### Validity of Derivative Data
Derivative data in `kamu` is created purely through transformations that are recorded in metadata. These transformations can still be malicious, but since they are usually small (e.g. a few SQL queries) we can easily audit them to ensure they are sound and done in good faith. Repeating this process for the entire transformation chain, starting with root datasets, will give you confidence in trustworthiness of derivative data.

### Verifying Validity
Based on the above, here are the steps needed to ensure a dataset is trustworthy:
- Inspect lineage and identify all root datasets it's composed of
- Ensure publishers of root datasets are reputable and credible
- Use lineage to audit all derivative transformations to see if they are sound and non-malicious
- Use `kamu verify` command to ensure that data you downloaded actually matches the declared transformations

Example:

```bash
# Inspect the dependency graph of a dataset to find all root sources
kamu inspect lineage ca.vancouver.opendata.weather.aggregated-daily

# Inspect the transformations applied
# Repeat this for every derivative dataset in the dependency graph
kamu inspect query ca.vancouver.opendata.weather.aggregated-daily

# Verify the data matches the declared metadata and transformations
kamu verify --recursive ca.vancouver.opendata.weather.aggregated-daily
```

For every derivative dataset the `kamu verify` command does two things:
- Compares hashes of data you downloaded to the ones stored in metadata (ensures data is not tampered or corrupted)
- Executes the declared derivative transformations locally to compare the hash of the result to one stored in metadata (ensures that metadata was not spoofed to match the fake result)

{{<info>}}
Remember that you are not alone in the fight for data validity. Other people will also be verifying these datasets, so the Open Data Fabric network can quickly detect and exclude the participants who distribute malicious data.
{{</info>}}
