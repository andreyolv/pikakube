[← API testing](../README.md)

# SoapUI

<https://github.com/SmartBear/soapui>

---

## The problem it solves

**SOAP, WSDL and WS-\*, which nothing else in this folder handles.**

SoapUI is not a fourth REST client. It is the tool for the protocol the other three effectively do
not support:

| Capability | Why the REST clients cannot do it |
|---|---|
| **WSDL import** | the service contract is an XML document that generates the whole request set |
| **XML schema validation** | responses are validated against XSD, not eyeballed |
| WS-Security | signing, encryption and the header ceremony around them |
| SOAP faults | a structured error model, not an HTTP status code |
| MTOM attachments | a SOAP-specific binary encoding |

Point it at a WSDL and it generates a request for every operation, with the correct envelope and
skeleton body. Doing the same by hand in a REST client means constructing SOAP envelopes as raw XML
strings, which is possible and is not a workflow anyone sustains.

It also does REST, and it has a test-suite model with assertions, data-driven runs and a Maven
plugin for CI. Those are useful; they are not why you would install it.

## When to use it

- **there is a SOAP service in the estate** — this is the tool, and effectively the only one
- validating responses against an **XSD**
- WS-Security, WS-Addressing, or anything else with `WS-` in the name
- an existing SoapUI project that already works — there is no reason to port it
- legacy integrations where the contract is a WSDL somebody sent you

## When not to use it

- **there is no SOAP anywhere** — then it is a heavy Java desktop application solving a problem you
  do not have; use [Bruno](../bruno/README.md)
- modern REST, GraphQL or gRPC workflows — the other three are better at all of them
- **load testing** — SmartBear sells a separate product for that; use
  [`load/`](../../load/README.md)
- as the general team API client

## Notes

The recorded note is <https://github.com/SmartBear/soapui> — open source, and maintained by
**SmartBear**, who also sell the commercial ReadyAPI built on the same foundation. The open-source
edition is what is meant here; some capabilities people associate with the name belong to the paid
product.

Its place in this folder is deliberate and narrow. It is not on the same axis as
[Bruno](../bruno/README.md), [Insomnia](../insomnia/README.md) and [Postman](../postman/README.md) —
those three are compared on storage model and collaboration, and SoapUI is compared on **protocol**.
The decision tree in [`api/`](../README.md) branches on SOAP first for exactly that reason.

Nothing is deployed for it here. It is a desktop application, with a Maven plugin or its own runner
for pipelines, and it stays on the map for one reason: if a WSDL turns up, none of the other three
will do anything useful with it.

---

[← API testing](../README.md)
