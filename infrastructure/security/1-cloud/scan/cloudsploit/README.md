[← Cloud posture scanning](../README.md)

# CloudSploit

<https://github.com/aquasecurity/cloudsploit>

<https://github.com/aquasecurity/cloud-security-remediation-guides>

---

## The problem it solves

CloudSploit is Aqua Security's open-source cloud configuration scanner. Same shape as the
other two in this folder: read-only credentials, a library of checks, a report about what is
misconfigured in a live account. Providers covered are AWS, Azure, GCP and Oracle Cloud.

Two things make it distinct rather than redundant:

- **It is Node.js.** Every check is a small JavaScript module with a declared list of the
  API calls it needs. That makes the check library unusually easy to read and to extend —
  if you want to know precisely what a finding is testing, the file is twenty lines and says
  so.
- **It is paired with a remediation guide repository.** The findings are not just
  identifiers; there is a companion repository documenting how to fix each class of issue,
  which is the part most scanners leave to the reader.

```bash
# scan an account using credentials from the environment
./index.js --console=table --compliance=cis

# restrict to one plugin category
./index.js --plugin s3BucketEncryption
```

## When to use it

| Situation | Why CloudSploit |
|---|---|
| Custom checks are needed and the team writes JavaScript | the plugin model is the simplest of the three |
| The Aqua stack is already in use | it is the open-source core behind Aqua's cloud posture product, so findings line up |
| The remediation guidance matters as much as the detection | the companion repository is genuinely useful, independent of the scanner |

## When not to use it

| Situation | Use instead |
|---|---|
| A default choice is wanted, with no strong reason to differ | **Prowler** — broader checks, more frameworks, more activity |
| Compliance framework evidence is the goal | Prowler |
| Kubernetes should be assessed too | Prowler's Kubernetes provider; CloudSploit is cloud-only |
| A browsable one-off report is the deliverable | ScoutSuite |

Check the repository's recent activity before adopting it. Aqua's investment has visibly
shifted toward Trivy and its commercial platform, and CloudSploit gets far less attention
than it did as a standalone product. The same warning that applies to ScoutSuite applies
here in a weaker form: a scanner is only as good as the currency of its check library.

## Notes

Both links in the original note, and what they are for:

- <https://github.com/aquasecurity/cloudsploit> — the scanner. The `aquasecurity`
  organisation in the path is the provenance: CloudSploit was an independent product,
  acquired by **Aqua Security**, and it became the basis of Aqua's cloud security posture
  offering. The open-source repository remains, and remains usable.
- <https://github.com/aquasecurity/cloud-security-remediation-guides> — recorded in the
  original note under the heading **"rules"**. It is the remediation companion: per-finding
  documentation explaining what the misconfiguration is, why it matters and the concrete
  steps to fix it, per provider.

That second link deserves emphasis, because it is useful **even if you never run
CloudSploit**. A posture scan produces a list of identifiers, and the hard part is not
detection — it is knowing what to do with three hundred findings. A well-written, publicly
readable remediation library is a resource for triage regardless of which scanner produced
the list. Bookmark it separately from the tool.

---

[← Cloud posture scanning](../README.md)
