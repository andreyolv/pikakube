[← Exporters](../README.md)

# Blackbox Exporter

<https://github.com/prometheus/blackbox_exporter>

---

## The problem it solves

Every other exporter reads metrics from something. This one **probes** — it makes a request
and reports whether it worked, how long it took, and what came back.

Supported probes: HTTP and HTTPS, TCP, ICMP, DNS and gRPC.

It is the difference between "the pod is running" and "the endpoint answers". Those are not
the same statement, and only the second is what a user experiences.

## When to use it

- synthetic monitoring of endpoints, internal or external
- **certificate expiry** — it exposes the remaining validity of a TLS certificate as a metric, which is the simplest possible way to never be surprised by an expired certificate
- checking dependencies you do not own: a partner API, a managed database, a payment gateway
- DNS resolution as an explicit check

## When not to use it

- as a substitute for instrumenting the application. A probe says the endpoint answered, not that it answered correctly for real users
- probing every service every few seconds; it is a real request, and each one costs the target something

## The Kubernetes-specific version

For the specific question "can every node reach every other node", the
[kubenurse](../../../../network/monitoring/kubenurse/README.md) tool builds a node-to-node matrix. Both
follow the same principle — **generate traffic to find out** — at different granularity.

## Certificate expiry, concretely

`probe_ssl_earliest_cert_expiry` is a timestamp, so an alert on it is a subtraction. It costs
one probe and removes an entire category of outage — worth setting up on day one, and often
forgotten until it fires the hard way.

See [certificates](../../../../security/2-cluster/certificates/README.md).

---

[← Exporters](../README.md)
