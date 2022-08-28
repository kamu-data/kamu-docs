---
Title: Sharing datasets with IPFS
description: Describes integration with content-addressable decentralized storage
weight: 20
alwaysopen: false
categories: []
aliases:
---

The `kamu` and [IPFS](https://ipfs.io/) (The Interplanetary File System) projects have overlaping goals - preserving and growing humanity's knowledge.

While IPFS focuses on storing files (objects), `kamu`'s focus is on structured data and dynamic data processing, but under the hood even a real-time dataset in `kamu` is just a set of files!

Below we show how `kamu` builds on top of many similar concepts as IPFS and how IPFS can be used as a very efficient **storage layer** for sharing your datasets and pipelines with the world.

## IPFS Basics
The IPFS is well-documented, so we will quickly review the basics, and if you find any of them confusing simply follow the links:

- IPFS is **decentralized**
  - You are fully responsible for your own data's persistence, replication, and availability ([more](https://docs.ipfs.io/concepts/persistence/))
  - To publish data you need to run a node ([more](https://docs.ipfs.io/concepts/nodes/))
  - To read data you can use your node or a public IPFS Gateway ([more](https://docs.ipfs.io/concepts/ipfs-gateway/))
- IPFS is a **content-addressable** storage ([more](https://docs.ipfs.io/concepts/content-addressing/))
  - The IPFS URL is based on a CID (content identifier) which is derived from a hash sum of the data it points to ([more](https://docs.ipfs.io/concepts/hashing/))
  - Every time the content of a file changes you get a **different URL**
  - Old and new file are different objects - the data in IPFS is **immutable** ([more](https://docs.ipfs.io/concepts/immutability/))
- **Mutability can be simulated** with special URLs that can point to different CIDs at different times
  - Currently supported naming mechanisms are [IPNS](https://docs.ipfs.io/concepts/ipns/) and [DNSLink](https://docs.ipfs.io/concepts/dnslink/)
  - IPNS uses a hashsum of a public key to create a unique name entry in a decentralized way ([more](https://docs.ipfs.io/concepts/ipns/)).

## Kamu and IPFS
Unlike any other data processing system `kamu` was build from ground up with reproducibility in mind - it defaults to never losing history. As the [ODF spec]({{<ref "spec">}}) explains in detail - the best way to do this is to represent data as **append-only** event streams. 

These event streams are represented by a linked list of metadata blocks (think git history or blockchain) that reference portions of raw data and checkpoint files:

{{<image filename="/images/pages/ipfs/odf-chain.svg" alt="ODF dataset structure" width="350px" align="center">}}

So, very similarly to IPFS, the composing parts of a datasets in `kamu` are:
- **Immutable** - dataset only changes by appending new blocks
- **Content-addressable** - a metadata block, data file, or a checkpoint are uniquely identified by their hashsum

Why it matters? Imagine you store a directory containing many large files in IPFS and it is assigned `CID1`. When you add a new file to it and do `ipfs add . -r` again IPFS will notice that it already has CIDs for all but one file and will reuse those objects:

{{<image filename="/images/pages/ipfs/ipfs-cids.svg" alt="CIDs in IPFS" width="250px" align="center">}}

If `CID1` remains "pinned" it basically represents the state of the same directory as `CID2` but at the previous point in time.

This also works for `kamu` datasets:

{{<image filename="/images/pages/ipfs/odf-chain-in-ipfs.svg" alt="ODF dataset in IPFS" width="350px" align="center">}}

- Each time you push to IPFS you are only adding the blocks and objects that were not seen previously. There is no duplication.
- Previous CIDs remain valid - they simply point to an older subset of an event stream.
- Having just one "pointer" to a metadata block you can "walk" the entire metadata chain and discover all dataset components.

Unlike many other data processing systems that mutate data, the cheapness of an "append" operation in `kamu` allows it achieve near real-time latencies of data propagation even when handling massive datasets and using immutable storage like IPFS.

{{<note>}}
The above diagrams are good to build up some intuition, but this is not exactly how data looks like in IPFS on the [IPLD DAG](https://ipld.io/) level. An accurate diagram would need to consider:
- Slicing of large files into multiple objects
- Raw vs. wrapped nodes
- Balanced vs. custom DAG structure
{{</note>}}

## Pulling from IPFS
`kamu` supports pulling data from IPFS just like from any [other repository]({{<ref "repositories">}}). 

You can use both `ipfs://` and `ipns://` URLs:

```bash
kamu pull ipfs://bafybeietcz4lxovy3ejdhb67nt3lj43vaeuyhectkqfnmmlnatfug5vqhe --as my-dataset --no-alias
kamu pull ipns://k51qzi5uqu5dic6zu9i2f4afctxmsm298ypiuy3ijmob1w6m96c092qp4ev7mn --as my-dataset
```

{{<tip>}}
Since the content behind an `ipfs://` URL never changes we use `--no-alias` flag to skip creation of the pull alias.
{{</tip>}}


### Configuring IPFS Gateway
Under the hood `kamu` will use the configured IPFS Gateway to fetch data converting the URL into something like `http(s)://{gateway}/ipfs/{cid}` or `http(s)://{gateway}/ipns/{key}`. 

By default it will try to use your local IPFS daemon as a gateway. You can see this by running:

```bash
kamu config get --with-defaults protocol.ipfs.httpGateway
> "http://localhost:8080/"
```

If you only read data from IPFS and not planning to write - you can avoid running an IPFS daemon by switching to one of the [public IPFS Gateways](https://ipfs.github.io/public-gateway-checker/):

```bash
kamu config set --user protocol.ipfs.httpGateway "https://dweb.link/"
```

## Pushing to IPFS
Clearly, pushing to an `ipfs://` URL will not work as we don't know the CID upfront, not until all data has been hashed:

```bash
kamu push my-dataset --to ipfs://<???>
```

We need a URL that remains stable when the underlying dataset is updated - we can use [IPNS](https://docs.ipfs.io/concepts/ipns/) for this. 

IPNS is like a named pointer to a CID that can be re-pointed to a different CID only by its owner. To create unique collision-free names in a decentralized way and to have a way for you to prove ownership of this name at the same time IPNS is using cryptographic key pairs:
- A public/private key pair is generated
- Name is derived by hashing the public key
- Private key is used for signing publishing requests to prove that you are the owner of said name.

To push data to IPFS you will need a local IPFS daemon running.

We first generate a new key pair that we will use for our dataset:

```bash
ipfs key gen my-dataset
> k51qzi5uqu5dgl4gf3uayepenee5tzix3r8oiwyimxsfuikr7alq928xxtwmew
```

We can now use this key to form a destination URL as `ipns://{key}` and push the dataset:

```bash
kamu push my-dataset --to ipns://k51qzi5uqu5dgl4gf3uayepenee5tzix3r8oiwyimxsfuikr7alq928xxtwmew
```

{{<warning>}}
Currently IPNS keys have a default lifetime of 24h (see `ipfs name publish --help`). This means you'll need to run push command periodically (e.g. on a cron job) to prevent it from expiring. Otherwise your URL will become non-resolvable.
{{</warning>}}

Since IPNS pointers are mutable the next time we update the dataset we can push it again using the push alias `kamu` created for us:

```bash
# Update the dataset locally
kamu pull my-dataset 
> <Dataset is updated>

# Push updates via IPNS push alias
kamu push my-dataset
> Syncing dataset (my-dataset > ipns://k51q...wmew)
> Updated to <head> (1 block(s))
```

And that's all there is to it! You now have all the basic building blocks to create **fully decentralized data pipelines**, both on storage and compute levels!
