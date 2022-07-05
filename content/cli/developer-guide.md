---
Title: Developer Guide
description: How to setup the development environment
weight: 110
alwaysopen: false
categories: []
---

# Building Locally
Prerequisites:
* Docker or Podman (note: unit tests run with Podman by default)
  * If using `docker` - make sure it's usable without `sudo` ([guidelines](https://docs.docker.com/engine/install/linux-postinstall))
  * If using `podman` - make sure it's setup to run root-less containers ([guidelines](https://github.com/containers/podman/blob/main/docs/tutorials/rootless_tutorial.md))
* Rust toolset
  * Install `rustup`
  * When running `cargo` in the repository it will detect and download the right toolchain version based on the `rust-toolchain` file
* Additional tools
  * Install [`jq`](https://stedolan.github.io/jq)
  * Install [`go-ipfs`](https://docs.ipfs.io/install/command-line/#official-distributions)
* AWS account and configured AWS CLI (optional, needed for S3 volumes)

Clone the repository:
```shell
git clone git@github.com:kamu-data/kamu-cli.git
```

Build it:
```shell
cd kamu-cli
cargo build
```

To use your locally-built `kamu` executable link it as so:
```shell
sudo ln -s $PWD/target/debug/kamu-cli /usr/bin/kamu
```


## Run Tests with Podman (Recommended)

Prepare test containers once before running tests:
```shell
cargo run --bin kamu-cli -- config set --user engine.runtime podman
kamu init --pull-test-images
```

Then run tests:
```shell
cargo test
```


## Run Tests with Docker (Alternative)

Prepare test containers once before running tests:
```shell
kamu init --pull-test-images
```

Then run tests:
```shell
KAMU_CONTAINER_RUNTIME_TYPE=docker cargo test

```


## Build Speed Tweaks (Optional)
Consider configuring Rust to use `lld` linker, which is much faster than the default `ld` (may improve link times by ~10-20x).

To do so install `lld`, then create `~/.cargo/config.toml` file with the following contents:

```toml
[build]
rustflags = ["-C", "link-arg=-fuse-ld=lld"]
```

One more alternative is to use `mold` linker, which is also much faster than the default `ld`.

To do so install `mold` or build it with `clang++` compiler from [mold sources](https://github.com/rui314/mold#how-to-build) then create `~/.cargo/config.toml` file with the following contents:

```toml
[build]
linker = "clang"
rustflags = ["-C", "link-arg=-fuse-ld=mold"]
```


## Building with Web UI (Optional)
To build the tool with embedded Web UI you will need to clone and build [kamu-web-ui](https://github.com/kamu-data/kamu-web-ui) repo or use pre-built release. Now build the tool while enabling the optional feature and passing the location of the web root directory:

```shell
KAMU_WEB_UI_DIR=`pwd`/../kamu-web-ui/dist/kamu-platform/ cargo build --features kamu-cli/web-ui
```

Note: `KAMU_WEB_UI_DIR` requires absolute path

Note: in debug mode the directory content is not actually being embedded into the executable but accessed from the specified directory.

# Release Procedure
1. While on the feature branch, bump the crates versions using `release` tool, e.g. `cargo run --bin release -- --major / --minor / --patch`
2. Create a CHANGELOG entry for the new version
3. Create PR, wait for tests, then merge
4. Checkout and pull `master`
5. Tag the latest commit with a new version: `git tag vX.Y.Z`
6. Push the tag to repo: `git push origin tag vX.Y.Z`
7. Github Actions will pick up the new tag and create a new GitHub release from it