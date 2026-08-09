[← KubeArmor](../README.md)

# KubeArmor policies

Two policies, one `Audit` and one `Block`, both scoped to pods labelled `app: nginx`. Together they
demonstrate the whole model.

## Contents

1. [The two policies](#1-the-two-policies)
2. [Audit before Block](#2-audit-before-block)
3. [Selector scope is the blast radius](#3-selector-scope-is-the-blast-radius)
4. [Anti-patterns](#4-anti-patterns)
5. [How this applies to pikakube](#5-how-this-applies-to-pikakube)

---

## 1. The two policies

### `audit-etc-nginx-acess.yaml`

```yaml
selector:
  matchLabels:
    app: nginx
file:
  matchDirectories:
  - dir: /etc/nginx/
    recursive: true
action: Audit
```

Every file access anywhere under `/etc/nginx/` is logged. Nothing is blocked.

This is **file integrity monitoring** expressed as a policy. `/etc/nginx/` holds the server's
configuration; a running nginx reads it at startup and reload and has no reason to write to it. An
attacker who wants to add a reverse proxy to an internal service, or route traffic somewhere else,
edits exactly these files.

`recursive: true` matters: nginx configuration is conventionally split across `conf.d/`,
`sites-enabled/` and `snippets/`, so a non-recursive rule on the parent directory would miss where
the interesting files actually live.

The choice of `Audit` over `Block` here is right for a different reason than caution: nginx
legitimately *reads* this directory constantly, so blocking would break it immediately. What you want
is to see writes, and `Audit` gives you the events to build that narrower rule from.

Note the filename typo — `acess` rather than `access`. Cosmetic, and worth fixing before anyone greps
for it.

### `block-pkg-mgmt-tools-exec.yaml`

```yaml
selector:
  matchLabels:
    app: nginx
process:
  matchPaths:
  - path: /usr/bin/apt
  - path: /usr/bin/apt-get
action: Block
```

Pods labelled `app: nginx` may not execute `apt` or `apt-get`. The kernel refuses; the process never
starts.

This is the highest value-to-risk ratio policy available in this whole subtree. A running web server
has no legitimate reason to install packages, so the false-positive rate is essentially zero — and
installing tooling inside a compromised container is a standard post-exploitation step. The
demonstration recorded in [`../README.md`](../README.md) installs **masscan**, a mass port scanner,
which is precisely what this blocks.

Two things it does not cover, which is the honest limitation of path-based process rules:

- **Other package managers.** `apk`, `yum`, `dnf`, `pip`, `npm`, `curl | sh`. The policy names two
  binaries; an attacker with a shell has other options.
- **Other paths to the same binary.** A copied or statically-linked binary at a different path is a
  different `matchPaths` entry.

That is not an argument against the policy — blocking the easy path is worth doing — but it is an
argument for understanding it as raising cost, not as prevention. A `matchDirectories` rule on
`/usr/bin/` with an allow-list would be stronger and needs the workload's real behaviour to be known
first.

## 2. Audit before Block

The two policies here are the two halves of the correct rollout, and having one of each in the same
folder is instructive:

| | audit-etc-nginx-acess | block-pkg-mgmt-tools-exec |
|---|---|---|
| Behaviour is | not fully known — nginx reads config constantly | completely known — a web server never installs packages |
| Action | `Audit` | `Block` |
| Cost of a false positive | none | the process fails with a permission error |

The rule: **`Block` is justified when the false-positive rate is genuinely zero, not when the action
looks suspicious.** Everything else starts at `Audit`, and the audit events are what you build the
narrower rule from.

This sits inside the global default posture set in `../kubearmorconfig.yaml`, which is `audit` for
files, network and capabilities. That default means anything *not* covered by a policy is logged
rather than denied. Flipping it to `block` inverts the cluster to deny-by-default and would require
a complete allow-list for every workload first.

## 3. Selector scope is the blast radius

Both policies select on `matchLabels: app: nginx`, and both are `KubeArmorPolicy` — namespaced, so
they apply within whichever namespace they are created in.

Three things follow:

- **The label is the contract.** Anything carrying `app: nginx` in that namespace is subject to these
  rules, including workloads that have nothing to do with nginx. Label collisions are how a policy
  ends up applying somewhere nobody expected.
- **Removing the label removes the protection.** Anyone who can edit a Deployment's pod labels can
  opt out of the policy. That is worth knowing when reasoning about what this actually enforces.
- **Namespaced means per namespace.** A rule that should apply everywhere needs
  `KubeArmorClusterPolicy`, not copies of a `KubeArmorPolicy` in each namespace.

Neither file declares a namespace, so both land wherever they are applied. Combined with the fact
that nothing in the parent folder has a `kustomization.yaml`, these are applied by hand rather than
delivered by Flux.

## 4. Anti-patterns

| Anti-pattern | Why it is bad | What to do instead |
|---|---|---|
| `Block` on behaviour you have not observed | a permission error inside the app, and nothing in the logs says a security policy caused it | `Audit` first, build the rule from the events |
| A path-based process rule treated as prevention | `apk`, `pip`, and a copied binary all bypass it | understand it as raising cost; use directory allow-lists where behaviour is narrow |
| Non-recursive rules on config directories | the interesting files are in `conf.d/`, `sites-enabled/` | `recursive: true` |
| Generic label selectors | `app: nginx` catches anything that happens to use that label | specific, owned labels |
| Policies applied by hand | not in the delivery path, so they vanish on a cluster rebuild | add them to a kustomization |
| Flipping the global posture to `block` | everything without a complete allow-list breaks at once | per-workload policies, global default left at `audit` |
| Auditing a path the workload reads constantly | volume with no signal | audit writes; read-heavy paths need a narrower rule |
| No alerting on the audit events | file integrity monitoring nobody looks at | route KubeArmor events to the same place as everything else |

## 5. How this applies to pikakube

These two files are a demonstration, not a policy set — they target `app: nginx`, which is not a
workload this platform runs, and they are applied by hand.

Their value is as templates, and two of them generalise well to this platform:

**The package-manager block.** It applies to essentially every long-running service in the cluster.
Scoped as a `KubeArmorClusterPolicy` excluding the namespaces that legitimately install things at
runtime, it is close to a free control. The one caveat for a data platform is real: Airflow DAGs and
Spark jobs sometimes do install Python packages at runtime, so those namespaces need an exception —
and that exception is itself a finding worth raising, because runtime package installation in a
production data pipeline is a supply-chain hole.

**File integrity monitoring on config directories.** The nginx pattern generalises to any workload
whose configuration is mounted and should never be written by the workload itself.

What is missing before either of those is real: a decision about who reads the audit events. Nothing
in this repository routes KubeArmor's output anywhere — no `ServiceMonitor`, no relay consumer, no
alert path. Audit-mode policies with no reader are the same failure described in
[`../../README.md`](../../README.md#5-detection-without-response-is-a-dashboard).

And the prior question: [Falco](../../falco/README.md) is the agent that is actually built out in
this repository, with three companions and a real configuration. Running two kernel-hooking
DaemonSets is not something to do by accident. KubeArmor earns its place here as the *enforcement*
answer — the thing Falco structurally cannot do — and that is a decision to make explicitly rather
than by having both installed.

---

[← KubeArmor](../README.md)
