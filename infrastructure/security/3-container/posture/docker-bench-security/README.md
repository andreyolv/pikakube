[← Container posture](../README.md)

# docker-bench-security

<https://github.com/docker/docker-bench-security>

---

## The problem it solves

The **CIS Docker Benchmark** is a long document of numbered configuration checks. Reading it and
verifying each item by hand against a host is a day of work that nobody repeats.

docker-bench-security is a shell script that automates it. Run it on a host with the Docker
daemon and it walks the benchmark, printing PASS / WARN / INFO / NOTE per numbered check:

```bash
# run against the host, with the access the checks require
docker run --rm --net host --pid host --userns host --cap-add audit_control \
  -v /etc:/etc:ro -v /var/lib:/var/lib:ro -v /var/run/docker.sock:/var/run/docker.sock:ro \
  docker/docker-bench-security
```

What it covers, in the benchmark's own sections: host configuration, daemon configuration,
daemon file permissions, image and build-file practice, container runtime settings, security
operations, and Swarm.

The output is a checklist against a published standard, which is its real value: it gives you a
**numbered, citable** result rather than an opinion. That is what makes it useful for an audit
conversation.

## When to use it

- **Hosts that actually run the Docker daemon** — CI runners, build machines, developer
  workstations, VMs with Docker Compose, legacy estate. This is the tool's real audience today
- **CI runners specifically.** They run a daemon, expose a socket, and hold registry credentials
  and signing keys. It is the highest-value host in most organisations and the least examined —
  related material lives under `security/0-governance/runner-hardening/`
- **A baseline before hardening.** Run it once to see where you stand, fix the findings that
  apply, then re-run as part of provisioning
- **When an auditor asks for CIS Docker Benchmark evidence.** The numbered output maps directly
  to the document

## When not to use it

- **Kubernetes nodes running containerd or CRI-O.** `dockershim` was removed in Kubernetes 1.24,
  so most clusters have no Docker daemon at all. The script will check a component that is not
  present and produce findings that mean nothing. The right document for a cluster is the **CIS
  Kubernetes Benchmark**, which Trivy Operator can produce in-cluster — see
  [`../../scan/trivy/README.md`](../../scan/trivy/README.md)
- **Managed Kubernetes node pools.** The provider hardens the node image, and much of what the
  script inspects is not yours to change. Read the shared responsibility model before acting on
  the output
- **As a runtime control.** It is detective, run on demand. Preventing privileged containers,
  host namespace sharing and `docker.sock` mounts is admission policy's job in
  `security/2-cluster/` — see [`../README.md`](../README.md) section 4
- **Expecting it to gate anything.** It is a script that prints a report; wiring it into a
  pipeline as a pass/fail gate means deciding which checks are mandatory, which the tool does not
  decide for you
- **Local development clusters.** Kind and Docker Desktop will fail many checks by design, and
  none of it reflects production risk

## Notes

Original note recorded for this tool:

- <https://github.com/docker/docker-bench-security> — the upstream script, maintained under the
  Docker organisation. The repository is worth reading rather than only running: each check is a
  small shell function annotated with its CIS number, so it doubles as a readable explanation of
  *why* each setting matters and *how* it is verified. That makes it a decent reference even on
  hosts where you would not run it.

Two caveats to record alongside it:

- **Check the currency of the benchmark version implemented.** The script tracks a specific
  edition of the CIS Docker Benchmark; if the version implemented lags the version an auditor is
  asking about, the mapping is not one-to-one.
- **It needs substantial host access to run** — host PID and network namespaces, `/etc` and
  `/var/lib` mounted, and the Docker socket. That is a lot of privilege for an audit tool.
  Run it deliberately, on hosts you control, not as a permanently scheduled workload.

---

[← Container posture](../README.md)
