[← API](../README.md)

# gRPC

<https://github.com/protocolbuffers/protobuf>

---

## The problem it solves

Two services in different languages need to call each other, and JSON over HTTP gives them no
agreement about what the fields are called, what types they hold, or which ones are required.
The contract lives in a wiki page and diverges from both implementations.

gRPC makes the contract the source code. A `.proto` file declares the messages and the methods,
and the client and server stubs are **generated** from it in every supported language:

```protobuf
service Users {
  rpc GetUser(GetUserRequest) returns (User);
}
```

Three things follow from that, and they are the reasons to choose it:

- **The contract cannot drift.** Both sides are generated from the same file, so a mismatch is a
  build failure rather than a runtime surprise.
- **Protobuf is binary and small.** Field names are not transmitted — field numbers are — so
  payloads are considerably smaller than the equivalent JSON, and parsing is cheaper.
- **HTTP/2 gives it streaming and multiplexing.** Client streaming, server streaming and
  bidirectional streaming are part of the model, not an extension bolted on.

**[Protocol Buffers](https://github.com/protocolbuffers/protobuf)**, the reference recorded here,
is the serialisation format underneath. It is worth separating in your head: Protobuf is a schema
and encoding, usable entirely on its own — for Kafka messages, for stored records, for anything
where a typed schema matters. gRPC is the RPC framework built on top of it. Choosing Protobuf does
not commit you to gRPC.

## When to use it

- **service-to-service calls inside the cluster**, especially across languages
- a strict typed contract is wanted and code generation is acceptable in the build
- payload size or serialisation cost is measurable — high call volumes, large messages
- **streaming** in either or both directions is part of the interaction
- the schema needs to evolve safely: adding fields is backward-compatible by design, as long as
  field numbers are never reused

## When not to use it

- **browsers.** A browser cannot speak gRPC directly. gRPC-Web plus a proxy exists, and it is a
  real cost with real limitations
- **public or partner APIs.** Consumers expect JSON they can `curl`; handing them a `.proto` and a
  code generator is a support burden you inherit
- debugging by hand matters. A binary payload cannot be read from a log or a packet capture without
  the schema
- the traffic is low and the team is small. The build-time code generation and the toolchain are
  overhead that a JSON endpoint does not have
- the edge cannot do L7 HTTP/2 — see below, this is not a small problem

## Notes

The original note recorded **Protocol Buffers** only; nothing is deployed in this folder.

The operational issue to understand before it is, because it is the one that reliably surprises
people:

**gRPC does not balance across pods behind an L4 load balancer.** gRPC opens a single long-lived
HTTP/2 connection and multiplexes every call over it. A load balancer working at the connection
level therefore makes one decision, at connect time, and every subsequent request from that client
lands on the same pod. With a plain Kubernetes `Service` — which balances connections, not
requests — a client will pin itself to one replica and stay there.

The symptom is one pod at high CPU while the rest idle, and it is invisible in staging with a
single client and three pods. What is needed is a proxy that balances **individual HTTP/2 streams**
— an L7 ingress that understands gRPC, or a service mesh sidecar. This is a
[`network/`](../../../network/README.md) decision, and it has to be made before gRPC is adopted
rather than after the traffic arrives.

The other thing worth writing down early is **schema evolution discipline**: field numbers are the
identity of a field on the wire. Adding a new field with a new number is safe. Renaming a field is
safe. **Reusing the number of a deleted field is a silent data-corruption bug**, because old
clients will decode the new field as the old one. Protobuf provides `reserved` for exactly this,
and using it is not optional in a schema more than one team depends on.

---

[← API](../README.md)
