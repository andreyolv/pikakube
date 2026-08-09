[← API](../README.md)

# GraphQL

<https://github.com/strawberry-graphql/strawberry>

---

## The problem it solves

A frontend needs a user, their last five orders and the status of each. Over
[REST](../rest/README.md) that is either three round trips, or a bespoke
`/users/1/dashboard` endpoint built for one screen — and a new endpoint every time the screen
changes.

GraphQL inverts the direction: the server publishes a **typed graph** of what exists, and the
client asks for exactly the fields it needs in one request.

```graphql
{
  user(id: 1) {
    name
    orders(last: 5) { id status }
  }
}
```

Two consequences follow, and they are what actually decide whether it fits:

- The **schema is the contract by construction**. There is no equivalent of an OpenAPI file that
  can drift, because the schema is the thing the server executes against.
- The frontend stops waiting on the backend for endpoint changes. That is the real organisational
  argument for GraphQL, and it is more often the deciding one than payload size.

**[Strawberry](https://github.com/strawberry-graphql/strawberry)** is the Python implementation
recorded here. It builds the schema from **type hints and dataclass-style declarations** rather
than a separate schema definition file, so the Python types are the schema — the same approach
[FastAPI](../rest/framework/fastapi/README.md) takes for REST, applied to GraphQL. It supports
both sync and async execution.

## When to use it

- **several clients with different data needs** against the same backend — web, mobile, a partner
- a UI that aggregates data owned by more than one service, where the alternative is a per-screen
  endpoint
- the shape of the frontend changes faster than the backend can ship endpoints
- the field-level typing is genuinely wanted, and the team will maintain it

## When not to use it

- a **single client** consuming a single backend — the schema, the resolvers and the tooling buy
  nothing that REST does not already give you
- caching matters. Everything is one URL and one verb, so HTTP caching, CDNs and per-route rate
  limiting stop applying, and all of it moves into the application
- service-to-service calls inside the cluster — [gRPC](../grpc/README.md) is a better fit for a
  typed contract between services
- file upload and download, which need an extension rather than being natural
- the team cannot commit to depth and complexity limits — see below

## Notes

The original note recorded **Strawberry** as the Python implementation of interest, covered above.
Nothing is deployed in this folder.

Three things worth knowing before that changes, because each of them is a production problem that
REST does not have:

**The N+1 problem is the default, not an edge case.** A query asking for 50 orders and the customer
on each one runs one resolver per order unless something batches them, which is 51 database
queries from one HTTP request. The fix is a **dataloader** — a per-request batching and caching
layer — and it is not optional at any real size. It is the single most common reason a GraphQL API
performs worse than the REST endpoints it replaced.

**An unbounded query is a denial of service.** Because the client composes the query, a nested
selection can walk the graph in a loop and read enormous amounts of data in one request. Query
**depth limits**, **complexity scoring** and, for public APIs, persisted queries are the controls.
None of them are on by default.

**Observability changes shape.** Every request is `POST /graphql` returning `200`, including the
ones that failed — GraphQL reports errors in the response body rather than the status code. Latency
and error-rate dashboards keyed on route and status code become useless, and the instrumentation
has to move to the resolver level. This is worth deciding before deployment rather than after the
first incident that nothing alerted on.

---

[← API](../README.md)
