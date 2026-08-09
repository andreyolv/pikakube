[← Site generators](../README.md)

# MkDocs

<https://github.com/mkdocs/mkdocs>
<https://github.com/squidfunk/mkdocs-material>
<https://github.com/oprypin/mkdocs-section-index>

---

## The problem it solves

Markdown in a repository, a static site out, configured by one YAML file. There is no project to
scaffold, no framework to learn, and no JavaScript build — which is why it is the default for
technical documentation.

**Material** is the theme that made it the default. Search, navigation, dark mode, versioning,
admonitions, tabbed code blocks and Mermaid rendering all arrive configured, and it is what
almost every MkDocs site you have seen is using.

## When to use it

- **technical documentation that is prose** — guides, references, runbooks
- the source should stay plain Markdown, readable on GitHub without the site
- publishing to GitHub Pages, where `gh-deploy` is a single command
- you want a site and not a front-end project

## When not to use it

- the output includes an API reference generated from source code —
  [Sphinx](../sphinx/README.md)
- multiple documentation versions live simultaneously, with translations and React components —
  [Docusaurus](../docusaurus/README.md)
- a build step is unwanted — [Docsify](../docsify/README.md) renders in the browser
- GitHub's own rendering is already sufficient, which is a legitimate end state

## Working with it

The environment here is Poetry:

```bash
poetry lock
poetry install
```

To get into the virtualenv, `poetry env activate` prints the command rather than running it:

```bash
eval "$(poetry env activate)"
```

A shell alias is more convenient day to day:

```bash
echo "alias venv='source \"\$(poetry env info --path)/bin/activate\"'" >> ~/.bashrc
```

Or skip activation entirely with `poetry run <command>`. To start over,
`poetry env remove --all`.

Then the three commands that matter:

```bash
mkdocs serve      # live reload on http://127.0.0.1:8000
mkdocs build      # static site into site/
mkdocs gh-deploy  # build and push to the gh-pages branch
```

`gh-deploy` is the reason MkDocs and GitHub Pages are paired so often — it commits the built site
to `gh-pages` and pushes, in one step.

## What to configure deliberately

| Setting | Why |
|---|---|
| **`nav`** | maintained by hand; a page missing from it is invisible |
| `theme.features` | navigation tabs, instant loading and search suggestions are off by default |
| Mermaid | Material renders it via `superfences`, so diagrams work without a plugin |
| Versioning | `mike`, and only if versions genuinely coexist |
| `site_url` | required for the sitemap and for canonical links |

The `nav` block is the recurring maintenance cost.
[mkdocs-section-index](https://github.com/oprypin/mkdocs-section-index) reduces it by letting a
section header be a real page rather than a label with no content — which is what makes a large
tree navigable.

## Notes

The [portfolio site](../../../../portfolio/) is built with this, using the Material theme, `mike`
for versioning and GitHub Pages for hosting.

Worth being explicit about the split in this repository: the portfolio is a **site**, and the
capability catalogue under [`infrastructure/`](../../../README.md) is **READMEs rendered by GitHub**. The
second deliberately has no generator, because the folder tree is the navigation and a build step
would take that away rather than add to it.

---

[← Site generators](../README.md)
