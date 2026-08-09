[← Authoring](../README.md)

# Pandoc

<https://github.com/jgm/pandoc>

---

## The problem it solves

Documentation frequently already exists — in Word, in a PDF produced for a review, in something
exported from Confluence. Retyping it into Markdown is slow and introduces errors the original
did not have.

Pandoc converts between essentially every document format, and for this repository the case that
matters is `.docx` → Markdown.

## When to use it

- **existing documents** that should become Markdown in the repository
- a one-off migration of a body of documentation
- generating PDF from Markdown, where LaTeX quality matters

## When not to use it

- content that will keep being edited in Word — converting it once just creates two versions
- as a substitute for rewriting; conversion preserves the structure, including the bad structure
- large-scale conversion without reviewing the output, which is always needed

## Running it

Installation is awkward; Docker avoids it entirely:

```bash
docker run --rm --volume "$(pwd):/data" --user $(id -u):$(id -g) \
  pandoc/core input.docx --extract-media=./ -o output.md
```

One thing the command cannot do: Pandoc reads `.docx`, not the older binary `.doc`. That has to
be converted first — <https://cloudconvert.com/doc-to-docx> or equivalent.

## What always needs cleaning up afterwards

The conversion is the easy half:

| Issue | Detail |
|---|---|
| **Images** | extracted into `./media/`, often as `.tmp` files that do not render |
| **Size attributes** | Pandoc emits `{width="..." height="..."}`, which most renderers show literally |
| Tables | complex Word tables convert badly, or not at all |
| Structure | Word heading styles map inconsistently to Markdown headings |
| Lists | nested and numbered lists frequently need manual repair |

[`convert.sh`](convert.sh) automates the mechanical part of this — convert, move images out of
`./media/` into `./images/`, turn `.tmp` files into PNG, rewrite the paths, and strip the size
attributes. That sequence is tedious enough to get wrong by hand, which is why it exists.

Set `FILENAME` at the top of the script before running it.

## Notes

Recorded from actually doing this:

> **markitdown** — <https://github.com/microsoft/markitdown> — poor quality, does not work
> properly.
>
> **pandoc** — this one works. The installation is bad; Docker is better. Use the shell script.

That comparison is the useful finding, and it is the kind that only comes from trying both.
Microsoft's converter looks like the obvious choice for Office formats and is not.

Also worth knowing about, from the original notes:
[confluence-docs-as-code](https://github.com/Workable/confluence-docs-as-code) goes the other
direction — publishing Markdown from a repository *into* Confluence, which is the pragmatic
answer when Confluence is where the organisation looks. See
[`site-generator/`](../../site-generator/README.md#4-hosting).

---

[← Authoring](../README.md)
