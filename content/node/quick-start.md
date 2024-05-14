---
Title: Quick Start
description:
weight: 5
underConstruction: false
categories: []
aliases:
---

**Ready to give Kamu Node a try?** This guide will help you deploy all components of Kamu Node and [Kamu Web Platform]({{<relref "platform">}}) on your local machine in a few simple steps.

Use it to familiarize yourself with the process of deploying all components in a minimalistic configuration. Once you are ready to deploy a production-ready node instance please refer to the [Deployment Manual]({{<relref "deploy">}}).


## Prerequisites
Kamu Node is a **Kubernetes-native application** and this guide assumes basic familiarity with Kubernetes. If you worked with `docker-compose` before - you will see a few new tools, but shouldn't encounter any problems.

Before we begin, you will need the following tools installed:
1. [**`git`**](https://git-scm.com/) - to clone the [`kamu-deploy-example`](https://github.com/kamu-data/kamu-deploy-example) repo
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

Go ahead and clone the [`kamu-deploy-example`](https://github.com/kamu-data/kamu-deploy-example) repo:
```sh
git clone https://github.com/kamu-data/kamu-deploy-example.git
cd kamu-deploy-example
```

## Select components
By default all components are enabled, but if, for example, you don't need JupyterHub open:
```
environments/minikube/environment.yaml
```
and modify it to:
```yaml
jupyterHub:
  enabled: false
```

## Deploy Kamu Node

### Using convenience script
To get all components installed and running you can use a convenience script:
```sh
./sync.sh
```

{{<warning>}}
Multiple container images will be downloaded in the process, so if script times-out it's safe to re-run again.
{{</warning>}}

Once it completes it's just a matter of exposing a few ports:

```sh
./port-forward.sh
```
```
=============== Kamu Web UI ===============
Web UI (fwd):     http://localhost:4200
Web UI:           http://192.168.X.X:30211

=============== JupyterHub ================
Web UI (fwd):     http://localhost:4300
Web UI:           http://192.168.X.X:30230

================ Kamu Node ================
GraphQL / REST:   http://192.168.X.X:30201
FlightSQL:        http://192.168.X.X:31402

================== Minio ==================
Minio API:        http://192.168.X.X:30401
Minio Console:    http://192.168.X.X:30402
Username:         admin
Password:         password123

Forwarding from 127.0.0.1:4200 -> 8080
Forwarding from 127.0.0.1:4300 -> 8000
Press Ctrl+C to exit
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

### Superset example
We are still working on automated Superset examples setup, so to see some data follow these simple steps:
1. Run `port-forward.sh` script
2. Open Superset Web UI and login
3. Go to "Settings" > "Database connections"
4. Select "+ Database" using type "Other"
5. Display name: `kamu`
6. For Sqlalchemy URL use:
   ```
   datafusion+flightsql://kamu:kamu@192.168.49.2:30241?insecure=True
   ```
   replacing the IP/port with the output of `port-forward.sh` script for `FlightSQL` protocol
7. Now go to `Datasets` tab and create one for `kamu/co.alphavantage.tickers.daily.spy`
8. Create a `Line Chart` by:
   1. dropping `event_time` onto `X-Axis`
   2. dropping `close` onto `Metrics`
   3. hitting `Create chart` at the bottom


## Making changes
After the initial deployment, if you modify any configuration you can easily **apply** your changes to the deployment using a convenience script:
```sh
./apply.sh
```
Or manually:
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
