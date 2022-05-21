---
Title: Repositories
description:
weight: 10
alwaysopen: false
categories: []
aliases:
---

## Supported Repository Types
Data in `kamu` is shared via repositories. There are multiple types of repositories that differ by the kinds of services they provide. The most basic repository allows you to simply upload ("push") and download ("pull") data.

|   Type   | Description                                                                                             |   Capabilities    | URL Examples                                                                                                              |
| :------: | ------------------------------------------------------------------------------------------------------- | :---------------: | ------------------------------------------------------------------------------------------------------------------------- |
| Local FS | A basic repository that uses the local file system folder. Mainly used for examples and testing.        | `pull`<br/>`push` | `file:///home/me/example/repository`<br/>`file:///c:/Users/me/example/repository`                                         |
| HTTP(s)  | A basic repository that provides read-only access to data.                                              |      `pull`       | `https://example.org/dataset`                                                                                             |
|    S3    | A basic repository that stores data in Amazon S3 bucket. Can be used with any S3-compatible storage API | `pull`<br/>`push` | `s3://bucket.my-company.example`<br/>`s3+http://my-minio-server:9000/bucket`<br/>`s3+https://my-minio-server:9000/bucket` |
|   IPFS   | Uses IPFS HTTP Gateway for reading. Push is only possible via IPNS (see [details]({{<ref "ipfs">}})).   | `pull`<br/>`push` | `ipfs://bafy...vqhe`<br/>`ipns://k51q...v7mn`                                                                             |


## Push / Pull Aliases
Starting out, you can always use explicit URLs when syncing data from and to repositories.

If some remote source contains a dataset you're interested in you can download it using the `pull` command:
```bash
kamu pull https://example.org/dataset --as example-dataset
```

If you have a dataset you would like to share, or made some changes to a dataset you are sharing with your friends - you can upload the new data using the `push` command:
```bash
kamu push example-dataset --to s3://my-bucket.example.org/example-dataset
```

When you run these commands, `kamu` will automatically create "pull" and "push aliases" for this dataset:

```bash
kamu repo alias list example-dataset
┌─────────────────┬──────┬────────────────────────────────────────────┐
│     Dataset     │ Kind │                Alias                       │
├─────────────────┼──────┼────────────────────────────────────────────┤
│ example-dataset │ Pull │ https://example.org/dataset                │
│ example-dataset │ Push │ s3://my-bucket.example.org/example-dataset │
└─────────────────┴──────┴────────────────────────────────────────────┘
```

With aliases in place, next time you want to pull or push data you can simply do:
```bash
kamu pull example-dataset  # Will pull from https://example.org/dataset
kamu push example-dataset  # Will push to s3://my-bucket.example.org/example-dataset
```

Both `pull` and `push` commands will analyze the state of the dataset in the workspace and at the repository and will only upload data and metadata that wasn't previously seen (a minimal update).

These commands are also "safe". They will detect all types of concurrent changes and history divergence and prevent you from overwriting someone else's changes.

{{<note>}}
When you pull a `Root` dataset from a remote source running `kamu pull` on it will attempt to sync it from the repository, and NOT execute a polling or other ingest action. In `kamu list` datasets with pull aliases will be showing up as `Remote(...)`. 
{{</note>}}


## Repositories
If you store multiple datasets side by side in some locations you can add it as a repository. Repositories are configured per workspace using the `kamu repo` command group.

To add new repo use:
```bash
kamu repo add my-s3-bucket s3://my-bucket.example.org/
```

This repo will now be visible in `kamu repo list`.

To pull/push a dataset from/to this repo you can now use remote references like `<repo-name>/<dataset-name>`:
```bash
kamu pull my-s3-bucket/example-dataset
kamu pull example-dataset --to my-s3-bucket
```


## Searching for Data
To look for datasets in the repos use:

```bash
kamu search covid19

# Searching with empty query lists (a limited number of) datasets in all repos
kamu search

# You can specify the search term and specific repo to look in
kamu search covid19 --repo my-s3-bucket
```

Search is delegated to the repository implementations and its capabilities depend on the type of the repo. Whereas smart repos may support advanced full-text search, simple storage-only repos may be limited to a substring search by dataset name.
