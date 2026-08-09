[← Documentation](../README.md)

# Authoring

Keeping the Markdown consistent, checking that it is still correct, and getting existing material
into it.

Tools covered: [`markdownlint`](markdownlint/README.md) · [`lychee`](lychee/README.md) ·
[`vale`](vale/README.md) · [`pandoc`](pandoc/README.md)

---

## Three jobs

| Job | Question | Tool |
|---|---|---|
| **Lint** | is the Markdown consistent, and does it render as intended? | [markdownlint](markdownlint/README.md) |
| **Check** | are the links still valid, and does the prose follow the style guide? | [lychee](lychee/README.md) · [Vale](vale/README.md) |
| **Convert** | how does an existing Word document become Markdown? | [Pandoc](pandoc/README.md) |

They sit together because all three are about the *source text* rather than the published output —
the layer beneath [`site-generator/`](../site-generator/README.md).

The split between the first two rows is worth being precise about, because both are called
"linting" in conversation and they fail for different reasons. **Linting is about the file**: it
reads one document and decides whether it is well formed, and every finding is fixable in that
file. **Checking is about what the file claims**: a link resolves or it does not, a term matches the
project's vocabulary or it does not, and the answer depends on things outside the document — the
rest of the tree, the network, a style guide.

That difference decides where each belongs in CI. Linting is deterministic and can always block a
merge. Checking is deterministic only when it is restricted to what the repository controls, which
is the central argument on the [lychee](lychee/README.md) page.

## Linting

Markdown is forgiving, which is why it drifts. Heading levels skip, lists use three different
bullet characters, code fences lose their language, and lines wrap at whatever width the author's
editor happened to use.

None of it is fatal and all of it accumulates, particularly across a repository written over
time.

| Rule class | What it catches |
|---|---|
| Heading structure | skipped levels, duplicate headings, missing top-level heading |
| **Code fences** | missing language, which is why syntax highlighting is inconsistent |
| Lists | mixed markers and inconsistent indentation |
| Links | empty text, bare URLs where a link was intended |
| Whitespace | trailing spaces, hard tabs, multiple blank lines |
| Line length | if the project cares |

The genuine value is in the middle rows. A code fence without a language renders as grey text,
and it is invisible in review because the diff shows the fence, not the rendering.

Two rules are worth disabling on purpose in most repositories: **line length**, which fights with
tables and long URLs, and **inline HTML**, which is sometimes the only way to get a result. A
linter whose failures are routinely ignored is worse than no linter.

## Checking

Two checks, and they are not equally urgent.

**Links.** A link is the one part of a document that breaks without anybody touching the document.
Renaming a folder produces a clean diff — the moved files are shown, the documents pointing at them
are not — so the links die silently and stay dead until a reader finds them.
[lychee](lychee/README.md) parses the Markdown, resolves relative paths against the filesystem and
requests external URLs, and it is fast enough to run on every pull request.

The operational decision that makes it stick is running **local links only** in the merge gate.
Those failures are always the repository's own fault and always fixable; external URLs fail because
somebody else's site is down, and a build that fails for reasons nobody can act on is a build
people learn to re-run without reading. External links belong in a scheduled run that reports
rather than blocks.

**Prose.** [Vale](vale/README.md) checks the text against a style guide rather than against
grammar — terminology, banned words, heading conventions, passive voice. It understands markup, so
it skips code fences, and it takes a project vocabulary so it does not flag every product name.

The honest caveat is that prose linting produces opinions, and enabling a full packaged style on
existing documentation yields hundreds of findings — the same adoption problem
[`code-quality/lint/`](../../software-engineering/code-quality/lint/README.md) describes for code,
made worse by being arguable. The narrow version is the one that works: **terminology rules only**,
which are objective and which are what actually drifts in a documentation set written over time.

| Check | Fails because | Blocking? |
|---|---|---|
| **Local links** | the tree moved and something was missed | **yes** — always our fault, always fixable |
| External links | a third party changed something | no — schedule it, report it |
| Terminology | a term does not match the project vocabulary | yes, once the vocabulary exists |
| Style rules — voice, wordiness | somebody wrote a sentence differently | only if the team genuinely agreed the rule |

