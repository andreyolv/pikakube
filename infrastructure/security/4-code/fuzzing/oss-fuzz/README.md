[← Fuzzing](../README.md)

# OSS-Fuzz

<https://github.com/google/oss-fuzz>

---

## The problem it solves

Coverage-guided fuzzing works, but it needs to run **continuously** on substantial hardware to be
effective — hours and days per target, not minutes in CI. Very few open-source projects have that
infrastructure, and the projects that most need fuzzing are exactly the widely used libraries
maintained by one or two people in their spare time.

OSS-Fuzz is Google's answer: **free, continuous fuzzing infrastructure for open-source projects**.
You contribute the fuzz targets and a build configuration; Google runs them forever.

How it works in practice:

| Step | Detail |
|---|---|
| **Onboard** | submit a `project.yaml`, a `Dockerfile` and a `build.sh` to the `oss-fuzz` repository, plus contact addresses |
| **Write targets** | fuzz targets live in your own repository, so they stay with the code |
| **It runs** | Google builds with libFuzzer/AFL++ and the sanitisers, and fuzzes continuously on their infrastructure |
| **Bugs are filed** | crashes are triaged, deduplicated and reported to the maintainers privately, with a reproducer |
| **Disclosure** | a 90-day deadline, after which the issue becomes public. This is the part to know before onboarding |
| **Fix verification** | it confirms when a fix actually resolves the crash, and reports regressions |

Two related things worth knowing because they connect this folder to the rest of the tree:

- **ClusterFuzzLite** is the cut-down version that runs in your own CI on pull requests. It is the
  right tool for private code and for catching regressions quickly, and it does not require
  onboarding to OSS-Fuzz.
- **OSS-Fuzz findings feed OSV.** Vulnerabilities discovered here are published into the OSV
  database, which means they arrive in [`../../sca/osv-scanner/README.md`](../../sca/osv-scanner/README.md)
  and in Trivy. A meaningful share of the dependency CVEs you triage originated as an OSS-Fuzz
  crash.

The scale is the argument: it has found tens of thousands of bugs across the widely used
open-source libraries almost everything depends on.

## When to use it

- **You maintain a widely used open-source library** that parses untrusted input — a codec, a
  parser, a protocol implementation, a compression or crypto library. This is precisely the target
  audience and the service is free
- **A memory-unsafe language** — C or C++ — where a parsing bug is potentially remote code
  execution
- **The project meets the eligibility criteria** — broadly, significant usage or importance to
  the ecosystem. Check before assuming
- **You want the reporting and triage done for you.** Deduplicated crashes with reproducers,
  filed as issues, is a substantial amount of work you do not have to do

## When not to use it

- **Private or proprietary code.** OSS-Fuzz is for open source, and the disclosure model is
  public by design. **ClusterFuzzLite** is the option for private repositories
- **You cannot commit to fixing what it finds.** The 90-day disclosure deadline is not optional.
  Onboarding a project you cannot maintain converts silent bugs into publicly disclosed ones on a
  clock
- **The project does not parse untrusted input.** A build tool, a web application, a set of
  configuration files — there is nothing for a fuzzer to explore
- **You are consuming open source rather than maintaining it.** Which is the usual case, and this
  repository's case. The relevant relationship is then indirect: OSS-Fuzz findings reach you as
  CVEs in your dependencies

## Notes

Original note recorded for this tool:

- <https://github.com/google/oss-fuzz> — the project repository. It contains the onboarding
  configuration for every participating project (which makes it a large corpus of working
  `build.sh` and `Dockerfile` examples to copy from), the documentation for writing fuzz targets
  in each supported language, the eligibility criteria, and the disclosure policy. The
  per-project directories are the most useful part: finding a project similar to yours and reading
  its build configuration is faster than reading the documentation.

Also worth recording:

- **The reward programme.** OSS-Fuzz has historically paid for integrating projects and for
  improving coverage, which is worth knowing if you maintain something eligible.
- **The language support has broadened.** It began as a C/C++ service and now covers Go, Rust,
  Python, Java and JavaScript, with the corresponding engines. The findings differ by language —
  memory corruption in C, unhandled exceptions and hangs in the memory-safe ones — but the
  continuous infrastructure is the same.

---

[← Fuzzing](../README.md)
