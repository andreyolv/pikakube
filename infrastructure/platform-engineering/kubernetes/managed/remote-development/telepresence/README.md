[← Remote development](../README.md)

# Telepresence

<https://github.com/telepresenceio/telepresence>

---

## The problem it solves

Telepresence has two modes, and understanding the split is understanding the tool.

**Connect** builds a network tunnel: cluster DNS resolves on your machine, and cluster Services are
reachable from local processes. Your laptop becomes, for networking purposes, part of the cluster.

**Intercept** goes further: traffic destined for a workload is redirected to a port on your machine.
The service's callers now reach your local process, with the pod's environment variables and mounted
volumes made available to it.

It is a CNCF project and the most established tool in this category.

## When to use it

- A service with many in-cluster dependencies that cannot all be run locally
- Debugging with a native local debugger against real cluster traffic
- Personal intercepts, so only your own requests are diverted on a shared cluster
- Simply reaching cluster services from local tooling — connect mode alone is useful

## When not to use it

- Production, without qualification
- Global intercepts on a shared cluster; everyone's traffic hits your uncommitted code
- Where the local process would write to real datastores
- If a VPN-style tunnel is all you need — [KubeVPN](../kubevpn/README.md) is smaller

## Notes

**Installed from an `OCIRepository`**, with a namespace manifest — the in-cluster traffic manager,
which is the component that makes intercepts possible.

**The recorded commands:**

```sh
telepresence connect
telepresence list
telepresence intercept example-service --port 8080:http
```

Each does something distinct:

- `connect` establishes the tunnel and installs or contacts the traffic manager. After this, cluster
  DNS names resolve locally — the immediate test is `curl` against a Service name.
- `list` shows the interceptable workloads in the current namespace, and which are currently
  intercepted. Worth running before intercepting, and worth running again afterwards to confirm you
  cleaned up.
- `intercept example-service --port 8080:http` redirects traffic. The `8080:http` syntax is
  `<local port>:<remote port name>` — the local port your process listens on, mapped to the **named**
  port on the Service. Using the port name rather than the number is the more robust form, and it is
  the part of the syntax people get wrong.

**Personal intercepts are the feature that makes this safe on a shared cluster.** A default intercept
is global: every request to that service reaches your machine. A personal intercept matches on a
header or on your identity, so only your own requests are diverted and everyone else continues to hit
the real pod. On any cluster with other users, this is not optional.

**Always disconnect.** An intercept left active means the service is down for its callers the moment
your laptop sleeps. `telepresence leave` and `telepresence quit` are the counterparts to the commands
above, and the habit worth building is `list` before walking away.

**Licensing** has moved around — Ambassador Labs maintain it, with an open-source core and a
commercial offering for team features, and the boundary has shifted between versions. Check which
version and which features before designing a team workflow around it, exactly as with
[mirrord](../mirrord/README.md).

---

[← Remote development](../README.md)
