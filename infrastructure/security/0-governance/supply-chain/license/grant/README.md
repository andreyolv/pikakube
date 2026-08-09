[← License compliance](../README.md)

# Grant

<https://github.com/anchore/grant>

---

## The problem it solves

You already generate SBOMs. Every one of them lists a licence per component. Nothing checks
those licences against a policy.

Grant is Anchore's small CLI for exactly that gap: point it at an SBOM, a container image or a
directory, give it a list of allowed and denied licences, and it returns a pass or fail plus
the offending components. It is deliberately narrow — no server, no database, no workflow, no
detection engine. A policy file and an exit code.

Its position in [`../README.md`](../README.md#4-declared-vs-detected) is the declared-licence
side: it reads what the package metadata says, which is fast and correct in the common case.
It does not scan file headers, so it will not catch a relicensed file or a vendored library
with no metadata.

The natural pairing is [syft](../../sbom/syft/README.md) — same vendor, same data model — so
one SBOM generation step feeds both the vulnerability path and the licence path.

## When to use it

- SBOMs are already produced and you want a **cheap CI gate** on licences without adopting a
  compliance platform
- the policy is simple and expressible as an allow/deny list of SPDX identifiers
- you want licence checks on the **built image**, which is where the base-image packages appear
  — the case [`../README.md`](../README.md#3-distribution-is-the-trigger--and-a-container-image-is-distribution)
  argues actually matters
- as a first step: catch the obvious problems now, decide later whether deeper detection is
  needed

## When not to use it

- when **detection** is required rather than declared metadata — vendored code, missing
  metadata, dual licences, relicensed files. That is [ORT](../ort/README.md)
- for due diligence, an acquisition, or anything where the answer has to be defensible. A
  declared-metadata scan is not an audit
- when attribution documents (NOTICE files, disclosure documents) are the deliverable — grant
  reports, it does not generate
- when the compliance process needs reviewers, exceptions with expiry, and an audit trail —
  that is [FOSSA](../fossa/README.md)'s shape
- if no SBOM exists and none is planned; grant can scan an image directly, but most of its
  value is as one more consumer of an SBOM you already produce

## Notes

Original reference recorded for this tool:

> <https://github.com/anchore/grant>

Nothing further was recorded, which is consistent with what the tool is — there is not much
surface to have opinions about.

Two things worth knowing before adopting it. First, **write the policy in SPDX identifiers**,
not in informal names: `GPL-3.0-only` and `GPL-3.0-or-later` are different licences, and "GPL"
matches neither precisely. The SPDX list linked from
[`../README.md`](../README.md#9-notes) is the reference.

Second, expect **`NOASSERTION` / unknown** results, and decide what they mean before turning
the gate on. A meaningful fraction of components in any real image carry no usable licence
metadata, and the two possible policies — fail on unknown, or allow and review — have very
different day-one consequences. Failing on unknown is the correct posture and will block the
first build; allowing it quietly is how a licence gate ends up permitting the exact components
it was installed to catch.

---

[← License compliance](../README.md)
