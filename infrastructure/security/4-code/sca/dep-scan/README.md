[← SCA](../README.md)

# OWASP dep-scan

<https://github.com/owasp-dep-scan/dep-scan>

---

## The problem it solves

Most SCA tools stop at matching: here is a package, here is a version, here is a CVE. dep-scan's
position is that matching is the easy part and the useful work starts afterwards — deciding which
findings matter and producing evidence you can act on and publish.

What it adds beyond a matcher:

| Capability | What it means |
|---|---|
| **SBOM-centric** | it generates a CycloneDX SBOM (via `cdxgen`) and analyses that, so the inventory is a reusable artefact rather than an internal step |
| **Reachability analysis** | for supported languages it attempts to determine whether the vulnerable code is actually reachable from your application, using call-graph analysis |
| **VEX and CSAF output** | it emits machine-readable statements about which vulnerabilities *do not* affect the artefact and why — which is how you communicate triage decisions downstream instead of burying them in an ignore file |
| **Prioritisation** | it factors in exploit availability (KEV, exploit maturity) rather than ranking purely by CVSS |
| **Broad ecosystem coverage** | many languages, plus container images, OS packages and some IaC |

The VEX output is the part worth understanding, because it is the piece nobody else in this
folder produces. A VEX document says "CVE-2024-x is present in this artefact but not exploitable,
because the affected function is never called". Published alongside the artefact, it means the
next scanner downstream — a customer's, or your own image scanner — can suppress the finding with
a recorded justification rather than a shrug. That is the mechanism which stops the same triage
decision being made independently by five different teams.

It is an **OWASP project**, developed under the `owasp-dep-scan` organisation (originating from
AppThreat).

## When to use it

- **You already produce or want to produce SBOMs**, and want the vulnerability analysis to be
  derived from them — this connects directly to `security/0-governance/supply-chain/sbom/`
- **Prioritisation is the problem, not detection.** If the complaint is "we have 400 findings and
  no idea which 4 matter", reachability and exploit-availability ranking is the right lever
- **You need to publish VEX.** Either because customers ask for it, or because you want your own
  image scanning to consume your triage decisions automatically
- **Polyglot repositories**, where its breadth is an advantage
- **As a deeper second pass**, run on a schedule, behind a fast scanner in CI

## When not to use it

- **As the simple default.** [`../osv-scanner/README.md`](../osv-scanner/README.md) is a single
  binary with essentially no configuration; dep-scan is a Python toolchain with more moving parts
  (including `cdxgen`, which is a Node tool). More capability, more to operate
- **When CI speed matters most.** SBOM generation plus reachability analysis is meaningfully
  slower than a lockfile match
- **When you will not act on the extra output.** Reachability and VEX are only valuable if
  someone consumes them. Generating VEX documents nobody reads is the same failure mode as
  generating SBOMs nobody reads
- **Expecting reachability to be uniform.** It is good for some languages and absent for others.
  Check your ecosystem before designing a policy around it
- **When the requirement is specifically an OWASP Dependency-Check report.** Despite both being
  OWASP projects with similar names, they are different tools —
  [`../dependency-check/README.md`](../dependency-check/README.md)

## Notes

Original note recorded for this tool:

- <https://github.com/owasp-dep-scan/dep-scan> — the upstream project. The repository documents
  the supported languages and package managers, the reachability analysis and which ecosystems it
  covers, the VEX/CSAF output options, the risk-audit features (which flag suspicious package
  characteristics, not only known CVEs), and the container image it ships for CI use.

Two adjacent projects from the same organisation that the documentation assumes you know about:

- **`cdxgen`** — the CycloneDX SBOM generator dep-scan uses. Useful on its own if SBOM generation
  is the requirement.
- **`vdb`** — the local vulnerability database it builds and queries, which is what allows offline
  and air-gapped operation.

A naming caution worth recording: **OWASP dep-scan and OWASP Dependency-Check are unrelated
tools** with different authors, different techniques and different data sources. They are
routinely confused, including in tender documents.

---

[← SCA](../README.md)
