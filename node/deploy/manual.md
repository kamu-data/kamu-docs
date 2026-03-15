---
title: Deployment Manual
---

<Info>
Want to try out Kamu Node in a **local environment**?

Then check out the [Quick Start](/node/quick-start) guide.
</Info>

## Recommended Steps
Deployment and customization of a production environment is an iterative process, but you may want to roughly follow these steps:

### 1. Prepare your Kubernetes cluster
All Kubernetes clusters are unique and have different sets of capabilities. See the [Kubernetes](/node/deploy/k8s) page to understand the basic requirements for Kubernetes cluster before you start deploying.


### 2. Prepare artifacts & configuration
The [Artifacts](/node/deploy/artifacts) page explains Helm charts as our distribution model, which is compatible with many deployment workflows and CI/CD tools. On this stage you should register necessary Helm repositories and prepare the initial configurations for the releases.

If you are starting from scratch and don't have a strong tooling preference - we recommend you to try the "infrastructure-as-code" approach that is described in our [Quick Start](/node/quick-start) guide.


### 3. Deploy a minimal environment
We recommend you to deploy to get things running early. It's always easier to progressively customize a working deployment than to plan out everything ahead.

On this stage we recommend you to deploy the Node using in-memory transient storage and dummy auth which we will subsequently replace with real implementations.

If you are using our deployment template, once again follow the [Quick Start](/node/quick-start) guide.


### 4. Customize authentication & authorization
See [Authentication & Authorization](/node/deploy/auth) page for available options of providing own or integrating with 3rd party auth providers.


### 5. Customize dataset and operational storage
Most companies will have their own preferences for storage, databases, security, and disaster recovery workflows. For this reason in a production deployment we expect you to provide storage to Kamu Node. All storage solutions we provide with our deployment examples are meant for demonstrative purposes only and must not be used for data of any value.

See [Storage](/node/deploy/storage) page for the list of supported storage systems for data lake and operational data.


### 6. Create a capacity plan and configure resources
Kamu Node is designed to provide optimal performance of all workloads according to the available cluster capacity, applying back pressure when needed. If you are deploying the node in a Kubernetes cluster shared with other applications you may want to restrict the resource usage of the node to prevent applications from "starving" one another. Limiting capacity can also be done for cost management.

See [Capacity](/node/deploy/capacity) page to understand available configuration options and the back pressure strategies the node uses when resources are insufficient.


### 7. Security checklist
Security of the deployment is your responsibility, but our [Security](/node/deploy/security) page provides a list of things to watch out for.


### 8. Further customization
Once you have a fully working secure deployment you can further customize it to your liking. See [Customization](/node/deploy/customization) page for the list of available options.

## What's Next?
Now that you have a working deployment, see [Operator Manual](/node/operator) to learn how to keep it up-to-date and troubleshoot issues.
