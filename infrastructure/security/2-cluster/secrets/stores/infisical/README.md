[← Secret stores](../README.md)

# Infisical

<https://github.com/Infisical/infisical>

A developer-facing secrets platform: a web UI, a CLI, and per-environment secret management. What is
deployed here is its Kubernetes **operator**, not the platform itself.

---

## The problem it solves

[Vault](../vault/README.md) is a security engineer's tool. Its model — engines, HCL policies, auth
methods, leases, seals — is powerful and it is a lot to learn before you can store a database
password. On a small team the practical outcome is often that nobody sets it up properly and secrets
stay in a `.env` file.

Infisical targets that gap. The mental model is projects and environments rather than mount points
and policies:

| Concept | Meaning |
|---|---|
| Project | usually one application or service |
| Environment | dev / staging / production, with different values for the same keys |
| Folder and path | organisation within an environment |
| Secret | a key-value pair with a version history |

Around that it puts a web UI a developer will actually use, a CLI that injects secrets into a local
process (`infisical run -- npm start`), integrations with GitHub Actions, Vercel and similar, and
**secret scanning** for credentials accidentally committed to Git.

That last one is a genuinely different feature from anything else in
[`../../`](../../README.md): it is prevention at the point where secrets most often leak.

It also does secret **sharing** — a link with an expiry, for the recurring problem of one person
needing to send another a credential without using Slack.

It is open source (MIT core, with paid features), self-hostable, and offers a managed cloud.

## When to use it

- **Developer experience is the binding constraint.** If the honest reason secrets are in `.env`
  files is that Vault is too much, a tool people will actually use is worth more than a better tool
  they will not.
- **Local development matters.** `infisical run` injecting secrets into a local process, from the
  same source as production, removes the `.env` file rather than encrypting it.
- **You want per-environment values as a first-class concept.** Vault expresses this with path
  conventions and policies; Infisical has it built in.
- **You want secret scanning too.** Detecting credentials in commits is a different control from
  storing them safely, and it addresses the more common failure.
- **The team is small.** One system, a UI, and a short setup, versus Vault's operational commitments
  in [`../README.md`](../README.md#6-operating-cost-stated-plainly).
- **CI/CD integrations are the main need.** Its integration catalogue is aimed squarely at that.

## When not to use it

- **You need dynamic secrets.** This is the decisive difference. Infisical has dynamic secret support
  for some backends, and Vault's is far more mature and covers more engines. If per-request database
  credentials with a TTL are the goal — the one capability that genuinely justifies running a store
  at all, per [`../README.md`](../README.md#2-dynamic-secrets) — Vault or
  [OpenBao](../openbao/README.md) is the answer.
- **You need PKI or encryption as a service.** Vault's `pki` and `transit` engines have no
  equivalent here.
- **The credential store must be the security boundary for a large organisation.** Vault's policy
  model, audit devices and enterprise features exist because large organisations needed them.
- **You are not going to self-host it.** The cloud offering is a third party holding your
  credentials. That may be fine; it must be a decision.
- **You want one store, and Vault is already running.** Two stores means two sources of truth and the
  question "where does this credential live" has no answer.

## Notes

The original `doc.md` contained only the repository link, which is at the top of this file. What
follows is the state of this folder, and it is the most important thing about it.

### What is deployed here is the operator, not Infisical

`helm/helmrelease.yaml` installs chart **`secrets-operator`** 0.8.0 from the `infisical-helm-charts`
HelmRepository, with no values.

That chart is the **Infisical Kubernetes Operator**, which does one job: watch `InfisicalSecret`
custom resources and sync secrets *from an Infisical instance* into Kubernetes `Secret` objects.

So this folder is structurally an [integration](../../integrations/README.md), not a store. The
Infisical platform itself — the API, the web UI, the database — is not deployed anywhere in this
repository, and the operator has nothing to sync from. It would install and idle.

That makes it the least complete of the three stores here. [Vault](../vault/README.md) has a real
deployment and a working consumer; [OpenBao](../openbao/README.md) runs in dev mode and can at least
be clicked through; this is a client for a server that does not exist.

### How it would fit if adopted

Two shapes, and the choice matters:

| Shape | Meaning |
|---|---|
| **Infisical Cloud** + this operator | no platform to run; a third party holds the credentials |
| **Self-hosted Infisical** + this operator | another stateful application with its own PostgreSQL and Redis, on the critical path |

The self-hosted version is not obviously lighter than Vault — it is a web application with a
database, so the operational surface is comparable, just differently shaped. The advantage is the
interface, not the running cost.

The `InfisicalSecret` CRD authenticates with a service token or a machine identity, held in a
Kubernetes `Secret`. That is the same static-credential pattern as the
[external-secrets Vault store](../../integrations/external-secrets/README.md) in this repo, with the
same objection: a long-lived token in a Secret is what a store was meant to remove. Infisical's
Kubernetes-native auth method is the version worth using.

### A simpler option

[external-secrets](../../integrations/external-secrets/README.md) supports Infisical as a provider.
Since it is already deployed and configured in this repository against two other stores, adding
Infisical through it would mean one integration API instead of a second operator — and it would keep
the "which store" decision reversible.

That is the argument for treating this folder as a reference rather than a fourth controller to
install.

---

[← Secret stores](../README.md)
