[← Configuration management](../README.md)

# Salt

<https://github.com/saltstack/salt>

---

## The problem it solves

Salt does configuration management like the others, but its real differentiator was never the
configuration part — it was the **event bus and the speed**.

| Component | What it is |
|---|---|
| Salt master / minions | agent-based, with a persistent message-bus connection rather than per-run SSH |
| States (`.sls`) | desired state, in YAML with Jinja templating |
| Grains and Pillar | facts about the minion; secret and per-minion data pushed from the master |
| Salt Reactor | run actions **in response to events on the bus** |
| `salt-ssh` | an agentless mode, for when installing a minion is not possible |

Because minions hold an open connection, a command against ten thousand hosts returns in seconds
rather than minutes. Salt is genuinely the fastest of the classic tools at fleet-wide execution,
and remote execution — not convergence — is what most people used it for.

The Reactor is the conceptually interesting piece: an event happens somewhere in the fleet, and
Salt runs something in response. That is the same shape as
[`event-driven/`](../../event-driven/README.md) in this discipline, built for servers.

## When to use it

- **fleet-wide remote execution at scale**, where the requirement is "run this against everything,
  now, and tell me what happened" — Salt is still very good at this
- existing Salt estates, especially large ones
- event-driven server automation via the Reactor, where an external system needs to trigger work on
  hosts

## When not to use it

- **for a new Kubernetes platform.** Same reasoning as the rest of this folder: the model is built
  for mutable long-lived servers
- if the master's security posture cannot be taken seriously. See below
- if a simple, agentless, low-ceremony tool is enough — [Ansible](../ansible/README.md) or
  [pyinfra](../pyinfra/README.md) require no master and no minions

## Notes

The only recorded reference is the repository: <https://github.com/saltstack/salt>.

**The security history matters and should not be glossed over.** In 2020 two vulnerabilities in the
Salt master's authentication and command handling were disclosed and then mass-exploited within
days, because a large number of Salt masters were reachable from the internet. A Salt master is,
by design, a service that can execute arbitrary commands as root on every machine that talks to it.
That is a much larger blast radius than an SSH-based push tool, and it means the master's exposure
is a first-order design decision, not an operational detail.

**Ownership** has also moved: SaltStack was acquired by VMware, which was subsequently acquired by
Broadcom. The Salt Project remains open source under Apache 2.0, but the corporate backing has been
through two transitions in five years, and the community activity reflects that.

Mapped for completeness alongside Ansible, Chef and Puppet. Of the four, Salt's Reactor is the idea
most worth carrying forward conceptually — the pattern reappears, done better and inside the
cluster, in [`event-driven/`](../../event-driven/README.md).

---

[← Configuration management](../README.md)
