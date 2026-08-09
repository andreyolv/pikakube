[← Diagrams](../README.md)

# awsdac — Diagram as Code for AWS

<https://github.com/awslabs/diagram-as-code>

---

## The problem it solves

AWS architecture diagrams from a **declarative YAML file**, using AWS's own icon set — from AWS
themselves, so the icons and the conventions match what appears in their documentation.

The difference from [Diagrams](../diagrams/README.md) is the input format rather than the output:

| | awsdac | Diagrams |
|---|---|---|
| Input | **YAML** | Python |
| Clouds | AWS only | AWS, Azure, GCP, Kubernetes, on-premise |
| Icons | AWS official | community-maintained per provider |
| Programmable | no | **yes** — loops, generation from data |
| Dependencies | a single binary | Python plus Graphviz |
| Learning curve | read one example | write a program |

**YAML when the diagram is fixed; Python when it should be generated.** A declarative file is
easier to hand to someone who does not write Python, and it cannot express "draw one of these per
item in this list".

## When to use it

- **AWS-only** architecture, where matching AWS's own visual conventions is worth something
- a declarative file is preferable to a program for the people who will edit it
- a single binary is preferable to a Python environment plus Graphviz

## When not to use it

- multi-cloud or Kubernetes — [Diagrams](../diagrams/README.md) covers more providers
- the diagram should be generated from a list or a data source, which needs a real language
- a concept or flow rather than infrastructure — [Mermaid](../mermaid/README.md)
- what is actually deployed — [KubeDiagrams](../kubediagrams/README.md)

## Running it

```bash
awsdac aws.yaml
```

## Notes

Recorded from actually running it:

> ```
> Error: failed to create diagram: failed to create diagram: error scaling diagram:
> failed to prepare font face: failed to open font file: open : no such file or directory
> ```

The font path resolves to an empty string, so the binary cannot find a font to render labels
with. It is an environment problem rather than a problem with the definition file — the tool
expects a font available on the system and does not fall back to one.

Worth knowing before evaluating it: the failure is at render time, after the file has parsed,
which makes it look like a problem with the diagram when it is not. Supplying a font explicitly,
or running it in a container image that includes one, is the direction to fix it.

[`aws.yaml`](aws.yaml) is the definition kept here.

The comparison that matters for this repository: [Diagrams](../diagrams/README.md) runs and
produces output, and this does not — which for a tool whose only job is producing an image is
most of the evaluation.

---

[← Diagrams](../README.md)
