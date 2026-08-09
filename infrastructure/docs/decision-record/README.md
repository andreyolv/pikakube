[← Documentation](../README.md)

# Architecture decision records

The documentation that code cannot replace — why this, and what was rejected.

Tools covered: [`madr`](madr/README.md) · [`log4brains`](log4brains/README.md)

Reference: <https://github.com/joelparkerhenderson/architecture-decision-record>

## Contents

1. [The problem](#1-the-problem)
2. [What an ADR is](#2-what-an-adr-is)
3. [The format is not the point](#3-the-format-is-not-the-point)
4. [The tools](#4-the-tools)
5. [When to write one](#5-when-to-write-one)
6. [Anti-patterns](#6-anti-patterns)
7. [How this applies to pikakube](#7-how-this-applies-to-pikakube)

---

## 1. The problem

Code records what was built. It does not record:

- what the alternatives were
- why they were rejected
- what constraints forced the choice
- what would have to change for the decision to be revisited

That information lives in the heads of the people who were in the room, and it leaves when they
do. The observable symptoms are specific:

| Symptom | What is actually happening |
|---|---|
| The same argument, annually | nobody recorded the conclusion or the reasoning |
| "Why is it like this?" answered with a shrug | the constraint that forced it is forgotten |
| A decision reversed, then reversed back | the original trade-off was rediscovered the hard way |
| New engineers proposing what was already tried | the failure is undocumented |

An ADR is a short document that answers those four questions, written when the decision is made
and never edited afterwards.

## 2. What an ADR is

Five parts. It is short by design:

| Section | Content |
|---|---|
| **Title and status** | proposed, accepted, deprecated, superseded by ADR-00X |
| **Context** | the forces at play — constraints, requirements, what was already true |
| **Decision** | what was chosen, stated plainly |
| **Consequences** | what this makes easy, what it makes hard, what it rules out |
| **Alternatives considered** | the options rejected, **and why** |

The last section is the one that carries the value, and it is the one most often skipped. "We
chose Flux" is a fact anyone can read from the repository. "We chose Flux over Argo CD because
the workflow is manifest-first and the UI was not worth the extra components" is the decision.

The **immutability** property is what makes the format work. An ADR is not updated when the
decision changes — a new ADR is written that supersedes it. That preserves the history, which is
the entire purpose. A living document that is edited loses exactly the information it was
supposed to keep.

## 3. The format is not the point

Worth stating early, because ADR tooling attracts more attention than it deserves.

The value is in **having written the reasoning down**. Whether it is MADR, Nygard's original
template, or five headings in a Markdown file changes almost nothing. A repository with plain
`docs/adr/0001-*.md` files and no tooling is doing this correctly.

What matters, in order:

1. The reasoning exists in writing
2. It is next to the code, so it is found
3. It is immutable, so the history survives
4. It is numbered and linkable, so it can be referenced

Tooling helps with the fourth and adds a web interface. Neither is the reason to start.

## 4. The tools

| Tool | What it is | Where it shines | Detail |
|---|---|---|---|
| **MADR** | a Markdown template and a numbering convention | **the sensible default** — a template, not a dependency | [→](madr/README.md) |
| **Log4brains** | a CLI plus a generated static site | teams large enough that browsing and searching ADRs is a real need | [→](log4brains/README.md) |

Worth reading before either: the
[ADR collection](https://github.com/joelparkerhenderson/architecture-decision-record) is the
canonical set of templates and background, and the
[actions-runner-controller ADRs](https://github.com/actions/actions-runner-controller/tree/master/docs/adrs)
are a good example of the practice in a real project.

## 5. When to write one

Not for every decision. The test is whether someone will ask "why?" in a year.

| Write one | Do not |
|---|---|
| Choosing between tools that solve the same problem | routine implementation choices |
| A decision that is expensive to reverse | anything easily changed |
| Rejecting the obvious option, for a reason | following the obvious option for the obvious reason |
| Accepting a known trade-off deliberately | decisions with no trade-off |
| A constraint imposed from outside — licensing, compliance, an existing estate | preferences |
| Something that will look wrong without context | something self-evident from the code |

The last row is the most practical trigger. If a decision would make a competent newcomer say
"that is odd", it needs an ADR — that reaction is exactly the cost of the missing context.

## 6. Anti-patterns

| Anti-pattern | Why it is bad | What to do instead |
|---|---|---|
| No ADRs at all | every decision is relitigated, and the reasoning leaves with people | start with five headings in a file |
| Editing an accepted ADR | the history it existed to preserve is destroyed | supersede it with a new one |
| Omitting the alternatives | the most valuable section is the one that is missing | record what was rejected, and why |
| Writing them retroactively, in bulk | reconstructed reasoning is invented reasoning | write at the moment of decision |
| ADRs in a wiki | separate from the code, so nobody finds them | in the repository |
| One for every decision | volume buries the ones that matter | only where "why?" will be asked |
| Tool selection before the first ADR | the format was never the obstacle | write one in Markdown today |
| Marketing prose instead of trade-offs | a decision with no downsides was not a decision | state what it makes worse |

## 7. How this applies to pikakube

**This is the named gap in the repository.**

Every capability folder under [`infrastructure/`](../../) catalogues the alternatives and
explains the trade-offs, which is most of the work. What is missing is the other half: which
option was chosen *here*, and why.

The candidates are already visible in the existing documentation, each one a decision with a
recorded rationale and no ADR:

| Decision | Where the reasoning currently lives |
|---|---|
| Flux over Argo CD | [`platform-engineering/gitops/`](../../platform-engineering/gitops/README.md) |
| nip.io over a real domain for the local cluster | [`network/dns/`](../../network/dns/README.md) |
| CloudNativePG over the other Postgres operators | [`databases/sql/postgresql/operator/`](../../databases/sql/postgresql/operator/README.md) |
| READMEs rendered by GitHub, rather than a generated site | [`site-generator/`](../site-generator/README.md) |
| The capability-based folder taxonomy itself | nowhere |

The last row is the clearest example. The decision to organise `infrastructure/` by capability
on a single axis per level — rather than by tool or by vendor — shapes the entire repository, and
it is recorded nowhere. Someone arriving at it has to infer the rule from the structure.

**MADR in `docs/adr/` is the recommendation**, and the reason is section 3: the tooling is not
the obstacle, and Log4brains would add a build step to solve a browsing problem this repository
does not yet have.

Note that [`docs/docs-standard.md`](../../../docs/docs-standard.md) at the repository root already
proposes a `docs/tech/adr/` folder. It does not exist. Implementing that is a smaller task than
the standard makes it sound.

---

[← Documentation](../README.md)
