[← Privileged access](../README.md)

# Teleport

<https://github.com/gravitational/teleport>

---

## The problem it solves

Teleport replaces the pile of long-lived credentials described in [`../README.md`](../README.md)
with a single **identity-aware access plane**. Engineers authenticate once, with the
organisation's SSO and MFA, and receive short-lived certificates for whatever they are permitted
to reach.

The architectural decision that makes it work is that Teleport runs **its own certificate
authority**. It does not proxy passwords or forward keys — it issues a certificate, valid for
hours, carrying the user's identity and roles inside it. Each protocol gets the certificate form
it already understands:

| Protocol | What Teleport issues and does |
|---|---|
| **SSH** | OpenSSH certificates. Hosts trust Teleport's CA, so `authorized_keys` stops being an inventory to maintain |
| **Kubernetes** | acts as a Kubernetes API proxy. It presents a client certificate on the user's behalf, maps Teleport roles to Kubernetes users and groups, and records `kubectl exec` sessions |
| **Databases** | Postgres, MySQL, MongoDB and others, with client certificates and per-session query logging |
| **Web applications** | an identity-aware proxy for internal HTTP apps |
| **Desktops** | RDP with screen recording |

Because Teleport terminates and understands each protocol rather than merely tunnelling bytes,
it can do three things a generic broker cannot:

- **Record sessions in a replayable form.** A terminal session plays back exactly as it looked.
- **Enforce policy inside the protocol.** Which Kubernetes namespaces, which database users,
  which SSH logins — not just "may connect".
- **Attribute every action.** Every Kubernetes API call through the proxy carries the human's
  identity, so the cluster audit log names a person rather than a shared certificate.

On top of that sits the RBAC and workflow layer: roles that map SSO groups to permitted
resources and logins, and **Access Requests** — the just-in-time elevation described in
[`../README.md`](../README.md) §4, with approval in the UI or through a chat integration.

Session recording, SSO for the enterprise edition, Access Requests and per-session audit are
split across editions, and which features are open-source has shifted over time. Check the
current edition matrix against your actual requirement before committing — this is the most
common source of disappointment with it.

## When to use it

- **Kubernetes access by humans, with attribution and recording.** This is Teleport's strongest
  case and the one most relevant here: it is the only tool in this folder that makes the cluster
  audit log say *who*, and that records what happened inside `kubectl exec`.
- **A fleet of SSH hosts.** Certificate-based SSH with central policy removes `authorized_keys`
  management entirely.
- **Database access must be audited per query and per person.** Shared database credentials in a
  password manager are the alternative, and it is a bad one.
- **A compliance requirement for session recording.** SOC 2, PCI and similar frameworks ask for
  exactly this, and reproducing it by hand is a project.
- **You want just-in-time elevation** with a real approval workflow rather than standing admin.
- **Access spans several protocols** and you want one policy model and one audit store across
  all of them.

## When not to use it

- **A small environment.** It is a certificate authority, a proxy, an auth service and an audit
  store. That is a substantial system, and below a certain size it costs more attention than the
  risk it removes.
- **Only HTTP dashboards need protecting.** [`auth-proxy/`](../../auth-proxy/README.md) is far
  lighter and sufficient.
- **You cannot make it highly available.** It becomes the only path to everything; a single
  replica means a restart locks the organisation out. This is not a component to run casually.
- **The feature you need is in a different edition.** Verify before designing around it.
- **A handful of SSH hosts and nothing else.** SSH certificates from
  [step-ca](../../../../certificates/step-ca/README.md) plus SSO give expiry and central revocation
  for a fraction of the operational weight.
- **Air-gapped or heavily constrained environments**, where the licensing, update and telemetry
  story needs checking carefully first.

## Notes

**`https://github.com/gravitational/teleport`** — the project. Go, from Gravitational (now
Teleport, the company). Open-source core with commercial editions layered on top.

What is staged in this folder: a `HelmRepository`, a `Namespace` `teleport`, and a `HelmRelease`.

| Setting | What it means |
|---|---|
| chart `teleport-cluster`, version `15.2.2` | the **cluster** chart — the Teleport control plane: auth service, proxy and web UI. This is the right chart for running Teleport itself |
| `clusterName: teleport-cluster` | the cluster's identity. It is baked into the certificate authority and into every issued certificate, and **changing it later is disruptive** — it invalidates trust relationships. Worth choosing a real, stable name rather than the placeholder |
| `service.type: ClusterIP` | not externally reachable. Fine for a local cluster; a real deployment needs a LoadBalancer or an ingress, and Teleport's proxy has particular requirements around TLS and SNI because it multiplexes several protocols on one port |

Two notes on what a working deployment would still need, since the staged values stop here:

- **Storage.** Teleport's auth service needs a backend for cluster state, and the audit and
  session recording store needs somewhere durable. On a local cluster that is a PVC; in the
  cloud it is typically object storage plus a database. Session recordings grow quickly, and
  retention should be decided before they start accumulating.
- **The certificate authority is the crown jewel.** Teleport's CA keys are what grant access to
  everything it fronts. They need backup, and they need the same custody care as any CA key —
  the reasoning is in [`certificates/README.md`](../../../../certificates/README.md).

There is a second chart worth knowing about, referenced in the manifest's own comment link:
`teleport-kube-agent`. That one runs *inside* a cluster you want to expose **to** an existing
Teleport control plane, rather than running the control plane itself. Confusing the two charts
is a common early mistake — `teleport-cluster` is the server, `teleport-kube-agent` is the
thing that joins a resource to it.

---

[← Privileged access](../README.md)
