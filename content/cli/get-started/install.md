---
Title: Installation
description: Covers installation steps to get kamu-cli running on your computer
weight: 15
categories: []
aliases:
  - /cli/install
  - /cli/installation
  - /cli/get-started/installation
---

{{<info>}}
Before using this product, please read the [project status disclaimer]({{<ref "project-status">}}).
{{</info>}}

## General Information
`kamu` is a **single-binary** utility that comes bundled with most of its dependencies.

It relies on container-based virtualization (e.g. `docker` or `podman`) to run such heavyweight frameworks like Spark, Flink, and Jupyter in isolated environments without needing you to install thousands of libraries and bloating your beloved laptop with their dependencies.

The tool comes with very good **shell completions**, so make sure to configure them!

Please report any issues during the installation process [here](https://github.com/kamu-data/kamu-cli/issues/).


## Supported Platforms

### Linux
Linux is our primary target environment. We don't have packages for various Linux flavors yet, but since the tool is just a simple binary it's very easy to get started:
1. Install `docker` using your distro's package manager (alternatively we highly recommend trying [podman]({{<relref "#using-podman-instead-of-docker">}}))
2. Make sure you can launch containers without `sudo` by following [official documentation](https://docs.docker.com/engine/install/linux-postinstall/)
3. Install `kamu` via installer script by running:
    ```bash
    curl -s "https://get.kamu.dev" | sh
    ```
4. Verify your setup by running:
    ```bash
    kamu system diagnose
    ```

See also:
<!-- no toc -->
- [Installing shell completions]({{<relref "#installing-shell-completions">}})
- [A Note on Docker Security]({{<relref "#a-note-on-docker-security">}})
- [Using Podman instead of Docker]({{<relref "#using-podman-instead-of-docker">}})

### MacOS X
We fully support Intel and M-series Macs, to install `kamu` please follow these steps:
1. Install [Docker for Mac](https://docs.docker.com/docker-for-mac/install/)
   1. Consider allocating more CPUs and memory to the Docker VM in the settings
   2. If you want to run `kamu` outside of your user home directory - you may need to add additional mounts to the Docker VM. For example if your workspace is in `/opt/myworkspace` you'll need to mount it under the same name into the VM in Docker settings.
2. Install `kamu` via installer script by running:
    ```bash
    curl -s "https://get.kamu.dev" | sh
    ```
3. Verify your setup by running:
    ```bash
    kamu system diagnose
    ```

See also:
<!-- no toc -->
- [Installing shell completions]({{<relref "#installing-shell-completions">}})
- [Using Podman instead of Docker]({{<relref "#using-podman-instead-of-docker">}})

### Windows (using WSL2)
1. Install WSL2 following [these steps](https://docs.microsoft.com/en-us/windows/wsl/install-win10)
2. Install `docker`
   1. We recommend you to install Docker Desktop for Windows with WSL2 backend (see [instructions](https://docs.docker.com/desktop/windows/wsl/))
   2. Ensure that from your linux distribution you can launch containers without `sudo`
3. Inside your WSL2 distribution of choice:
4. Install `kamu` via installer script by running:
    ```bash
    curl -s "https://get.kamu.dev" | sh
    ```
5. Verify your setup by running:
    ```bash
    kamu system diagnose
    ```

To get the best experience using `kamu` with WSL2 we recommend you to also:
- Use [Windows Terminal](https://apps.microsoft.com/store/detail/windows-terminal/9N0DX20HK701) that supports unicode symbols and full colors
- Configure [shell completions]({{<relref "#installing-shell-completions">}})

See also:
<!-- no toc -->
- [Installing shell completions]({{<relref "#installing-shell-completions">}})
- [Using Podman instead of Docker]({{<relref "#using-podman-instead-of-docker">}})

### Windows (using Docker Desktop)
{{<warning>}}
The native Windows binary is still highly experimental, so in most cases it's better to use the WSL
{{</warning>}}

1. Install and run [Docker Desktop](https://docs.docker.com/docker-for-windows/install/).
   1. It's a good idea to give the Docker's VM more CPU and RAM - you can do so in `VirtualBox`.
   2. Make sure that you can run `docker ps` successfully.
2. We recommend using [Windows Terminal](https://apps.microsoft.com/store/detail/windows-terminal/9N0DX20HK701) that supports unicode symbols and full colors
3. Download the latest `kamu` binary for Windows
4. Add it to your `PATH` environment variable

Docker Toolbox runs Docker in a Virtual Machine. This means to mount a file from your host file system into a Docker container the file first needs to be mounted into VM, so make sure all paths that `kamu` will need are mapped in VirtualBox VM settings.

{{<tip>}}
**Example:** Lets assume your workspace directory is `C:\Users\me\kamu`. When `kamu` runs it will detect that Docker runs in a VM it will convert it to `/c/Users/me/kamu`. So in your VM settings you may need to add a mapping from `C:\Users\me` to `/c/Users/me`.
{{</tip>}}

## Upgrading
On most platforms a new version of `kamu` can be installed by simply re-running the installer script:
```bash
curl -s "https://get.kamu.dev" | sh
```

## Installing shell completions
To be able to auto-complete the `kamu` commands please install completion scripts for the shell of your choosing. You can find detailed instructions by running `kamu completions --help`.

If you use `bash` add the following to your `~/.bashrc` file:

```bash
source <(kamu completions bash)
```

If you use `zsh` add the following to your `~/.zshrc` file:

```bash
autoload -U +X bashcompinit && bashcompinit
source <(kamu completions bash)
```

## A Note on Docker Security
We take your security very seriously. Unfortunately the execution model of `docker` that involves running the daemon process under `root` violates the Unix user permission model. Combined with the step of making `docker` command [sudo-less](https://docs.docker.com/engine/install/linux-postinstall/) this means that any process you run under your user can potentially access the entire file system with root privileges. Until `docker` changes its runtime model, sudo-less access to Docker will remain a security threat.

On our side we are taking following measures to gain your trust:
- `kamu` and all of its components are open-source and [available for review](https://github.com/kamu-data/kamu-cli/)
- All of our `docker` images are based on reputable source images and are [available for review]({{<relref "supported-engines">}})
- When `kamu` starts `docker` containers it limits the scope of volumes it's mounting to a minimum. You can review the volume mounts by running `kamu` with `-v` flag or using `docker ps`.

To avoid all these issues please consider using [`podman`]({{<relref "#using-podman-instead-of-docker">}}) - this container runtime operates in **daemon-less** and **root-less** mode, so it's fully compliant with the standard Unix permission model.


## Using Podman instead of Docker 
[`podman`](https://podman.io/) is an alternative container runtime that fixes the [security shortcomings of `docker`](#a-note-on-docker-security). We highly recommend you to give it a try, as we are planning to make it a default runtime in the near future.

{{<warning>}}
Make sure to follow [Podman's Rootless Setup Guide](https://github.com/containers/podman/blob/main/docs/tutorials/rootless_tutorial.md) to allow `kamu` to run containers without `sudo`.
{{</warning>}}

In order to instruct `kamu` to use `podman` run:

```bash
kamu config set --user engine.runtime podman
```

{{<info>}}
On some systems you need to separately install `podman-dnsname` package to allow containers to communicate with one another via hostnames. To check whether you have it run:

```bash
podman network create test
podman network ls
# NETWORK ID    NAME    VERSION  PLUGINS
# 9f86d081884c  test    0.4.0    bridge,portmap,firewall,tuning,dnsname
#                                                               ^^^ plugin installed
podman network prune
```
{{</info>}} 


## Development Images
It is sometimes convenient to get `kamu-cli` in a Docker/Podman image. For this we have few options:

- [`ghcr.io/kamu-data/kamu-base:latest`](https://github.com/kamu-data/kamu-cli/tree/master/images/kamu-base) - comes with just `podman` and `kamu-cli` pre-installed
- [`ghcr.io/kamu-data/kamu-base:latest-with-data`](https://github.com/kamu-data/kamu-cli/tree/master/images/kamu-base-with-data) - comes with a sample data pipeline that you can use to test different features with
- [`ghcr.io/kamu-data/kamu-base:latest-with-data-mt`](https://github.com/kamu-data/kamu-cli/tree/master/images/kamu-base-with-data-mt) - comes with a sample multi-tenant dataset repository

For example, try running:

```bash
docker run -it --rm ghcr.io/kamu-data/kamu-base:latest-with-data kamu list
```

{{<info>}}
These images have `podman` installed inside the container, so when `kamu` runs an engine `podman` will be trying to pull an image and start a container from within another container. For such container-in-container setup to work you may need to pass `--privileged` flag when running this image.
{{</info>}}
