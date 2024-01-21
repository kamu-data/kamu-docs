---
Title: Project Status
description: The state of development of the project's key functionality
weight: 10
categories: []
aliases:
---

## Project Status Disclaimer
`kamu` is at the MVP stage of maturity, but is still **actively evolving**. Before `v1.0` we reserve the right to break compatibility between the releases.

Therefore, we don't recommend using `kamu` in production yet. When you use it for projects, make sure to **maintain your source data separately** and not rely on `kamu` for durable long-term data storage. This way any time a new version comes out that breaks some compatibility you can simply delete your workspace and re-create it from scratch in a matter of seconds.

### Note on Performance
Please be patient with current performance and resource usage. Stream processing technologies is a relatively new area, and some of the data processing engines `kamu` uses (e.g. Apache Spark and Flink) are tailored to run in large clusters, not on a laptop. They take a lot of resources to just boot up, so the *start-stop* nature of `kamu`'s transformations is at odds with their design. We are hoping that the industry will recognize our use-case and expect to see a better support for it in future. We are committed to continuously improving the performance and user experience.


## Feature Coverage

| Feature                               |  ODF  | kamu  |
| ------------------------------------- | :---: | :---: |
| Root datasets                         |   ✔️   |   ✔️   |
| Ingest merge strategies               |   ✔️   |   ✔️   |
| Derivative datasets                   |   ✔️   |   ✔️   |
| Verifiability - Metadata integrity    |   ✔️   |   ✔️   |
| Verifiability - Data integrity        |   ✔️   |   ✔️   |
| Verifiability - Transformation replay |   ✔️   |   ✔️   |
| Engines - Determinism enforcement     |   ❌   |   ❌   |
| Source evolution                      |   ❌   |   ❌   |
| Schema evolution                      |   ❌   |   ❌   |
| Query migrations                      |   ❌   |   ❌   |
| Engine versioning                     |   ❌   |   ❌   |
| Engine migrations                     |   ❌   |   ❌   |
| Dataset identity                      |   ✔️   |   ✔️   |
| Dataset ownership                     |   ❌   |   ❌   |
| Transaction signing                   |   ❌   |   ❌   |
| Data encryption                       |   ❌   |   ❌   |



## Stability

| Component              | Stability |
| ---------------------- | :-------: |
| Dataset on-disk layout | Unstable  |
| CLI interface          | Unstable  |
| Engine interface       | Unstable  |


---

See also:
- [Supported engines]({{<ref "supported-engines">}})