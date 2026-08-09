[← Traffic analyzer](../README.md)

# Kubeshark

<https://github.com/kubeshark/kubeshark>

Context and comparison: [../README.md](../README.md)

---

## The problem it solves

`tcpdump` gives you packets. Kubeshark gives you **protocol-aware flows across the whole
cluster** — HTTP requests with their headers and bodies, gRPC calls, DNS queries, Kafka and
Redis traffic — presented in a UI, without having to guess which pod on which node to attach
to first.

Often described as Wireshark for Kubernetes, which is close enough: capture across every
node, then filter and read.

## When to use it

- an investigation where the [troubleshooting method](../../troubleshooting/README.md) has narrowed things down and you now need to see the **payload**
- mapping undocumented calls — what is this service actually talking to?
- debugging behaviour that only shows up between services, not inside one

## When not to use it

- **as a permanent installation.** It observes real traffic including credentials and
  personal data, costs CPU and memory on every node, and is an obvious target. Turn it on
  for an investigation and off afterwards
- when [Cilium](../../cni/cilium/README.md) is already the CNI — **Hubble** covers much of this with
  nothing extra to install
- as a first step; most problems are DNS, endpoints or policy and never reach the wire

## Licensing caveat

> The open-source version is **heavily limited** and pushes constantly toward the paid tier,
> which makes it tiring to use.

Worth knowing before investing time in it. If the goal is flow visibility rather than full
payload inspection, Hubble or the service mesh telemetry already in this repo will likely
get you further with less friction.

---

[← Traffic analyzer](../README.md)
