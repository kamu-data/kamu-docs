---
Title: Demo
description: A detailed self-guided tour of the took and its features
weight: 11
categories: []
aliases:
  - /cli/demo
  - /cli/self-serve-demo
  - /cli/get-started/self-serve-demo
---

## Online Demo Environment
The self-guided demo is available online at: https://demo.kamu.dev

{{<info>}}
The capacity of this environment is limited and you may experience a worse performance than running it on your machine.
{{</info>}}


## Video Intro
Check out this video for a quick overview of key functionality:
{{<youtube-list PLV91cS45lwVG20Hicztbv7hsjN6x69MJk>}}

The demo described below will guide you through the basics of using `kamu` and let you try out most of the tool's features without having to install it.


## Run It Yourself
### Requirements
To run this demo you'll only need:
* `docker`
* `docker-compose`

### Running
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

### Shutting down
To shutdown the environment do:

```bash
docker-compose down
```