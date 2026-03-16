---
title: "Welcome to Kamu!"
sidebarTitle: Welcome
icon: hand-spock
mode: wide
---

<Tooltip headline="API" tip="Application Programming Interface: a set of protocols for software applications to communicate." cta="Read our API guide" href="/api-reference">API</Tooltip> documentation helps developers understand how to integrate with your service.


<Card
  title="First time here?"
  icon="rocket"
  href="/start/first-steps"
  horizontal
>
  Follow these steps to get started
</Card>

## Projects
Our documentation is organized around four closely related projects:

<Columns cols={2}>
  <Card>
    <h4 class="project-title"><a href="/odf">Open Data Fabric</a></h4>
    <a href="/odf"><img src="/images/projects/odf.svg" noZoom/></a>
    ODF is an open protocol spec for exchange and verifiable multi-party processing of data. It's an independent open-source project. It is included on this website for convenience of cross-referencing with the rest of documentation.

    <Columns cols={2}>
      <div><a href="/odf" class="project-quicklink">&gt; About</a></div>
      <div><a href="/odf/spec" class="project-quicklink">&gt; Specification</a></div>
      <div><a href="/odf/schemas" class="project-quicklink">&gt; Schemas</a></div>
      <div><a href="/odf/rfcs" class="project-quicklink">&gt; RFCs</a></div>
    </Columns>
  </Card>

  <Card>
    <h4 class="project-title"><a href="/cli">Kamu CLI</a></h4>
    <a href="/cli"><img src="/images/projects/kamu-cli.svg" noZoom/></a>
    A powerful command line tool that implements ODF protocol. You can run it on any device to build data pipelines, ingest and explore data, and interact with other nodes on ODF network.

    <Columns cols={2}>
      <div><a href="/cli/install" class="project-quicklink">&gt; Install</a></div>
      <div><a href="/cli/quick-start" class="project-quicklink">&gt; Quick Start</a></div>
      <div><a href="/start/tutorial" class="project-quicklink">&gt; Tutorial</a></div>
      <div><a href="/examples" class="project-quicklink">&gt; Examples</a></div>
    </Columns>
  </Card>

  <Card>
    <h4 class="project-title"><a href="/node">Kamu Node</a></h4>
    <a href="/node"><img src="/images/projects/kamu-node.svg" noZoom/></a>
    A scalable server implementation of ODF. It's a set of Kubernetes applications that can be installed in a distributed environment to:
    - Operate data pipelines
    - Verify computations done by other parties
    - Execute queries on co-located data
    - Provide data via rich set of APIs to applications and smart contracts.
  
    <Columns cols={2}>
      <div><a href="/node/quick-start" class="project-quicklink">&gt; Quick Start</a></div>
      <div><a href="/api" class="project-quicklink">&gt; APIs</a></div>
      <div><a href="/node/deploy" class="project-quicklink">&gt; Deploying</a></div>
      <div><a href="/node/commitments" class="project-quicklink">&gt; Operating</a></div>
    </Columns>
  </Card>

  <Card>
    <h4 class="project-title"><a href="/platform">Kamu Web Platform</a></h4>
    <a href="/platform"><img src="/images/projects/kamu-platform.svg" noZoom/></a>
    A front-end application that acts as a window into the ODF network. Think of it as GitHub for data pipelines or Etherscan of ODF. It can be used in multiple setups: from exploring your local Kamu CLI workspace, to managing your distributed Kamu Node deployment, and to interacting with remote nodes in the global ODF network.

    <Columns cols={2}>
      <div><a href="/platform" class="project-quicklink">&gt; Overview</a></div>
      <div><a href="/platform" class="project-quicklink">&gt; Get Started</a></div>
      <div><a href="/platform/admin" class="project-quicklink">&gt; Administration</a></div>
    </Columns>
  </Card>
</Columns>
