[← Configuration management](../README.md)

# pyinfra

<https://github.com/pyinfra-dev/pyinfra>

---

## The problem it solves

Ansible's YAML stops being a good idea at about the point where a playbook needs a loop with a
condition inside it. What follows is Jinja embedded in YAML embedded in more YAML, and a file that
is neither readable data nor readable code.

pyinfra takes the other branch: **the deploy script is Python.** Operations are Python function
calls, control flow is Python control flow, and there is no DSL to learn on top of a language you
already know.

```
from pyinfra.operations import apt, files, systemd
```

The rest of the design is deliberately close to Ansible's, because that part was right:

| Property | Detail |
|---|---|
| **Agentless** | SSH, like Ansible — nothing installed on the target |
| **Idempotent operations** | each operation inspects current state and emits only the commands needed |
| **Two-phase execution** | it builds the full command list first, then runs it — which makes `--dry` a genuine plan, not a guess |
| **Fast** | connections and fact gathering run in parallel; it is noticeably quicker than Ansible on the same inventory |
| **Multiple connectors** | SSH, local, Docker, and others — the same script can configure a container or a host |

The two-phase model is the underrated part. Because the commands are computed before anything runs,
a dry run shows exactly what would be executed, per host, which is the thing push-based tools
usually cannot tell you.

## When to use it

- **the team writes Python** and the YAML-plus-Jinja tax is being paid daily
- provisioning that needs real logic — branching on facts, computing values, reusing functions
- fast, ad-hoc fleet operations where iteration speed matters
- building or configuring images and containers as well as hosts, using the non-SSH connectors
- as the modern alternative when the choice is being made fresh rather than inherited

## When not to use it

- when the **ecosystem** is the deciding factor. Ansible's collection and module coverage — network
  vendors, cloud providers, appliances, databases — is far larger, and for those targets it is not
  close
- if the operators are not programmers. YAML has a real advantage: it is hard to write something
  clever in it, and sometimes that is the point
- if continuous reconciliation is required. Like Ansible, pyinfra runs when you run it and knows
  nothing between runs
- **to configure workloads inside Kubernetes** — the same prohibition that applies to every tool in
  this folder

## Notes

The only recorded reference is the repository: <https://github.com/pyinfra-dev/pyinfra>.

pyinfra is **the interesting one in this folder**, and the only one here that is a reasonable
choice for a greenfield project today. Ansible, Chef, Puppet and Salt are all mapped as history and
as the pre-Kubernetes answer; pyinfra is mapped because it is a live, well-designed tool solving the
same problem with fewer layers.

The comparison that matters is against Ansible, since they occupy the same architectural position —
agentless, push, SSH:

| | Ansible | pyinfra |
|---|---|---|
| Deploy definition | YAML + Jinja | Python |
| Ecosystem | very large | small |
| Speed | adequate | noticeably faster |
| Dry run | best-effort `--check` | a real, computed command plan |
| Who it suits | operations teams | engineers who already write Python |

For a pikakube-shaped platform — Python-heavy, with a small number of nodes to bootstrap — pyinfra
is the better fit on every axis except ecosystem, and ecosystem is exactly the axis that decides it
when the targets are network devices or cloud APIs rather than Linux hosts.

---

[← Configuration management](../README.md)
