[← Remote development](../README.md)

# mirrord

<https://github.com/metalbear-co/mirrord>
<https://github.com/mihailtd/mirrord-demo>
<https://www.youtube.com/watch?v=KJpEebC1tNE>

---

## The problem it solves

mirrord runs your local process **as if it were a pod**, without deploying anything. It hooks the
process's syscalls and redirects them into the cluster: network traffic, environment variables,
mounted files and DNS all come from a target pod. You run your application from your IDE, and it sees
what the pod sees.

The distinguishing choice is the default: **mirroring, not stealing**. The target pod keeps serving
real traffic; your local process receives a *copy* of it. Nothing breaks if your code crashes,
because your code is not in the request path. Stealing is available when you want it, and it is
opt-in.

That default is what makes it usable on a shared cluster without a conversation first.

## When to use it

- Debugging a service locally with the cluster's real traffic, safely
- No `kubectl` deploy step at all — it wraps your existing run or debug command
- Shared clusters, where diverting traffic would disrupt colleagues
- Reproducing a bug that only appears with real request data

## When not to use it

- Team-wide use without the operator, which is licensed — see below
- Production; mirroring is safer than stealing, and this is still not for production
- Where duplicated side effects matter: mirrored requests mean your local code may write to the same
  database twice
- Platforms and languages its syscall hooking does not cover; check before planning around it

## Notes

**The licensing finding, which is the reason this folder is worth reading:**

> The Helm chart is enterprise-only and **requires a licence key**.

- <https://github.com/metalbear-co/charts/blob/main/mirrord-operator/values.yaml>

The distinction matters and is easy to miss. The **mirrord CLI is open source** and works
standalone — one developer, one laptop, mirroring a pod, no cluster component required. The **mirrord
operator** is the commercial part, and it is what provides the team-oriented capabilities: queueing
and coordinating concurrent sessions, policy over what may be targeted, and safe concurrent stealing
so two developers do not fight over the same workload.

So the free tier covers the individual case completely and the multi-developer case not at all. If
the reason for adopting mirrord is "our team debugs against a shared cluster", that is precisely the
licensed feature.

**The demo**, recorded as *"excellent"*:

- <https://www.youtube.com/watch?v=KJpEebC1tNE>
- <https://github.com/mihailtd/mirrord-demo>

Worth the endorsement — mirrord's value is difficult to convey in prose, because "your local process
thinks it is a pod" sounds like a tunnel until you watch a debugger break on a request that came from
inside the cluster.

**The duplicate-side-effects caveat** is the one thing mirroring does not solve. A mirrored request
is processed twice: once by the real pod and once by your local process. If handling it writes to a
database, sends an email or publishes a message, both happen. Mirroring is safe for *availability*,
not for *effects* — point the local process at scratch dependencies for anything that writes.

---

[← Remote development](../README.md)
