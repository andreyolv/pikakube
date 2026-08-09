[← Provenance](../README.md)

# in-toto

<https://github.com/in-toto/in-toto>
<https://github.com/in-toto/attestation>

---

## The problem it solves

Supply-chain evidence needs a common shape. Without one, every claim about an artefact — this
is its SBOM, this is how it was built, this passed the tests, two people reviewed it — arrives
in a different format, signed a different way, and verified by different code.

in-toto is that common shape. A CNCF project, originally from NYU, it defines a signed
statement with three parts:

| Part | Meaning |
|---|---|
| `subject` | what the statement is about — a name and a digest (`sha256:...`) |
| `predicateType` | what **kind** of statement this is, identified by a URI |
| `predicate` | the statement itself, structured according to its type |

wrapped in a **DSSE** envelope carrying the signature. That is the whole model, and its
generality is the point: `slsa.dev/provenance` is one predicate type,
`cyclonedx.org/bom` is another, VEX is another, and a custom "this was approved by change
management" predicate is equally valid. One verification path covers all of them.

The original in-toto framework also covers **layouts**: a signed definition of the steps a
supply chain must go through, who is authorised to perform each, and what artefacts flow
between them — so a verifier can check the whole pipeline was followed rather than checking a
single step. That part is less widely deployed than the attestation format, which has become
the industry standard on its own.

## When to use it

- **anywhere provenance or evidence is produced** — you are already using it if you use SLSA
  provenance, cosign attestations, or BuildKit's `--attest`; the format underneath is in-toto
- you need to attach a **custom claim** to an artefact: an internal approval, a test result, a
  scan result, a manual review, and want it verified the same way as everything else
- building tooling that consumes supply-chain evidence — the `attestation` repository is the
  canonical list of predicate types and their schemas
- multiple evidence producers exist and you want one verification story rather than one per
  tool

## When not to use it

- as an alternative to SLSA. They are not comparable: SLSA says what to claim and how
  trustworthy the claim is, in-toto says how to write it down. See
  [`../README.md`](../README.md#2-slsa-is-levels-in-toto-is-the-format)
- expecting the layout/step-authorisation model to be a turnkey product — it is the more
  ambitious and less commonly deployed half, and adopting it is a project
- as something to install. In most pipelines in-toto is a format you emit through cosign,
  `actions/attest` or BuildKit, not a tool you run directly
- if nothing verifies. An attestation format with no verifier is JSON

## Notes

Original references recorded for this tool:

> <https://github.com/in-toto/in-toto>
> <https://github.com/in-toto/attestation>

The split between the two repositories is worth understanding, because they are used by
different people.

**`in-toto/in-toto`** is the framework and the reference Python implementation: layouts,
steps, functionaries, link metadata — the full model of a supply chain as a sequence of
authorised operations. This is the research-grade, complete version of the idea.

**`in-toto/attestation`** is the specification that everyone actually implements: the
Statement/DSSE format above, plus the registry of predicate types. When a tool says "in-toto
attestation", it means this repository. If you are looking for the exact JSON your verifier
expects, or for whether a standard predicate already exists for the claim you want to make,
this is where to look — writing a bespoke predicate when a standard one exists is the most
common way to make evidence non-portable.

One practical note for anyone debugging verification failures: the signature is over the DSSE
**payload**, which is the base64-encoded statement, not over the artefact and not over the
pretty-printed JSON you are reading. Re-serialising an attestation, even without changing its
meaning, invalidates it.

---

[← Provenance](../README.md)
