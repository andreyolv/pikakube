[← Local storage](../README.md)

# ksync

<https://github.com/ksync/ksync>
<https://github.com/syncthing/syncthing>

---

> **This is not storage.** ksync provisions nothing, implements no CSI interface, creates no
> PersistentVolume and appears as no StorageClass. It is an inner-loop development tool that
> synchronises files between a laptop and a running container. It is filed under `local/` because
> of the word "local", and that is a filing accident worth flagging rather than a category.

## The problem it solves

The Kubernetes inner loop is slow. Change one line of code and the path to seeing it run is:

```
edit → docker build → push to a registry → update the manifest
     → wait for the rollout → wait for the pod → look
```

That is a minute or more, per keystroke-sized change, and it destroys the rhythm of interactive
development. For an interpreted language — Python, Node, Ruby, PHP — the whole cycle exists to
move a text file into a container that could have read it directly.

ksync removes it. It watches a directory on the developer's machine and mirrors changes into a
running pod's filesystem, continuously and in both directions. Save the file, and the process
inside the container sees it immediately. With a framework that reloads on change, the result is
visible before you have moved your hand off the keyboard.

| Concern | ksync's answer |
|---|---|
| Transport | a [Syncthing](https://github.com/syncthing/syncthing) instance on each side |
| Placement | a DaemonSet in the cluster; a `ksync watch` daemon locally |
| Selection | pods matched by label selector and container name |
| Direction | bidirectional, so files generated in the container come back |
| Restart on change | optional — it can restart the container after a sync |

The bidirectional part is more useful than it sounds: dependency lock files, generated code and
migration scaffolding produced inside the container land back in the working tree where they can
be committed.

### Why it is filed here, and why that is misleading

Everything else under [`local/`](../README.md) answers "how does a pod get a PVC on this node".
ksync answers "how does my editor's output reach a container", which is a question about
developer experience.

Nothing in the storage decision tree leads here. It does not compete with
[local-path-provisioner](../local-path-provisioner/README.md), does not provide an access mode,
does not persist anything, and has no opinion about what happens when a node dies. Its
neighbours in concept are the tools in
[platform-engineering/kubernetes/local/development](../../../../platform-engineering/kubernetes/local/development/README.md)
— [Tilt](../../../../platform-engineering/kubernetes/local/development/tilt/README.md),
[Skaffold](../../../../platform-engineering/kubernetes/local/development/skaffold/README.md),
DevSpace — and the remote-development tools Telepresence and Mirrord.

If you arrived here looking for storage, the answer is in
[`../local-path-provisioner/`](../local-path-provisioner/README.md) or in
[`../../block-storage/`](../../block-storage/README.md).

## When to use it

Read the Notes first — the maintenance status is the deciding factor. Assuming a version that
works in your environment:

- **Interpreted languages with hot reload**: Flask, Django, Express, Rails, Vite. This is where
  file sync is transformative, because there is genuinely nothing to build.
- **Debugging in an environment that cannot be reproduced locally** — the pod has service
  accounts, sidecars, network policies and secrets that a laptop does not.
- **Large images with slow builds**, where the rebuild cost dwarfs the change.
- **Editing configuration or templates** inside a running container to test a hypothesis quickly.

## When not to use it

- **Anywhere near production.** Files that exist in a container and not in an image are files
  that vanish on the next restart and appear in no Git history. The whole mechanism is the
  opposite of the immutable-image discipline the rest of this repository assumes.
- **For compiled languages** without extra work — Go, Java, Rust need a build step that syncing
  source does not trigger. Tilt and Skaffold model that properly.
- **As a deployment mechanism**, in any form. It is not one, and using it as one produces
  containers whose contents nobody can reconstruct.
- **For anything expecting persistence.** Synced files live in the container's writable layer and
  die with it.
- **In a shared cluster**, casually. The DaemonSet has broad access to pod filesystems, which is
  a meaningful privilege to grant for a convenience.
- **As a new choice today** — see the Notes.

## Notes

The recorded note for this folder is the upstream repository,
<https://github.com/ksync/ksync>, and the necessary context is what has happened to it since.

**Check the maintenance status before adopting it.** ksync has seen very little activity for
years, and the ecosystem moved on while it stood still. That matters more than usual for this
tool, because it touches the kubelet's view of pod filesystems and depends on Kubernetes API
behaviour that changes across versions — an unmaintained tool in that position stops working
quietly, at upgrade time.

**What replaced it:**

| Tool | Approach |
|---|---|
| [Tilt](../../../../platform-engineering/kubernetes/local/development/tilt/README.md) | live-update of files into containers, plus builds and a UI, driven by a `Tiltfile` |
| [Skaffold](../../../../platform-engineering/kubernetes/local/development/skaffold/README.md) | build/deploy/sync pipeline with a file-sync mode |
| DevSpace | similar, with an emphasis on interactive terminals into pods |
| Telepresence / Mirrord | invert the problem — run the process **locally** and connect it to the cluster's network and environment |

The last row is the more interesting evolution. ksync moves files into the cluster; Telepresence
and Mirrord bring the cluster's context to the local process. For most of what people used ksync
for, the second model turns out to be less machinery and fewer surprises — the debugger, the
profiler and the editor all work normally because the process is genuinely local.

**Syncthing underneath** is worth knowing: ksync is essentially orchestration around
[Syncthing](https://github.com/syncthing/syncthing), which is a mature, actively maintained,
peer-to-peer file synchronisation tool. The transport is sound; the Kubernetes integration around
it is the part that has aged.

**Failure modes to expect** with any file-sync approach, ksync included:

- **Drift.** The container's filesystem and the image diverge, so "it works in my pod" becomes
  literally true and reproducible nowhere else.
- **Deletes.** Bidirectional sync means an accidental delete propagates in both directions.
- **Ignore rules.** Without them, `.git`, `node_modules` and build output sync too, which is slow
  and occasionally destructive.
- **Permissions and ownership.** Files arriving as the wrong UID inside the container produce
  errors that look like application bugs.

**No manifests exist in this folder**, and that is correct — ksync is installed as a CLI on the
developer's machine, which then creates its own DaemonSet. There is nothing for Flux to
reconcile, and nothing about it belongs in a GitOps repository's desired state.

---

[← Local storage](../README.md)
