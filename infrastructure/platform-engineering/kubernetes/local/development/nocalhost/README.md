[← Development](../README.md)

# Nocalhost

<https://github.com/nocalhost/nocalhost>

---

## The problem it solves

Nocalhost puts the inner loop inside the IDE. Its VS Code and JetBrains plugins let you enter
"development mode" on a workload — the container is replaced with a dev image, your source is
synced in, and you can attach the IDE's debugger to the process running in the cluster. Breakpoints
in a pod, from the editor, without a separate CLI in another window.

That is the differentiator. Everything else it does — sync, restart, port-forward — the other tools
here also do.

## When to use it

- Interactive debugging against in-cluster dependencies is the actual requirement
- The team lives in JetBrains or VS Code and wants no terminal in the loop
- A CNCF-adjacent tool is preferred over a vendor CLI

## When not to use it

- Project health matters to you — see the note below
- You want a config that also works in CI
- The debugger is not the point; simpler sync tools cover the rest
- Against a shared cluster, where replacing a workload disrupts other people

## Notes

Recorded as a link only:

```
https://github.com/nocalhost/nocalhost
```

Known, not evaluated — and in this specific case the absence of evaluation is worth flagging rather
than glossing over. **Check the repository's activity before adopting it.** Nocalhost was a CNCF
Sandbox project and development has been slow to stopped; an IDE plugin that is not tracking IDE
releases stops working in a way that is nobody's fault and nobody's fix.

If the debugging story is what appeals and the project turns out to be dead, the closest
replacements are [mirrord](../../../managed/remote-development/mirrord/README.md) and
[Telepresence](../../../managed/remote-development/telepresence/README.md), which come at the same
problem from the other direction: run the process locally, in your debugger, and give it the
cluster's network and environment.

---

[← Development](../README.md)
