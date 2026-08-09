[← Diagrams](../README.md)

# Diagrams

<https://github.com/mingrammer/diagrams>

---

## The problem it solves

Cloud architecture diagrams written as **Python**, with the real provider icon sets — AWS, Azure,
GCP, Kubernetes, on-premise.

The output is what [Mermaid](../mermaid/README.md) cannot produce: a polished diagram with
recognisable service icons, suitable for a design document or a presentation. The input is code,
so it still diffs, still gets reviewed, and can still be regenerated.

```python
from diagrams import Diagram, Cluster
from diagrams.aws.compute import EKS
from diagrams.aws.database import RDS

with Diagram("platform", show=False):
    with Cluster("cluster"):
        EKS("workloads") >> RDS("postgres")
```

Being a program is the real differentiator: a diagram can be built from a list, so twenty
services with consistent styling is a loop rather than twenty copy-pasted shapes.

## When to use it

- **cloud architecture** for a document, a review, or a presentation
- vendor icons are part of what makes it legible to the audience
- the diagram is repetitive enough that generating it beats drawing it
- it must be regenerated as the architecture changes

## When not to use it

- a concept, a flow, or a decision tree — [Mermaid](../mermaid/README.md), inline, no build
- the diagram should reflect **what is actually deployed** —
  [KubeDiagrams](../kubediagrams/README.md) reads the manifests
- AWS only, and a declarative file is preferable to code —
  [awsdac](../aws-dac/README.md)
- explaining an idea informally — [Excalidraw](../excalidraw/README.md)

## The cost

| Concern | Detail |
|---|---|
| **Graphviz** | a system dependency, not a Python one; it must be installed separately |
| Output is an image | the PNG has to be committed alongside the source, or generated in CI |
| Layout | Graphviz decides it; the same constraint as Mermaid, with more nudging available |
| Rendering | not inline anywhere — the image is referenced, the source is a separate file |

The second row is the trade against Mermaid. A generated image can go stale if the script is not
re-run, so if the image is committed, regenerating it in CI is what keeps the guarantee.

## Running it

The project here uses `uv`:

```bash
uv run python aws.py
```

Which produces [`aws_architecture.png`](aws_architecture.png) from
[`aws.py`](aws.py) — the source and its output side by side, which is the shape this tool
implies.

## Related

Worth knowing about, from the original notes:

| Project | What it is |
|---|---|
| [KubeDiagrams](https://github.com/philippemerle/KubeDiagrams) | generates from Kubernetes manifests — see [`kubediagrams/`](../kubediagrams/README.md) |
| [Diagrams-as-Code](https://github.com/HariSekhon/Diagrams-as-Code) | a large collection of ready-made examples using this library |
| [Kubernetes-configs](https://github.com/HariSekhon/Kubernetes-configs) | the accompanying manifest collection |
| [diagram-as-code](https://github.com/awslabs/diagram-as-code) | AWS's own, YAML rather than Python — [`aws-dac/`](../aws-dac/README.md) |

The Diagrams-as-Code collection is the fastest way to get useful output: most architecture
diagrams are variations on an existing example rather than something new.

## Notes

Present here as a working example — a Python project with `pyproject.toml`, a lockfile, a script
and its rendered PNG.

Worth being aware that it is a **hand-written** architecture diagram, with all the usual
consequences: it describes what someone drew, not what is deployed. For that guarantee, the tool
is [KubeDiagrams](../kubediagrams/README.md), which is the notable absence in this folder given
how many manifests this repository contains.

---

[← Diagrams](../README.md)
