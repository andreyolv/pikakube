[← Configuration management](../README.md)

# Puppet

<https://github.com/puppetlabs/puppet>

---

## The problem it solves

Puppet is the other agent-based, pull-based answer to configuration drift, and the oldest of the
tools in this folder. Its distinguishing idea is a **declarative resource model with an explicit
dependency graph**:

| Concept | What it is |
|---|---|
| Manifest | desired state in Puppet's own declarative language (not a general-purpose one) |
| Resource | an abstract thing — a package, a file, a service — with a provider per platform |
| Catalog | the compiled, node-specific graph the agent applies |
| Facter | facts gathered from the node and fed back into compilation |

You declare resources and the relationships between them (`require`, `before`, `notify`), and
Puppet computes the order. You do not write the order yourself. That is genuinely different from a
sequential playbook, and it is why Puppet manifests describe *state* more purely than Ansible's do.

The agent runs on a schedule and converges, so — like [Chef](../chef/README.md) — drift is
corrected continuously rather than at the moment somebody runs a command.

## When to use it

- **there is an existing Puppet estate**, particularly a large one. The resource abstraction holds
  up well across heterogeneous operating systems
- fleets where continuous convergence and reporting on compliance state are required
- environments with a long-standing investment in Puppet Forge modules

## When not to use it

- **for a new Kubernetes platform**, for the same reason as Chef: the thing it does well is
  managing mutable servers, and a Kubernetes platform tries not to have any
- if the declarative language is a barrier. Puppet's DSL is neither YAML nor a general-purpose
  language, and it has to be learned as its own thing
- for orchestration. Puppet describes the state of one node; coordinating a sequence across many
  nodes is not what the model is for

## Notes

The only recorded reference is the repository: <https://github.com/puppetlabs/puppet>.

**Like Chef, Puppet has receded**, and the ownership history is the reason to be cautious rather
than the technology. Puppet was acquired by Perforce, and in 2025 Perforce announced changes to how
open source Puppet is developed — moving day-to-day development out of the public repository and
publishing source releases instead. The community response was a fork, **OpenVox**, maintained by
Vox Pupuli, which now carries the open-source continuation of the ecosystem's modules and tooling.

The practical consequence for anyone reading this folder: "Puppet" is no longer one unambiguous
thing. There is Puppet Enterprise, there is what Perforce publishes as open source, and there is
OpenVox. That fragmentation is a good reason not to start here, independent of the merits of the
tool.

Mapped for completeness. The argument for why none of the four classic tools in this folder is how
you configure a Kubernetes platform is in [`../README.md`](../README.md).

---

[← Configuration management](../README.md)
