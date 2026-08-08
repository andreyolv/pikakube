[← Network troubleshooting](../README.md)

# netshoot

<https://github.com/nicolaka/netshoot>

The debugging **method** — which layer to check in which order:
[../README.md](../README.md)

---

## The problem it solves

Diagnosing a network problem needs `dig`, `tcpdump`, `ss`, `nc`, `curl`, `traceroute` and
`iperf`. Application images have none of them, and installing them means mutating a running
workload — polluting the container, and changing the thing you are trying to observe.

netshoot is a container image with all of it already present. Nothing gets installed
anywhere.

## How to run it

```bash
# 1. Inside an EXISTING pod's network namespace — usually the right one.
#    Same netns, same resolv.conf, same NetworkPolicies as the real workload.
kubectl debug -it <pod> --image=nicolaka/netshoot --target=<container>

# 2. A throwaway pod, to test from a namespace in general.
kubectl run tmp-shell --rm -it --image=nicolaka/netshoot -- /bin/bash

# 3. On a NODE — host networking, routes, the CNI dataplane.
kubectl debug node/<node> -it --image=nicolaka/netshoot
```

**Option 1 is the important one.** Debugging from a *different* pod answers a different
question: it shares neither the target's DNS configuration nor the policies that select it.
"It works from my debug pod" therefore proves very little.

## Common checks

```bash
# name resolution
nslookup <url>

# is the port open?
telnet <url> <port>
nc -vz <url> <port>

# which public IP does the cluster egress from?
# (the address a partner firewall has to allow-list)
curl ifconfig.me
```

## When not to use it

- **as a permanent workload** — it is a shell full of network tools; leaving it running is unnecessary attack surface. Use `--rm`, or ephemeral containers, which disappear with the pod
- as a substitute for method — the tools do not tell you *where* to look. Walk the layers in [../README.md](../README.md) first

---

[← Network troubleshooting](../README.md)
