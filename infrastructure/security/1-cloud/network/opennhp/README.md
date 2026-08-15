[← Cloud network](../README.md)

# OpenNHP

<https://github.com/OpenNHP/opennhp>

Making a service **unreachable until the requester has authenticated** — so that scanning,
fingerprinting and pre-authentication exploits have nothing to talk to. The open reference
implementation of network hiding, and the page where the ZTNA/SDP category is covered.

---

## 1. The gap the other four categories leave

Every control in [`../README.md`](../README.md#3-the-categories) assumes the connection
happens. A [WAF](../waf/README.md) inspects a request that arrived; an [IPS](../ips/README.md)
inspects packets in flight; an [NGFW](../ngfw/README.md) decides by address and port; a
[VPN](../vpn/README.md) grants reachability to a network and then trusts what is behind it.

What none of them changes is the first fact an attacker relies on: **a listening port answers
anyone.** The TCP handshake completes, the TLS certificate is presented, the login page renders, the
SSH banner names the version — all of it before any identity has been established. Everything that
follows from that is familiar:

- the service is **discoverable**, by anyone scanning the address space
- the **pre-authentication attack surface** is exposed — every parser reachable before login, which
  is where the memorable CVEs live
- credential stuffing, brute force and denial of service all have a target
- the version banner tells an attacker which exploit to try

The answer this category proposes is older than it sounds: **authenticate first, then open the
port.** The service is behind a default-drop rule; a would-be client proves who it is over a
separate channel; only then is a path opened, for that source, to that resource.

Two families implement the idea. **Identity-aware proxies** — Cloudflare Access, Teleport,
Pomerium, Tailscale's ACLs — terminate the connection at a broker that authenticates the user and
then forwards; the resource is never publicly addressable because only the broker can reach it.
**Single Packet Authorization** keeps the resource where it is and hides it behind a firewall that
opens on a cryptographically authenticated knock. OpenNHP is the second kind.

## 2. OpenNHP

The lineage matters, because "port knocking" has a deservedly poor reputation and this is three
generations past it:

| Generation | Mechanism | Weakness |
|---|---|---|
| **Port knocking** | a sequence of connection attempts to closed ports | trivially replayed, observable, no identity |
| **Single Packet Authorization** (fwknop) | one encrypted, authenticated packet carrying a request | better, but a static shared secret and a thin identity model |
| **NHP** | a cryptographic protocol with identity, key agreement and a separate control plane | — |

OpenNHP is the reference implementation of the **Network-infrastructure Hiding Protocol**, published
through the Cloud Security Alliance, whose earlier work produced the Software Defined Perimeter
model. It is written in Go, Apache-2.0.

Three components, and the separation is the design:

| Component | Role |
|---|---|
| **Agent** | on the client; sends the encrypted knock |
| **Server** | the control plane; validates identity and decides |
| **AC** (access control gateway) | sits at the resource; enforces default-drop and opens a path when told to |

The flow is short: the agent knocks; the server authenticates the request and instructs the AC; the
AC opens the firewall for that specific source; the server tells the agent where to go; the agent
connects. Until the first step succeeds, the AC drops everything — **the port does not answer, and
nothing distinguishes the host from one that does not exist.** The protected resource's DNS name, IP
and port are all hidden simultaneously, and because the server holds no per-connection state the
control plane scales horizontally.

Cryptography is built on the **Noise protocol framework**, with two interchangeable suites:
Curve25519 + AES-256-GCM + BLAKE2s, or SM2 + SM4-GCM + SM3. An identity-based mode with a key
generation centre is also available. The SM suite is the Chinese national cryptographic standard set,
which is a useful signal about where the project's institutional interest comes from — its sponsors
include Tencent Cloud — and is not, by itself, a criticism.

## 3. When this is worth it

- **administrative access to infrastructure** — SSH, RDP, jump hosts, admin panels, a Kubernetes API
  server that must be reachable from outside. High-value, non-public, and exactly the surface that
  gets scanned
- services with a **pre-authentication history** — VPN concentrators and management interfaces are
  where the worst CVEs of the last decade have landed, and hiding the listener removes the class,
  not the instance
- **denial of service resistance** for a non-public service: traffic from an unauthenticated source
  is dropped at the gateway rather than handled by the application
- when the alternative on the table is *"open it to the office IP range"*, which is a rule that
  outlives the office, the range and the reason
- as a **layer over** a VPN rather than instead of it — closing the flat-network problem described in
  [`../vpn/README.md`](../vpn/README.md#1-a-vpn-is-reachability-not-security), where one credential
  yields reachability to everything

## 4. When it is not

- **anything genuinely public.** A website that hides from users is a website that is down. This
  category is for services with a known, enrolled population of clients
- **every client needs the agent.** That is the adoption cost and it is the reason most SDP
  deployments stall: contractors, mobile devices, CI runners and third-party integrations each need
  provisioning, and anything that cannot run an agent needs an exception — which is a hole in the
  control
- **the exposure is HTTP and the users are people.** An identity-aware proxy does the same job
  through a browser with no client software, integrated with the identity provider you already run.
  For most organisations this is the pragmatic answer and SPA is over-engineering
- **it is a niche protocol.** Adopting one at the network edge means your access path depends on a
  project few operate at scale, with no second implementation to fall back to. Weigh that against
  WireGuard, which is boring, ubiquitous and already delivers *unreachable-unless-authenticated* for
  most threat models
- **it authenticates nothing inside the service.** Hiding the listener is not authorisation; the
  application still needs its own identity, and a compromised enrolled client still gets in.
  Removing pre-auth exposure is a real and narrow win — treat it as such
- **the knock server becomes the target.** You have not removed the internet-facing component, you
  have replaced several with one. That one is small and purpose-built, which is the point, but it is
  now the thing whose CVEs matter most

## 5. Anti-patterns

| Anti-pattern | Why it is bad | Instead |
|---|---|---|
| Treating hiding as authentication | an enrolled client is still whoever is holding it | keep application authn/authz unchanged |
| Hiding a service and skipping patching | the listener is unreachable **until an agent is compromised** | patch; hiding buys time, not immunity |
| Rolling it out to public services | users cannot enrol; the service is simply broken | identity-aware proxy, or leave it public and defend it |
| One knock granting broad network access | that is a VPN with extra steps | per-resource authorisation, which is the whole point |
| No plan for agentless clients | exceptions accumulate until the default-drop is decorative | decide the exception path before deployment, not after |
| Deploying it instead of an identity provider integration | you now have a second identity system | it slots **alongside** IAM, DNS and policy engines — that is the project's own framing |

## 6. How this applies to pikakube

Nothing here implements this and nothing here should yet. The category is recorded because it names
a question this repository does answer in practice: **what is reachable from outside, and does it
answer to strangers?** On a [Kind](../../../../platform-engineering/kubernetes/README.md) cluster the
honest answer is *nothing*, which is the strongest form of network hiding available and requires no
protocol at all.

The value is in the sequence it implies for the day something does need remote access — the API
server, an ingress, a jump host. The order to try, cheapest first:

1. **Do not expose it.** Unreachable beats hidden.
2. **A WireGuard mesh** — Tailscale or Headscale, already discussed in
   [`../vpn/README.md`](../vpn/README.md#5-mesh-and-overlay-networks). No listener on the public
   internet, and boring technology.
3. **An identity-aware proxy** for HTTP services, tied to the identity provider in
   [`security/2-cluster/identity-access/`](../../../2-cluster/identity-access/README.md).
4. **SPA/NHP** for the remainder — non-HTTP, high-value, agent-capable clients — where the
   pre-authentication surface is the specific thing being removed.

OpenNHP is the open reference implementation to reach for at step 4, and step 4 is further away than
it looks.

---

[← Cloud network](../README.md)
