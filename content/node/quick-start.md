---
Title: Quick Start
description:
weight: 5
underConstruction: false
categories: []
aliases:
---

**Ready to give Kamu Node a try?** This guide will help you deploy all components of Kamu Node and [Kamu Web Platform]({{<relref "platform">}}) on your local machine in four simple steps.

Use it to familiarize yourself with the process of deploying all components in a minimalistic configuration. Once you are ready to deploy a production-ready node instance please refer to the [Deployment Manual]({{<relref "deploy">}}).


## Prerequisites
Kamu Node is a **Kubernetes-native application** and this guide assumes basic familiarity with Kubernetes. If you worked with `docker-compose` before - you will see a few new tools, but shouldn't encounter any problems.

Before we begin, you will need the following tools installed:
1. [**`git`**](https://git-scm.com/) - to clone the example deploy repo
2. [**`minikube`**](https://minikube.sigs.k8s.io/docs/) - to create a local Kubernetes cluster
3. [**`kubectl`**](https://kubernetes.io/docs/reference/kubectl/) - client for interacting with Kubernetes cluster
4. [**`helm`**](https://helm.sh/) - software management tool for Kubernetes
5. [**`helmfile`**](https://helmfile.readthedocs.io) - "infrastructure-as-code" wrapper for `helm`
6. [**`aws-cli`**](https://aws.amazon.com/cli/) (optional) - needed to download example datasets


## Start your cluster
First we will start by creating a local Kubernetes cluster using `minikube`:
```sh
minikube start
```

{{<info>}}
You can also specify how much resources to allocate to the cluster. For example, we can let it use all available resources as:
```sh
minikube start --cpu no-limit --memory no-limit
```

{{</info>}}

Once command finishes you should have a fully functional Kubernetes cluster running on your local machine!

Ensure that `kubectl` client can communicate with your new cluster:

```sh
kubectl get pods --all-namespaces
```
```
NAMESPACE     NAME                               READY   STATUS    RESTARTS  AGE
kube-system   kube-apiserver-minikube            1/1     Running   0         2m8s
kube-system   etcd-minikube                      1/1     Running   0         2m7s
...
```


## Clone the example repo
While we could deploy all components by running `helm install` commands, we will use "infrastructure-as-code" approach where the entire state of our deployment is described by files in a `git` repository.

Go ahead and clone the example repo:
```sh
git clone https://github.com/kamu-data/kamu-deploy-example.git
cd kamu-deploy-example
```

## Deploy Kamu Node

### Using convenience script
To get all components installed and running you can use a convenience script:
```sh
./deploy.sh
```
```
===========================================================
                      KAMU                                 
-----------------------------------------------------------
Kamu Web UI:      http://192.168.XX.YY:30211
Kamu API:         http://192.168.XX.YY:30201
```

You can now open the provided `Kamu Web UI` URL in your browser and see the [Kamu Web Platform]({{<relref "platform">}}) interface.


### Using helmfile
Instead of the convenience script you can use `helmfile` directly to **synchronize** the current state the cluster with the desired state of our deployment defined in configuration files:
```sh
export MINIKUBE_HOST=$(minikube ip)
helmfile -e minikube sync
```

Either way you will now have multiple `kamu` component pods running:

```sh
kubectl get pods
```
```
NAME                               READY   STATUS      RESTARTS   AGE
kamu-api-server-79974ff49c-5bb7s   1/1     Running     0          1h
kamu-web-ui-85fb7b7957-vb5kf       1/1     Running     0          1h
minio-58c59dd784-4jkfk             1/1     Running     0          1h
minio-provisioning-zfz5n           0/1     Completed   0          1h
...
```

## Example Content
If you open the `Kamu Web UI` URL in your browser you will see a functional but very empty platform.

To load some example data to play with use:
```sh
./bootstrap-examples.sh
```

Refresh the browser tab and you should see a lot of new pipelines to explore.


## Making changes
After the initial deployment, if you modify any configuration you can easily **apply** your changes to the deployment using:
```sh
helmfile -e minikube apply
```


## Under the hood
Main entry point of this repository is `helmfile.yaml` which:
- Configures some basic `helm` parameters (e.g. deployment timeouts)
- Connects [Kamu's helm chart repository](https://artifacthub.io/packages/search?org=kamu)
- Defines the `minikube` environment
- And defines a multi-layer structure for supplying configuration values to individual helm chart releases

The skeleton `helmfile.yaml` provided in this example is simple yet very capable. It can be a good foundation for operating multiple different Kamu Node environments in production.


## What's Next?
See [Architecture]({{<relref "node/architecture">}}) section for the description of all components we have installed and how they interoperate.

Once you get familiar and comfortable with this local setup - proceed to the [Deployment Manual]({{<relref "node/deploy">}}) for instructions on setting up a production-grade environment.

Oh, and don't forget to clean up your `minikube` environment:
```sh
minikube delete
```
