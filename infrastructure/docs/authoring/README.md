[← Documentation](../README.md)

# Authoring

Keeping the Markdown consistent, and getting existing material into it.

Tools covered: [`markdownlint`](markdownlint/README.md) · [`pandoc`](pandoc/README.md)

---

## Two jobs

| Job | Question | Tool |
|---|---|---|
| **Lint** | is the Markdown consistent, and does it render as intended? | [markdownlint](markdownlint/README.md) |
| **Convert** | how does an existing Word document become Markdown? | [Pandoc](pandoc/README.md) |

They sit together because both are about the *source text* rather than the published output —
the layer beneath [`site-generator/`](../site-generator/README.md).

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
| Retyping an existing document | slow, and it introduces errors the original did not have | Pandoc |
| Committing converted output unreviewed | broken tables and literal `{width=...}` attributes in the published page | read it after converting |
| Converted images left as `.tmp` | they do not render | convert to PNG — the script does it |
| Lint failures that do not fail the build | an advisory linter is a disabled linter | fail the build, with rules you agree with |

## How this applies to pikakube

**Pandoc has real history here** — [`pandoc/`](pandoc/README.md) carries the working script and
the recorded comparison against `markitdown`, which is the kind of finding that is only made by
trying both.

**markdownlint is the gap, and it is now the relevant one.** This repository contains several
hundred Markdown files written across many sessions, and the consistency questions it checks —
heading levels, code-fence languages, list markers — are exactly the ones that drift at that
scale.

Paired with the link checking noted in [`site-generator/`](../site-generator/README.md), those
are the two CI checks that would have caught real problems in this repository rather than
hypothetical ones.

---

[← Documentation](../README.md)
