[← Dependency updates](../README.md)

# Scala Steward

<https://github.com/scala-steward-org/scala-steward>

---

## The problem it solves

Scala's build tooling is unusual enough that generic dependency bots handle it badly. Scala
Steward is the ecosystem's own updater, and it exists because of specifics no general tool
encodes:

| Scala-specific problem | What Scala Steward does about it |
|---|---|
| **Cross-building** — artefacts are published per Scala version (`_2.13`, `_3`), and a library may not exist for the version you use | it resolves the correct cross-published artefact rather than proposing a version that does not exist for your build |
| **Build definitions are Scala code** — `build.sbt`, `project/*.scala`, `project/build.properties` | it parses and rewrites those, including sbt plugins and the sbt version itself |
| **Binary compatibility conventions** | it understands the ecosystem's versioning conventions, so a minor bump means something specific |
| **Scalafix migrations** | some library upgrades ship automated code migrations; Scala Steward can run them as part of the update PR |
| Also handles Mill and other Scala build tools | not only sbt |

That last capability — running the library's own Scalafix migration in the same pull request — is
genuinely distinctive. It is the difference between "this upgrade breaks compilation, good luck"
and "here is the upgrade with the mechanical changes already applied".

The project runs a public instance that opens pull requests against opted-in open-source
repositories, and it can also be self-hosted for private ones.

## When to use it

- **Scala repositories.** If the build is sbt or Mill, this is the tool the ecosystem uses, and
  the cross-building handling alone justifies it
- **Libraries with Scalafix migrations** — the automated migration support turns painful upgrades
  into reviewable ones
- **Open-source Scala projects**, where the public instance means nothing to operate
- **Alongside Renovate in a polyglot repository.** Scala Steward for the Scala modules, Renovate
  for the Docker images, charts and actions around them. They do not conflict if scoped

## When not to use it

- **Anything that is not Scala.** This is a single-ecosystem tool by design
- **A polyglot repository where you want one tool.** Renovate supports sbt and does an acceptable
  job; if uniformity matters more than depth, use it —
  [`../renovate/README.md`](../renovate/README.md)
- **When you will not run it for private repositories.** Self-hosting means operating a service
  with credentials to your repositories; for a small number of private Scala repositories,
  Renovate is less to run
- **Expecting vulnerability awareness.** It keeps dependencies current, which is the best
  prevention, but it is not driven by advisories. Pair it with
  [`../../sca/README.md`](../../sca/README.md) if you need CVE-driven updates

## Notes

Original note recorded for this tool:

- <https://github.com/scala-steward-org/scala-steward> — the upstream project. The repository
  documents the `.scala-steward.conf` configuration (update frequency, package allow/deny lists,
  grouping, `pullRequests.frequency`), how to opt a repository into the public instance, how to
  self-host, and the Scalafix migration mechanism. It also maintains the list of known migrations,
  which is worth browsing before a major library upgrade.

Relevance note for this repository: pikakube is not a Scala codebase, so this is mapped for
completeness rather than for use. It becomes relevant only if Scala workloads appear — which, on a
data platform running Spark, is not implausible. Spark jobs written in Scala are exactly the case
where this tool would earn its place.

---

[← Dependency updates](../README.md)
