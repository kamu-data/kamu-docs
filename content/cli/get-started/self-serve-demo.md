---
Title: Self-Serve Demo
description:
weight: 15
categories: []
aliases:
---

This demo guides you through the basics of using `kamu` and its key concepts. It lets you try out most of the tool's features without having to install it.

{{<info>}}
The demo is also available online at: https://demo.kamu.dev

*(for financial reasons the capacity of this environment is limited)*
{{</info>}}

## Requirements
To run this demo you'll only need:
* `docker`
* `docker-compose`

## Running
First you will need to download the `docker-compose.yml` file:

```bash
wget https://raw.githubusercontent.com/kamu-data/kamu-cli/master/images/demo/docker-compose.yml
```

To run all demo components on your computer simply do:

```bash
docker-compose up
```

> If you've ran the environment before you might want to get latest versions of the images using `docker-compose pull` command.

This will run:
* JupyterHub web notebooks with Kamu integration
* Minio - S3-like storage server used as a shared dataset repository

Once you start the environment you should see a log line that looks like this:

```
jupyter_1  |   http://127.0.0.1:8765/?token=...
```

Use this URL in your browser to open Jupyter. Once in Jupyter, navigate to the `demo` directory, open first notebook, and follow the instructions.

Enjoy, and please send us [your feedback](https://github.com/issues)!

## Shutting down
To shutdown the environment do:

```bash
docker-compose down
```