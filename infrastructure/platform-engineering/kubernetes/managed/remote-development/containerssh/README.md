[← Remote development](../README.md)

# ContainerSSH

<https://github.com/ContainerSSH/ContainerSSH>

---

## The problem it solves

ContainerSSH is an SSH server that launches a **container per connection**. A user connects with SSH;
ContainerSSH authenticates them against a webhook of your choosing, asks a configuration server which
image and which resources they should get, starts that container in Kubernetes or Docker, and
attaches the session to it. When the session ends, the container is destroyed.

So it is not remote development in the sense of the other tools here. It is a way to hand people a
disposable, isolated shell environment — with no user accounts on any host, no shared machine, and no
state surviving the session.

## When to use it

- Giving people shell access without creating accounts on a real machine
- Honeypots — its original well-known use, where every attacker gets a clean, isolated container
- Training and lab environments where each participant needs an identical, disposable shell
- Auditing shell sessions centrally, since every session passes through one service

## When not to use it

- Debugging your own service against cluster dependencies — that is what the other three tools here do
- Where `kubectl exec` and [`ephemeral containers`](../../core/ephemeral-containers/README.md) already
  cover the need, which is most of the time
- Without a plan for authentication; the auth webhook is not optional and it is yours to write
- Casually — an SSH endpoint that starts containers is a significant piece of exposed surface

## Notes

Recorded as a link only, with no chart and no manifests.

**It is filed here somewhat loosely.** [Telepresence](../telepresence/README.md),
[mirrord](../mirrord/README.md) and [KubeVPN](../kubevpn/README.md) all connect a developer's laptop
to a cluster. ContainerSSH gives someone a shell **inside** one. Related in the sense of "remote
access to compute", different in almost every other way — and worth stating so nobody evaluates it
against the other three and concludes it is worse at their job.

**The architecture is the interesting part**, and it is unusually clean: authentication and
configuration are both **webhooks you implement**. ContainerSSH itself makes no decisions about who
may connect or what they get; it asks your service and does as it is told. That makes it a building
block rather than a product — you can hand different users different images, different resource
limits, or a container in a different namespace, entirely from your own logic.

The cost of that design is that there is no useful default. A deployment requires writing at least an
authentication service before anything works, which is why this is not a thing you try in an
afternoon.

**Security posture**, stated once: this is an SSH server exposed to users, holding credentials to
create pods in a cluster. It is designed for that role and the isolation model is sound, but it
belongs on the list of things whose configuration deserves review rather than a quick install.

---

[← Remote development](../README.md)
