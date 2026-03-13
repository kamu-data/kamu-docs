---
Title: MQTT
description:
categories: []
aliases:
---

**🚧 This page is under construction 🚧**

Kamu Node supports ingesting data using the [MQTT](https://mqtt.org/) protocol. See {{<schema "FetchStep::Mqtt">}} and this [example](https://github.com/kamu-data/kamu-cli/tree/master/examples/mqtt).

In current implementation Kamu Node acts as an MQTT **client** that subscribes to a given set of topics , meaning that an external broker is required to ingest MQTT data, and this broker needs to be accessible to wherever environment Kamu Node is running.

In future versions we are planning to add support for a simple publish-only **broker** in Kamu Node itself, allowing you to connect MQTT devices to it directly. If your use case requires this - let us know!

## Data Delivery Guarantees
Kamu Node may not have perfect connectivity with MQTT broker, so prolonged periods of disconnects should be accounted for. Additionally, MQTT sources can be used even with [kamu-cli]({{<ref "/cli">}}) tool, and since the tool doesn't use any background processes it will connect to MQTT broker only when you run:

```sh
kamu pull my-mqtt-device
```

What data `kamu` can get when it is connected to the broker depends on:
- [Retained](https://www.hivemq.com/blog/mqtt-essentials-part-8-retained-messages/) message mode
- [QoS level](https://www.hivemq.com/blog/mqtt-essentials-part-6-mqtt-quality-of-service-levels/) of the publisher (e.g. device) and the subscriber (`kamu`)
- Implementation of your MQTT broker - since delivery semantics is left under-specified in the core MQTT spec.

For example:
- `retained: true, qos: 0 (at most once)` - will ensure that broker remembers the last message from a device and always transmits it to `kamu` upon reconnect. This mode is sufficient for a lot of cases e.g. where device periodically reports temperature data and `kamu` periodically ingests the readings on its own schedule.
- `retained: false, qos: 1 (at least once)` - will *likely* make broker to buffer all messages from the device and deliver them to `kamu` upon reconnect. This mode is good for devices like door sensors, where the whole series of events matters. The exact behavior is very broker-specific, so make sure to read you broker's documentation.

{{<note>}}
You can use [merge strategies]({{<ref "merge-strategies">}}) to avoid duplication of retained data in your dataset.
{{</note>}}