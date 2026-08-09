[← Authoring](../README.md)

# markdownlint

<https://github.com/DavidAnson/markdownlint>

---

## The problem it solves

Markdown is forgiving, which is why it drifts. Heading levels skip, bullet characters vary
between files, code fences lose their language, and none of it is visible in a diff — the diff
shows the fence, not the rendering.

Across a repository written over months, the result is a documentation set that reads as though
several people wrote it, which it effectively was.

| Rule class | What it catches |
|---|---|
| Heading structure | skipped levels, duplicates, a missing top-level heading |
| **Code fences** | a missing language, which is why highlighting is inconsistent |
| Lists | mixed markers, inconsistent indentation |
| Links | empty link text, bare URLs where a link was intended |
| Whitespace | trailing spaces, hard tabs, multiple blank lines |
| Line length | if the project has an opinion |

The code-fence rule is the one that pays for the setup. A fence without a language renders as
grey text, and nobody notices in review.

## When to use it

- more than a handful of Markdown files, written over time
- a documentation set that should read consistently
- CI exists, so it can fail the build rather than being advisory

## When not to use it

- a few files, where the drift is not real
- the rules cannot be agreed on, so failures would be routinely overridden — a linter people
  ignore is worse than none

## Configuring it so it stays useful

The single most important step is **disabling the rules that fight the content**. Two in
particular:

| Rule | Why to disable it |
|---|---|
| **MD013** — line length | fights with tables and long URLs, and fires constantly |
| **MD033** — inline HTML | sometimes the only way to get a result |

Left on, both generate enough noise that the real findings get lost, and the linter stops being
consulted.

```jsonc
// .markdownlint.jsonc
{
  "default": true,
  "MD013": false,   // line length — tables and URLs
  "MD033": false,   // inline HTML
  "MD024": { "siblings_only": true }  // repeated headings under different parents
}
```

`MD024` is worth the nuance rather than disabling: repeated headings are a problem within one
section and entirely normal across sibling sections — which is exactly the shape of the
capability READMEs in this repository.

## Running it

```bash
npx markdownlint-cli2 "**/*.md"
```

There is also a VS Code extension that reports inline while writing, which catches most issues
before they reach CI.

## Notes

**Not present here, and it is now the relevant gap.**

This repository contains several hundred Markdown files written across many sessions, and the
consistency questions it checks — heading levels, code-fence languages, list markers, repeated
headings — are exactly the ones that drift at that scale.

Paired with the **link checking** noted in
[`site-generator/`](../../site-generator/README.md), those are the two CI checks that would catch
real problems in this repository rather than hypothetical ones. The tree has been reorganised
more than once, and a moved folder breaks links silently.

Of the two, link checking has the higher return. A wrong bullet character is cosmetic; a link
pointing at a folder that no longer exists is a broken document.

---

[← Authoring](../README.md)
