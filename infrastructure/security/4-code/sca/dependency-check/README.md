[← SCA](../README.md)

# OWASP Dependency-Check

<https://github.com/dependency-check/DependencyCheck>

---

## The problem it solves

Dependency-Check is the long-standing OWASP software composition analysis tool. It predates most
of this folder and works differently from the lockfile-based scanners: rather than parsing a
dependency manifest, it **inspects files** — JARs, DLLs, `package.json`, `.whl` files — extracts
evidence about what each one is (vendor, product, version, from manifests, filenames and
embedded metadata), builds a **CPE** identifier from that evidence, and matches it against the
**NVD**.

That design has one significant advantage and one significant cost.

**The advantage:** it can identify dependencies that no manifest declares. A shaded JAR with
another library repackaged inside it, a vendored DLL, a JAR dropped into `lib/` by hand — the
file-based approach finds these, and a lockfile scanner cannot.

**The cost:** CPE matching is inherently fuzzy. The tool assigns a confidence to its evidence and
still produces **false positives** — a library matched to a similarly named commercial product is
the classic case — as well as misses where no CPE was ever assigned. Anyone who has run it on a
large Java project has a suppression file to prove it.

Integrations exist for Maven, Gradle, Ant, Jenkins, and as a CLI, which is why it is deeply
embedded in Java build pipelines.

## When to use it

- **Java and .NET codebases**, which is where its file-based analysis is strongest and where
  shaded and repackaged dependencies are common
- **When an auditor or a standard asks for "OWASP Dependency-Check".** This is a real and
  frequent requirement. The tool is named in policies and compliance checklists, and substituting
  a technically better scanner is a conversation you may not want to have
- **When dependencies are not fully declared** — a legacy project with JARs committed into the
  repository, or artefacts assembled by a build that no manifest describes
- **Inside an existing Maven or Gradle build**, where the plugin makes it one line of
  configuration

## When not to use it

- **As a general polyglot scanner in 2025.** For npm, PyPI, Go, Cargo and the rest,
  [`../osv-scanner/README.md`](../osv-scanner/README.md) gives more accurate results with far less
  noise, because OSV keys on ecosystem and version range rather than on CPE strings
- **Without budgeting for suppression maintenance.** The `suppression.xml` file is not optional on
  a real project, and it becomes a maintained artefact in its own right
- **Without an NVD API key.** The NVD data feed has been rate-limited since 2023; without a key,
  the initial database download is extremely slow or fails outright. This is the single most
  common reason a first run appears to hang, and it catches everyone
- **In short-lived CI containers with no cache.** The NVD database is large; re-downloading it
  every build is slow enough to matter. Cache the data directory
- **Expecting reachability.** It reports presence, not exploitability

## Notes

Original notes recorded for this tool, including the judgement in the original file:

- <https://github.com/dependency-check/DependencyCheck> — the upstream project. Note the
  repository moved out of the `jeremylong` namespace into its own `dependency-check`
  organisation, which is worth knowing because older links and documentation point at the old
  location. The repository documents the analysers per file type, the suppression file format,
  the NVD API key configuration, and the Maven/Gradle/Ant/Jenkins integrations.

- **"documentation nonexistent, guesswork, it is closer to a scan"** — the verdict recorded in
  the original note, translated. Two separate complaints are worth separating out:

  - *Documentation and guesswork.* The upstream documentation is thin relative to the tool's
    behaviour, and the CPE evidence-matching model means the tool is genuinely **guessing** which
    product a file corresponds to. That is not a criticism of the implementation so much as an
    accurate description of how CPE matching works: it assigns confidence levels because it
    cannot be certain. When the guess is wrong you get a false positive, and the only remedy is a
    suppression entry.
  - *"Closer to a scan."* The point being made is a taxonomy one. Dependency-Check does not
    really analyse a declared dependency graph the way a lockfile-based SCA tool does — it walks
    files and identifies what it finds, which is the behaviour of a **scanner** rather than a
    composition analyser. That is why the results feel different in kind from
    [`../osv-scanner/README.md`](../osv-scanner/README.md)'s, and it explains both the extra
    coverage (shaded JARs) and the extra noise.

The practical conclusion from that note: use it where its file-based approach or its name is the
requirement — Java, .NET, compliance — and use an OSV-based tool everywhere else.

---

[← SCA](../README.md)
