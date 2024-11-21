---
Title: Licensing Terms
description:
weight: 30
alwaysopen: false
categories: []
aliases:
  - /contrib/license
---

## Brief explanation of Kamu's license
Kamu is using [Business Source License](https://mariadb.com/bsl-faq-adopting/) (BSL). We chose it as the closest thing to a fully Open Source license that allows us to build a sustainable business and continue to pursue our ambitious technology goals.

Under BSL:

- All source **code is provided in the open**
- All your **contributions benefit the community** in the same way as with any Open Source project
- Most people and organizations can **use the product for free** in any environment and for any purpose
  - The **only condition** as imposed by the "Additional Use Grant" is to **not provide product's functionality as a service** to third parties
  - If you clearly don't fall into this category - you can stop reading here. It's that simple :)

## Understanding the Change Date

If you look at the [LICENSE.txt](https://github.com/kamu-data/kamu-cli/blob/master/LICENSE.txt) you will see the "Change Date" that is roughly 4 years from now. It represents the date on which a _specific version_ of this software will automatically convert into permissive Apache 2.0 license ("Change License").

We increment this date during every release, so earlier versions of our software are closer to becoming pure Open Source.


## Motivation behind using BSL
The BSL license was **created by MariaDB** to strike a balance between being able to run a financially viable software company while still supporting the original tenets of Open Source, such as empowering all software developers to be part of the innovation cycle – giving them open access to the code so they can modify or distribute the software by making the entire source code available from the start. Ultimately, hoping that BSL will create more Open Source software.

BSL allows us to fund the project, while allowing virtually anyone to use our software for free. Because our solution is decentralized and encourages alternative implementations by being developed as an open standard we are hoping to create an environment where companies profit from data by providing **great value-added services at a fair price**, not by holding your data hostage.

As opposed to the "open-core" model, we believe BSL license also avoids wasting effort and splitting up the community when an open-source clone has to be written from scratch to be used instead of some proprietary component that does not satisfy some use cases.


## Who else is using BSL?
Unfortunately, there are many precedents where the work of Open Source companies was bluntly exploited. This not only prevents the developers of the technology from reaping the well-deserved rewards, but also prevents them from **re-investing the resources into improving the tech**, which leads to stagnation. Many such companies have successfully adopted the BSL license as a way to restore the balance:

- [MariaDB](https://mariadb.com/bsl-faq-adopting/)
- [CockroachDB](https://www.cockroachlabs.com/blog/oss-relicensing-cockroachdb/)
- [Couchbase](https://blog.couchbase.com/couchbase-adopts-bsl-license/)
- [Sentry](https://blog.sentry.io/2019/11/06/relicensing-sentry)

{{<info>}}
Same reasons have also lead to creation of the [SSPL license](https://www.mongodb.com/licensing/server-side-public-license/faq) by MongoDB, which is also adopted by many companies, but we chose BSL for being **simpler and less ambiguous**.
{{</info>}}


## FAQ

**_Can a company use Kamu for free to provide their data to customers?_**

Yes, the way we look at it is:

- Your company uses `kamu` internally to publish datasets
- Datasets are available online in [ODF format]({{<ref "odf">}}), which is an open protocol
- Your clients independently can use `kamu` (or any other tool compatible with ODF) to download data

Since you're not running `kamu` _for_ your customers - you're good according to the "Additional Use Grant".
