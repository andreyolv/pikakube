[← Log collectors](../README.md)

# Vector

<https://github.com/vectordotdev/vector>
<https://github.com/vectordotdev/helm-charts>

---

## The problem it solves

Log collector configuration formats are declarative and limited. Anything beyond "parse this,
drop that" becomes a chain of filters that is hard to read and harder to test.

Vector, written in Rust, gives you **VRL** — a real expression language for transforming
events. Reshaping payloads, conditional routing, enrichment from external data, redacting
fields: all of it is expressed as code rather than assembled from config primitives.

It also has a genuinely useful property the others lack: **`vector tap` and unit tests**, so a
transformation can be verified before it reaches production.

## When to use it

- transformation is a real requirement, not an afterthought
- **redaction** — stripping credentials or personal data from logs before they are stored, which is far easier to get right in VRL
- one agent for logs, metrics and traces
- routing the same stream to several destinations with different shapes

## When not to use it

- simple shipping with light filtering — [Fluent Bit](../fluent/fluent-bit/) is smaller and the more common choice
- you want the most widely deployed option with the most examples available

## Where it fits best

As the **aggregator** in an agent-plus-aggregator setup: Fluent Bit on every node doing the
cheap work, Vector in the middle doing the expensive transformation once, before storage.

That arrangement gets VRL's power without paying its cost on every node.

---

[← Log collectors](../README.md)
