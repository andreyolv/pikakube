[← API](../README.md)

# SOAP

No project references were recorded for this folder.

---

## The problem it solves

Nothing you have. SOAP is here because it is still running somewhere you will have to integrate
with — banks, payment processors, government services, telecom provisioning, ERP systems and
anything built on a mid-2000s enterprise Java or .NET stack.

What it solved when it was designed is worth understanding, because it explains why the systems
that use it have not moved:

| Concern | SOAP's answer |
|---|---|
| Contract | **WSDL** — a machine-readable service description, from which clients are generated |
| Types | XML Schema, with real types and validation |
| Message signing and encryption | WS-Security, **per message** rather than per connection |
| Transactions across services | WS-AtomicTransaction |
| Guaranteed delivery | WS-ReliableMessaging |
| Transport | not only HTTP — SMTP and JMS were in scope |

The WSDL row is the one that has aged well and was ahead of its time: a generated, typed client
from a published contract was standard in SOAP a decade before OpenAPI made it normal for
[REST](../rest/README.md).

The rest is why it lost. The WS-\* stack is enormous, implementations disagreed about the parts
that mattered, and message-level security is far heavier than TLS plus a token for the vast
majority of services. XML envelopes are verbose, XML parsers have a long history of vulnerabilities,
and none of it is debuggable with `curl`.

## When to use it

- **the counterparty requires it.** This is the only reason
- an existing enterprise estate already standardised on it, and the integration is one endpoint in
  a system that is not being rewritten
- per-message signing or encryption is a contractual requirement rather than a preference — this is
  the one capability REST has no direct equivalent for, and it is why some regulated integrations
  stay on SOAP

## When not to use it

- **any new service.** There is no scenario where a greenfield internal API is better in SOAP than
  in [REST](../rest/README.md) or [gRPC](../grpc/README.md)
- anything a browser or a JavaScript client will call directly
- anything where payload size or parse cost matters — XML envelopes are large and expensive
- as a way to get a typed contract. [gRPC](../grpc/README.md) and OpenAPI give you that without the
  WS-\* stack

## Notes

**The original note in this folder was empty.** The file existed with no content, which is itself
the record: the protocol was catalogued deliberately so the taxonomy under [`api/`](../README.md)
would be complete, and then nothing was evaluated — because there was nothing to evaluate. No SOAP
integration exists in this platform, and none is planned.

That is the correct outcome, and the folder is kept for the same reason the empty note was: when a
SOAP integration does appear, it will arrive as a requirement from outside rather than as a choice,
and there should be somewhere obvious to put what is learned about it.

Two practical points for when that happens:

**Do not hand-write the client.** The WSDL exists to generate one. Constructing XML envelopes by
string manipulation is how integrations acquire encoding and namespace bugs that appear months
later on an unusual character.

**Turn off XML external entity resolution.** XXE — where a parser is persuaded to fetch a local
file or an internal URL through a document's entity declarations — is the classic SOAP
vulnerability, and most XML parsers were historically permissive by default. This is the single
security control to verify before a SOAP endpoint is exposed to anything.

---

[← API](../README.md)
