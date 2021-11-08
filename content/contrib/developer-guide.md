---
Title: Developer Guide
description: How to setup the development environment
weight: 20
alwaysopen: false
categories: []
---

# Building Locally
Prerequisites:
* Docker or Podman
  * If using `docker` - make sure it's usable without `sudo`
  * If using `podman` - make sure it's setup to run root-less containers
* Rust toolset
  * Use `rustup` to install the compiler and `cargo`
* AWS account and configured AWS CLI (optional, needed for S3 volumes)

Clone the repository:
```shell
git clone git@github.com:kamu-data/kamu-cli.git
```

Build it and run tests:
```shell
cd kamu-cli
cargo build
cargo test
```

To use your locally-built `kamu` executable link it as so:
```shell
sudo ln -s $PWD/target/debug/kamu /usr/bin/kamu
```

# Release Procedure
1. While on the feature branch, bump the crates versions using `release` tool, e.g. `cargo run --bin release -- --major / --minor / --patch`
2. Create a CHANGELOG entry for the new version
3. Create PR, wait for tests, then merge
4. Checkout and pull `master`
5. Tag the latest commit with a new version: `git tag vX.Y.Z`
6. Push the tag to repo: `git push origin tag vX.Y.Z`
7. Github Actions will pick up the new tag and create a new GitHub release from it