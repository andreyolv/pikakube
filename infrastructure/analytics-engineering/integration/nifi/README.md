[← Integration](../README.md)

# Apache NiFi

<https://github.com/apache/nifi>
<https://nifi.apache.org/>

---

> **Not an ELT tool.** NiFi is a **dataflow** system — routing, mediation and transformation
> between arbitrary systems. Using it to load a warehouse works and misses the point.

## The problem it solves

Moving data between systems that were never designed to talk to each other, with routing
decisions, transformation, and guarantees along the way.

Its distinguishing features are genuinely unusual:

| Feature | What it means |
|---|---|
| **Data provenance** | every record's full path through the flow is recorded and replayable — where it came from, what changed it, where it went |
| Back pressure | queues between processors, so a slow sink slows the source instead of dropping data |
| Prioritisation | which records move first when the queue is full |
| Visual flow | the pipeline is a diagram, and the diagram is the runtime |

Provenance is the one nothing else here offers. For regulated environments — proving what
happened to a specific record — that is a capability rather than a convenience.

## When to use it

- **routing and mediation** between many heterogeneous systems, not loading a warehouse
- provenance and auditability are requirements
- edge or IoT collection, where NiFi (and MiNiFi) are commonly used
- flows must be operated by people who are not writing code

## When not to use it

- straightforward EL into a warehouse — [Airbyte](../airbyte/README.md) or [SeaTunnel](../seatunnel/README.md) are the right shape
- **transformation logic belongs in Git**. This is the real risk: it is easy to build business logic in the canvas, where it is not reviewable, not testable, and understood only by whoever drew it

## The warning that matters

NiFi's power is what makes it dangerous in an ELT platform. Because transformation is a
first-class feature, logic migrates into the flow — and then the answer to "why is this number
wrong" is a diagram someone drew two years ago.

If it is used here, the discipline is the same as everywhere else in
[`integration/`](../README.md): **land raw, transform in
[SQL](../../transform/README.md)**. NiFi moves and routes; it does not decide what the data
means.

---

[← Integration](../README.md)
