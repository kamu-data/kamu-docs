---
Title: Troubleshooting
description: Diagnosing the errors and reporting issues.
weight: 100
categories: []
aliases:
---

Here are some tips on diagnosing the errors:

## Common Environment Issues
This command can be used to verify your environment setup:

```sh
kamu system diagnose
```
<pre><i>
docker installed .. <span style="color:green">ok</span>
docker can pull images .. <span style="color:green">ok</span>
docker can run without sudo .. <span style="color:green">ok</span>
docker can mount volumes .. <span style="color:green">ok</span>
workspace consistency check .. <span style="color:green">ok</span>
...
</i></pre>

## Standard Logging
When `kamu` runs, it logs into `.kamu/run` directory. This directory is **cleaned up on every run**, so if you encounter an error make sure to copy important logs before running next `kamu` command.

## Verbose Logging
When encountering an error that is not descriptive enough you may want to see more debugging information by using `kamu -v <command>` flag. This flag will redirect `kamu` log output into the terminal (while removing all UI widgets for clarity) and will enable backtrace information on errors. Please use this mode when submitting bugs on this repo.

## Tracing
Using `kamu --trace` flag allows you to record the execution of the program and open [Perfetto UI](https://perfetto.dev/) in a browser, allowing to easily analyze async code execution and task performance.

> Note: If you are using Brave or a similar high-security browser and get an error from Perfetto when loading the trace - try disabling the security features to allow the UI app fetch data from `http://localhost:9001`.

{{<image filename="/images/cli/index/trace-perfetto.png" alt="Perfetto UI displaying a trace">}}

## Engine Errors
In this early stages of development `kamu` does a minimal amount of error reporting from engines, so you might definitely encounter some issues that will require an ability to read exception information logged by the engines.

When `kamu` runs an engine it redirects its logs into `.kamu/run` directory. If you get a cryptic "engine operation failed" error you will need to inspect the logs in that directory for some clues on why your query failed.

Bear with us while we are working on improving the error reporting and introducing more guard rails to prevent errors in the first place.

## Reporting Issues
If you could not resolve the error yourself - please file an issue in our [GitHub repository](https://github.com/kamu-data/kamu-cli).
