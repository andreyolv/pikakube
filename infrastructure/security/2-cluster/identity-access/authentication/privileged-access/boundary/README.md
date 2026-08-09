[← Privileged access](../README.md)

# HashiCorp Boundary

<https://github.com/hashicorp/boundary>

---

## The problem it solves

Boundary brokers access to infrastructure without giving anyone network access to it, and
without anyone holding the target's credentials.

The design is deliberately narrower than [Teleport](../teleport/README.md), and the narrowness
is the point: Boundary authenticates and authorises, then **brokers a session**. It does not
try to understand every protocol it carries.

The pieces:

| Concept | What it is |
|---|---|
| **Controller** | authentication, authorisation and session management — the brain |
| **Worker** | the data plane; it sits near the target and proxies the connection. Workers can live inside private networks the user cannot reach |
| **Host catalog / host set** | targets, discovered **dynamically** from AWS, Azure, GCP or Vault rather than maintained by hand |
| **Target** | a host set plus a port plus a policy |
| **Credential library** | where the target's credentials come from — normally **Vault**, which generates them per session |

The two properties that distinguish it:

**Identity-based access with no network access.** The user never receives a route to the target.
The Boundary client opens a local listener, and the worker relays. The target's network stays
closed, which makes it a genuine replacement for "put everyone on the VPN" rather than an
addition to it.

**Credentials are brokered, not held.** With Vault behind it, Boundary requests a *dynamically
generated* credential for each session — a Postgres user created for that session and revoked
when it ends, for instance. Nobody ever knows the password, because the password did not exist
before the session and does not exist after it. That is the strongest form of the principle in
[`../README.md`](../README.md), and it is Boundary's best argument.

**Dynamic host catalogues** matter more than they sound: in an autoscaling environment, targets
appear and disappear constantly, and a tool that requires a maintained inventory is always
wrong. Boundary discovers them from the cloud provider's API.

## When to use it

- **You already run Vault.** This is by far the strongest reason. Boundary plus Vault gives
  per-session, dynamically generated, automatically revoked credentials for databases and hosts,
  and the integration is first-class rather than bolted on.
- **The HashiCorp stack is the platform's spine** — Terraform, Vault, Consul, Nomad. Boundary is
  consistent with all of it: same identity model, same Terraform provider, same operational
  idioms.
- **Targets are dynamic.** Autoscaling groups and ephemeral instances, discovered from the cloud
  API rather than tracked in a list.
- **You want to remove the VPN as the access mechanism.** Boundary gives per-resource access
  without network reachability, which is the actual thing a VPN gets used for and does badly.
- **The requirement is "stop distributing credentials", not "record everything".** If audit
  recording is not the driver, Boundary's smaller surface is an advantage.

## When not to use it

- **Session recording is a hard requirement.** This is the decisive limitation. Recording in
  Boundary is a commercial feature and, even then, less deep than Teleport's — where terminal
  replay and per-session Kubernetes and database audit are core. If the driver is compliance
  evidence of *what was done*, Teleport is the answer.
- **Kubernetes access is the main use case.** Boundary brokers a TCP connection to the API
  endpoint. Teleport proxies the Kubernetes API itself, maps identities into cluster RBAC, and
  records `exec` sessions. Very different depth for this specific case — which is the one that
  matters most on a Kubernetes platform.
- **You do not run Vault.** Much of the value is the credential brokering, and without Vault you
  are left with a connection broker whose main benefit is network isolation.
- **You want deep per-protocol policy** — which SSH login, which database user, which namespace.
  Boundary's protocol awareness is thinner by design.
- **Small environments.** A controller, workers, a database and Vault is a lot of machinery for
  a handful of targets.

## Notes

**`https://github.com/hashicorp/boundary`** — the project, and the only note recorded for this
folder. Go, and since 2023 under HashiCorp's Business Source License rather than MPL, which is
worth checking against your own policy before adopting it — the same licence change that
affected Terraform and Vault.

**No manifests are staged here.** Unlike [Teleport](../teleport/README.md), which has a
HelmRelease and a namespace, this folder contained only the link. The accurate status is that
Boundary was catalogued as an alternative and not taken further.

Three things worth knowing if it ever is:

- **It needs Postgres.** The controller stores all its state there, and it is not optional.
- **Worker placement is the design decision.** Workers are what make private targets reachable
  without the user having network access, so where they run *is* the network architecture.
  Getting this right is most of the deployment.
- **Everything is Terraform-able**, and in a HashiCorp-centric environment that is how it is
  meant to be managed. In a Flux-based GitOps repository like this one, that is a second
  configuration mechanism to reconcile with the first — worth deciding deliberately rather than
  discovering later.

For this platform the conclusion in [`../README.md`](../README.md) applies: there are no SSH
hosts, no fleet, no Vault, and one operator. Neither broker has a problem to solve here. The
transferable idea — short-lived credentials issued against a verified identity instead of
long-lived credentials held at endpoints — is the same one that
[`workload-identity/`](../../workload-identity/README.md) makes for workloads, where it does
apply.

---

[← Privileged access](../README.md)