Spelling sits next to these and is catalogued elsewhere, because it applies to code as much as to
prose: see [`typos`](../../software-engineering/code-quality/lint/typos/README.md) and
[`codespell`](../../software-engineering/code-quality/lint/codespell/README.md).

## Converting

Documentation frequently already exists — in Word, in Confluence, in a PDF someone produced for a
review. Retyping it is not a plan.

**Pandoc** is the tool. It converts between essentially every document format, and the recorded
experience here is worth carrying forward:

> `markitdown` — poor quality, does not work properly.
> `pandoc` — this one works. The installation is awkward; Docker is better. Use the shell script.

Running it through Docker avoids the installation entirely:

```bash
docker run --rm --volume "$(pwd):/data" --user $(id -u):$(id -g) \
  pandoc/core input.docx --extract-media=./ -o output.md
```

The conversion is the easy half. What follows always needs manual work:

| After conversion | Why |
|---|---|
| **Images** | extracted into `./media/`, often as `.tmp` files needing conversion to PNG |
| Width and height attributes | Pandoc emits `{width="..." height="..."}` that Markdown renderers show literally |
| Tables | complex Word tables convert badly, or not at all |
| Structure | Word heading styles map inconsistently to Markdown headings |

[`pandoc/convert.sh`](pandoc/convert.sh) automates the whole sequence — convert, move images,
turn `.tmp` files into PNG, strip the size attributes — which is the part that is tedious enough
to get wrong by hand.

One caveat about `.doc`: Pandoc reads `.docx`, not the older binary `.doc`. That has to be
converted first, and it is the one step the script cannot do.

## Anti-patterns

| Anti-pattern | Why it is bad | What to do instead |
|---|---|---|
| No linting | style drifts across a repository until nothing matches | markdownlint in CI |
| Linting with every rule enabled | line-length failures on every table, so everyone ignores it | disable the rules that fight the content |
| Code fences without a language | no syntax highlighting, and it is invisible in review | always specify it |
| No link checking | a folder rename breaks links silently and nothing reports it | lychee on every pull request |
| Blocking a merge on external URLs | the build fails because someone else's site is down, so people stop reading it | local links in the gate, external on a schedule |
| A full prose style enabled on day one | hundreds of arguable findings, so the tool is removed | terminology rules first, style later or never |
| A growing link-exclusion list nobody reads | it becomes the mechanism by which real breakage is ignored | keep it short, and comment each entry |
| Retyping an existing document | slow, and it introduces errors the original did not have | Pandoc |
| Committing converted output unreviewed | broken tables and literal `{width=...}` attributes in the published page | read it after converting |
| Converted images left as `.tmp` | they do not render | convert to PNG — the script does it |
| Lint failures that do not fail the build | an advisory linter is a disabled linter | fail the build, with rules you agree with |

## How this applies to pikakube

**Pandoc has real history here** — [`pandoc/`](pandoc/README.md) carries the working script and
the recorded comparison against `markitdown`, which is the kind of finding that is only made by
trying both.

**Checking is the gap, and link checking is the urgent half of it.** There are 1204 `README.md`
files under [`infrastructure/`](../../README.md), navigated entirely by relative links, and the
tree has been reorganised more than once — `tests/` became `testing/`, `code-review/` became
`code-quality/review/`. Every one of those moves silently broke inbound links that had to be found
by hand afterwards. [lychee](lychee/README.md) in offline mode finds them before the rename merges,
in seconds. This is the recommendation [`site-generator/`](../site-generator/README.md) has already
made twice without naming a tool.

**markdownlint is the second gap.** The consistency questions it checks — heading levels,
code-fence languages, list markers — are exactly the ones that drift across that many files written
across that many sessions. It is worth having, and it is worth less than link checking: a wrong
bullet character is cosmetic, and a link pointing at a folder that no longer exists is a broken
document.

**Vale is third, and only in its narrow form.** A vocabulary and a set of terminology rules would
find real drift in a catalogue of several hundred tool names; a packaged style guide would start an
argument. The order matters more than the list — a repository that adds all three at once fixes
none of them.

---

[← Documentation](../README.md)
