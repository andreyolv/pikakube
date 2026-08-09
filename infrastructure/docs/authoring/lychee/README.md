[← Authoring](../README.md)

# lychee

<https://github.com/lycheeverse/lychee>

---

## The problem it solves

A link is the one part of a document that can break without anybody touching the document.

Two failure modes, and they are not the same problem:

| Failure | Cause | Whose fault |
|---|---|---|
| **A relative link to a file that moved** | the repository was reorganised | ours, and entirely preventable |
| An external URL that went away | someone else's site changed | nobody's here, and unfixable at the source |

The first is the one that matters, and it is invisible in review. Renaming a folder produces a
clean diff — the moved files are shown, the several dozen documents that pointed at them are not.
Nothing fails, nothing warns, and the links are dead from the moment the rename lands.

**lychee checks both kinds.** It parses Markdown, HTML and plain text, extracts every link, and
resolves relative paths against the filesystem as well as requesting external URLs. It is written
in Rust and issues requests asynchronously, which is what makes checking a large tree a matter of
seconds rather than a coffee break — and that speed is the difference between a check that runs on
every pull request and one that runs never.

## When to use it

- **a documentation repository navigated by relative links** — this is the case it is built for
- after any folder rename or restructuring, as the verification step
- in CI on every pull request, restricted to local links, so a move cannot merge broken
- on a published documentation site, where a 404 is the reader's problem rather than the author's
- as a scheduled job for external URLs, separately from the pull-request gate

## When not to use it

- a handful of files with no cross-references — there is nothing to break
- as a blocking CI gate **including external URLs**; see below, this is the mistake that kills it
- as a substitute for checking that a link points at the *right* page; it verifies the target
  exists, not that it is the one intended
- for anchor-level certainty in every generator's output — heading fragments depend on how the
  renderer slugifies, so treat fragment checking as useful rather than authoritative

## The two modes, and why the split matters

This is the whole operational argument for the tool, so it is worth being explicit.

| Mode | Checks | Where it belongs |
|---|---|---|
| **Offline** | relative file paths only, no network | **the pull-request gate** — deterministic, fast, and always our fault when it fails |
| Full | relative paths **and** external URLs | a scheduled run, reporting rather than blocking |

Offline mode is the one that matters for a repository like this one. It has no network dependency,
so it cannot fail because a CI runner had no egress or because a host was briefly down. Every
finding is a real defect in the repository, and every finding is fixable by the person who caused
it.

Running the full check as a blocking gate is the failure everybody discovers eventually: a build
that fails because a third party's certificate expired is a build people learn to re-run without
reading. Once that habit forms the check is dead, including for the local links it was actually
good at. **External link rot is real and worth knowing about; it is not worth blocking a merge
on.**

## Making the external run survivable

The full run still needs tuning, because the internet is hostile to anything that requests a
thousand URLs at once.

| Problem | What to do |
|---|---|
| **GitHub returning 429** | unauthenticated requests to github.com are rate-limited aggressively, and a documentation repository is mostly GitHub links — supply a token so the requests are authenticated |
| Too many requests in flight | lower the concurrency limit; the default is tuned for throughput, not for politeness |
| The same URLs re-checked every run | enable the cache, with an age limit, so unchanged links are not re-requested |
| Hosts that always fail | exclude them by pattern — paywalls, sites that block non-browser user agents, hosts behind a corporate network |
| Endpoints that answer 403 to a HEAD request | accept the status codes that mean "reachable but not fetchable" rather than treating them as broken |

The exclusion list is maintenance in itself, and it should be short and commented. An exclusion
list that grows without anybody reading it becomes the mechanism by which genuinely broken links
get ignored.

## Notes

Written in Rust, distributed as a binary, a container image and a GitHub Action, and configurable
from a file rather than an ever-growing command line — which matters once the exclusions and
accepted status codes are more than a couple of entries.

**This repository has now recommended link checking twice, in two separate places, without naming
a tool.** [`site-generator/`](../../site-generator/README.md) calls it *"the single highest-value
check"* and *"the one piece of CI that this repository would benefit from immediately"*.
[`markdownlint/`](../markdownlint/README.md) goes further and ranks it above its own subject: *"Of
the two, link checking has the higher return. A wrong bullet character is cosmetic; a link
pointing at a folder that no longer exists is a broken document."*

lychee is the tool those two pages are describing.

The scale is the argument. There are **1204 `README.md` files under `infrastructure/`**, and the
navigation between them is entirely relative links — the folder tree *is* the table of contents,
which is the deliberate decision recorded in
[`site-generator/`](../../site-generator/README.md). That makes every link a structural dependency
rather than a convenience.

And the tree has moved. Repeatedly:

| Was | Became |
|---|---|
| `tests/` | [`testing/`](../../../software-engineering/testing/README.md) |
| `message-queue/` | [`messaging/broker/`](../../../software-engineering/messaging/broker/README.md) |
| `code-review/` | [`code-quality/review/`](../../../software-engineering/code-quality/review/README.md) |
| `envirorment/` | [`developer-environment/`](../../../software-engineering/developer-environment/README.md) |

Every one of those renames silently invalidated inbound links from elsewhere in the tree, and every
one of them was repaired by hand — by noticing, searching, and fixing. That is the work an offline
lychee run in CI does in seconds, before the rename is merged rather than weeks after.

The recommendation, concretely: **offline mode on every pull request, failing the build**, and a
full run on a schedule that opens an issue rather than breaking anything.

---

[← Authoring](../README.md)
