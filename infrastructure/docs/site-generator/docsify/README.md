[← Site generators](../README.md)

# Docsify

<https://github.com/docsifyjs/docsify>

---

## The problem it solves

**No build step at all.** Docsify ships a single `index.html` that loads the Markdown files at
runtime and renders them in the browser.

There is no generated output, no `site/` directory, and nothing to publish beyond the files that
already exist. Editing a Markdown file changes the site immediately, because the site *is* the
Markdown files.

| | Docsify | Every other generator here |
|---|---|---|
| Build | **none** | a build step |
| Deploy | serve the repository | publish the generated output |
| Rendering | in the browser, at request time | ahead of time |
| Time to first site | one HTML file | a project |

## When to use it

- **an internal site** where the audience is a team, not a search engine
- documentation that should be servable straight from a repository or a static host
- no CI available, or no appetite for a build pipeline
- a small site where the build would be most of the work

## When not to use it

- **SEO matters** — content is rendered client-side, so crawlers see an almost empty page. This
  is the disqualifying limitation for anything public
- offline use, or any environment where JavaScript is not guaranteed
- large sites, where fetching Markdown per navigation becomes noticeable
- versioning, i18n, or a plugin ecosystem — [Docusaurus](../docusaurus/README.md)
- a polished technical documentation site with search that works well —
  [MkDocs Material](../mkdocs/README.md)

## The trade in one line

Everything Docsify gives you comes from rendering at runtime, and every limitation comes from the
same place. It is not a lesser MkDocs; it is a different answer to "must there be a build?"

## Notes

Not used here. Mapped as the option for the case where a build pipeline is genuinely the
obstacle — an internal reference served from a repository, with nothing between the Markdown and
the reader.

For this repository the equivalent role is already filled more simply: the capability
documentation is READMEs rendered by GitHub, which needs neither a build nor a host.

---

[← Site generators](../README.md)
