[← Authoring](../README.md)

# Vale

<https://github.com/vale-cli/vale>

---

## The problem it solves

A grammar checker asks whether a sentence is correct. Vale asks a different question: **does this
sentence follow the style guide we said we would follow?**

That distinction is the entire point of the tool, and it is why it belongs next to a linter rather
than next to a spell checker. Correct prose can still be wrong for a documentation set — the wrong
term for a component, a heading capitalised differently from every other heading, a paragraph in
the passive voice where the surrounding pages are direct.

| What it checks | Example |
|---|---|
| **Terminology** | the same component called three different things across the tree |
| **Banned or discouraged words** | vague qualifiers, marketing language, terms the project decided against |
| Passive voice | *"the cluster is bootstrapped by the script"* |
| Wordiness | *"in order to"*, *"at this point in time"* |
| Heading conventions | sentence case in one file and title case in the next |
| Inclusive language | via the `alex` style, if the project wants it |

Vale ships no opinions of its own. It is a rules engine, and the opinions come from **styles** —
packaged rule sets that get selected deliberately:

| Style | What it is |
|---|---|
| **Microsoft** | the Microsoft Writing Style Guide, aimed at technical documentation |
| **Google** | the Google developer documentation style guide, same territory, different calls |
| `write-good` | general readability — passive voice, weasel words, long sentences |
| `proselint` | a large collection of usage rules, considerably more opinionated |
| `alex` | inclusive-language checks only |

Custom rules are written in YAML, which is what makes the terminology case practical: a rule that
says *"this component is spelled this way and only this way"* is a few lines, and it is the rule
most worth having.

## When to use it

- **a large documentation set written over a long period**, where terminology has drifted
- more than one author, or one author across many months, which amounts to the same thing
- a project that has actually chosen a style guide and wants it enforced rather than remembered
- **terminology consistency specifically** — the strongest and least arguable use of the tool
- in CI, with a narrow rule set, once the existing findings are at zero

## When not to use it

- as a grammar or spell checker; that is a different job — see
  [`typos`](../../../software-engineering/code-quality/lint/typos/README.md) for spelling
- with a full style enabled on existing documentation on day one — the first run produces hundreds
  of findings and the reliable outcome is that the tool is removed
- where nobody will agree on the rules. Prose linting produces **opinions**, and an opinion that
  fails a build has to be one the team actually holds
- for a handful of files, where the inconsistency is not real

## Two mechanisms that decide whether it is usable

**It understands markup.** Vale parses Markdown, HTML, reStructuredText and source-code comments,
so it lints prose and skips code blocks, inline code, URLs and front matter. Without that, every
code fence in a technical document becomes a wall of findings and the tool is unusable on the first
run. This is the property that separates it from running a general prose checker over the files.

**The vocabulary.** Each project defines accept and reject lists — a vocabulary of terms that are
correct despite not being words. Product names, tool names, acronyms, deliberate spellings. Without
it Vale flags every proper noun in a technical repository; with it, the same mechanism becomes the
terminology enforcement described above, because the reject list is where *"do not call it this"*
is recorded.

Curating the vocabulary is the real setup cost, and it is unavoidable. A repository documenting
several hundred tools has several hundred names that are not English words.

## Adopting it on documentation that already exists

The same problem [`lint/`](../../../software-engineering/code-quality/lint/README.md) describes for
code linters, and prose is worse because the findings are subjective. Enabling the Microsoft style
across an existing documentation set yields hundreds of results, most of which somebody will
disagree with.

| Approach | How |
|---|---|
| **Start with terminology only** | custom vocabulary rules, no packaged style — near-zero false positives, immediate value |
| **Ratchet** | add one rule class at a time, fixing as it is enabled |
| **New and changed files only** | gate the diff, not the tree |
| Choose one style, not several | Microsoft and Google contradict each other in places |

The recommended order is that first row. Terminology rules are objective — either the component is
called what the project decided or it is not — and they carry none of the argument that passive-voice
findings do.

## Notes

Written in Go, distributed as a binary and a container image, with an editor extension and a
GitHub Action. Styles are installed into a local folder from a package index, and the whole
configuration is one file plus the vocabulary.

**Not present in this repository, and it is a lower priority than the other gap.** The two checks
already identified — [link checking](../lychee/README.md) and
[Markdown linting](../markdownlint/README.md) — find defects. Vale finds inconsistencies, and the
difference in urgency is real: a broken link is a broken document, while an inconsistent heading
style is a document that reads slightly wrong.

That said, this repository is exactly the shape Vale's strongest case describes. It is a large
documentation set, written across many sessions, cataloguing hundreds of tools whose names have to
be spelled consistently to be searchable — and searchability is the practical reason terminology
consistency matters, more than the aesthetic one.

The narrow adoption is the defensible one: **a vocabulary and a set of terminology rules, no
packaged style**. That is a check that would find real drift without starting an argument about
the passive voice.

---

[← Authoring](../README.md)
