[← Configuration management](../README.md)

# Chef

<https://github.com/chef/chef>

---

## The problem it solves

The same problem as [Ansible](../ansible/README.md) — converging a long-lived server to a described
state — with the opposite architecture. Chef is **agent-based and pull-based**:

| Component | Role |
|---|---|
| Chef Infra Client | runs on every node, on a timer, and converges the node |
| Chef Infra Server | holds cookbooks, node attributes and the search index |
| Cookbooks and recipes | the desired state, written as a **Ruby DSL** |

Two properties follow from that, and they are the reason Chef existed at all:

- **Continuous reconciliation.** The client runs every thirty minutes whether or not anyone asked.
  Drift is corrected rather than merely discovered. This is the same idea Kubernetes controllers
  implement, arrived at a decade earlier and applied to servers
- **Real code.** Recipes are Ruby, not a templating language pretending to be a programming
  language. That makes complex logic straightforward and makes it very easy to write a cookbook
  nobody else can follow

## When to use it

- **there is an existing Chef estate.** That is the honest answer. Chef is competent at what it
  does, and organisations running it are not wrong to keep running it
- large fleets of mutable, long-lived servers where continuous convergence is genuinely required
  and immutable infrastructure is not on the table
- environments where the compliance story matters and Chef InSpec is already in use

## When not to use it

- **for a new Kubernetes platform.** There is no scenario where starting with Chef today is the
  right call for configuring a Kubernetes estate. Node bootstrapping is better served by
  [Ansible](../ansible/README.md) or an image-building pipeline; everything inside the cluster
  belongs to controllers
- if the team does not write Ruby. The DSL is the barrier to entry, and it is a real one
- for anything ephemeral. An agent that converges every thirty minutes is a poor fit for a node
  that lives for two days
- where the licensing situation is a problem — see below

## Notes

The only recorded reference is the repository: <https://github.com/chef/chef>.

**Chef has receded, and this folder should say so plainly.** Two things caused it. First, Chef
moved its distributions to a commercial licence — the source remains open, but the binaries most
people actually install carry a licence agreement — and the trust cost of that change was
significant. Second, Chef Software was acquired by Progress, and the product's centre of gravity
moved towards the commercial compliance and security portfolio rather than towards the open
configuration-management tool.

Neither of those makes Chef bad software. Both make it a poor default for a new platform, and
adoption in the wider ecosystem reflects that.

It is mapped here for completeness, because "how did people solve configuration drift before
Kubernetes" is a question worth being able to answer, and because Chef's continuous-convergence
model is the direct intellectual ancestor of what a Kubernetes controller does. The full framing
is in [`../README.md`](../README.md).

---

[← Configuration management](../README.md)
