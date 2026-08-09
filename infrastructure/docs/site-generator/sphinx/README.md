[← Site generators](../README.md)

# Sphinx

<https://github.com/sphinx-doc/sphinx>

---

## The problem it solves

It is the only tool in this folder that generates reference documentation **from source code**.

`autodoc` reads modules, classes and functions, extracts their docstrings and signatures, and
produces a reference that cannot drift from the implementation — because it is derived from it.
The others publish Markdown someone wrote; this one publishes what the code says.

That is a different job, and it is why Sphinx is the standard across the Python ecosystem — the
Python language documentation itself is built with it.

| Capability | Why it is distinctive |
|---|---|
| **autodoc** | the API reference is generated from docstrings |
| **Cross-references** | `:class:` and `:func:` roles link across the whole project, and break the build when the target is gone |
| **intersphinx** | link into *other* projects' documentation by object name |
| doctest | examples in docstrings executed as tests |
| Multiple outputs | HTML, PDF via LaTeX, ePub, man pages |

The cross-reference behaviour is worth singling out. A reference to a function that has been
renamed fails the build, which makes it the only setup here where the documentation is checked
against the code by construction.

## When to use it

- the output includes a **Python API reference**
- documentation and code should be verified against each other
- PDF output is a requirement — LaTeX is a genuine advantage
- the project is a library, where consumers read signatures rather than guides

## When not to use it

- the content is prose with no API surface — [MkDocs](../mkdocs/README.md) is far less work
- the team writes Markdown and will not write reStructuredText
- a documentation product with versions and translations —
  [Docusaurus](../docusaurus/README.md)
- the project is not Python; other ecosystems have their own generators

## The reStructuredText question

Sphinx's native format is reStructuredText, not Markdown, and this is the main obstacle to
adopting it. RST is more capable — its directive and role system is what makes the
cross-referencing work — and it is unfamiliar to most people now.

**MyST** resolves it: Markdown with the Sphinx directives available, so prose is written in
Markdown while `autodoc` and cross-references still work. It is the sensible default for a new
Sphinx project and removes the usual reason people reject the tool.

## Sphinx or MkDocs

| | Sphinx | MkDocs |
|---|---|---|
| Generates from source code | **yes** | no |
| Cross-references checked at build | **yes** | no |
| Native format | RST, or Markdown via MyST | Markdown |
| PDF | strong | weak |
| Setup effort | real | minimal |
| Best at | **reference** | **guides** |

The bottom row is the summary. Many projects want both, and running MkDocs for the guides
alongside a generated API reference is a reasonable outcome rather than a failure to decide.

## Notes

Not used here. It is mapped for the case this repository does not currently have: a Python
package whose documentation should include a generated API reference.

The nearest candidates would be the Python projects that already exist in the tree — the
[Diagrams](../../diagram/diagrams/README.md) definitions and the Airflow DAGs — neither of which
is a library with consumers reading signatures.

---

[← Site generators](../README.md)
