[← Core](../README.md)

# Ephemeral containers

<https://kubernetes.io/docs/tasks/debug/debug-application/debug-running-pod/>

---

## The problem it solves

A pod is misbehaving and its image is distroless, or scratch, or a hardened base with no shell.
`kubectl exec` fails because there is nothing to exec. Historically the answer was to rebuild the
image with debugging tools in it, deploy that, and lose the state you were trying to inspect.

Ephemeral containers fix this properly: `kubectl debug` injects an **additional container** into a
**running pod**, sharing its namespaces, without restarting anything. You bring your own image —
`busybox`, `ubuntu`, `netshoot` — and get a shell alongside the process you are investigating.

## When to use it

- Distroless or minimal images with no shell, no `ps`, no `curl`
- Network debugging from inside the pod's own network namespace, where DNS and routing are what the app sees
- Inspecting a live process without disturbing it, using `--share-processes`
- Any situation where restarting the pod would destroy the evidence

## When not to use it

- Where debug tooling is not permitted; the injected image is arbitrary and that is a real privilege
- As a way to patch a running container — changes are lost, and the pod is now different from its manifest
- If the pod is already `CrashLoopBackOff`; there is no running container to attach to, and a copy is the answer
- On clusters old enough that the feature is not available or not enabled

## Notes

The recorded commands, and what each part does:

```sh
kubectl run myapp --image=busybox:1.28 --restart=Never -- sleep 1d
```

A target to practise against. `--restart=Never` makes it a bare `Pod` rather than a Deployment, and
`sleep 1d` keeps it alive with no useful process — deliberately, so the debugging is the exercise.

```sh
kubectl debug myapp --container=myapp -it --image=ubuntu --share-processes --copy-to=myapp-debug
```

Four things happen here and each flag matters:

- `--image=ubuntu` — the debug container's image, which has the tools the target lacks
- `--share-processes` — enables the shared process namespace, so `ps` in the debug container sees the
  **target's** processes. Without it you see only your own shell, which makes the whole exercise
  pointless
- `--copy-to=myapp-debug` — creates a **copy** of the pod with the extra container instead of
  attaching to the original. The copy is a new pod with a new name; the original is untouched
- `--container=myapp` — names the target container within the pod

The `--copy-to` distinction is the one to understand. Without it, `kubectl debug` attaches an
ephemeral container to the live pod — which requires the `EphemeralContainers` feature to be
available and is the true "debug in place" mode. With it, you get a clone you can also modify
(different command, different image), which works on a pod that is crash-looping and where attaching
would not.

Two consequences of the clone worth remembering: it does not receive Service traffic unless its
labels happen to match, and it must be deleted afterwards. A forgotten `-debug` pod is a running copy
of a workload nobody is watching.

---

[← Core](../README.md)
