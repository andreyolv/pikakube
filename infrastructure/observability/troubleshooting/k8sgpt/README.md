[← Troubleshooting](../README.md)

# k8sgpt

<https://github.com/k8sgpt-ai/k8sgpt>
<https://github.com/k8sgpt-ai/k8sgpt-operator>

---

## The problem it solves

Scans the cluster for **known failure patterns** — failing pods, broken Services, unbound
PVCs, misconfigured Ingress — and reports what is wrong in plain language.

The scan itself is rule-based and needs no LLM. The `--explain` flag adds a model on top,
turning "readiness probe failed" into an explanation and a suggested fix.

That split matters: the useful half works offline, and the AI is optional.

## When to use it

- you want an immediate list of what is broken, with no setup
- onboarding someone to a cluster — it surfaces problems people had stopped noticing
- CI or a scheduled check, via the operator, to catch drift

## When not to use it

- the problem is below the application layer — [Inspektor Gadget](../inspektor-gadget/README.md)
- you need investigation across alerts and history — [HolmesGPT](../holmesgpt/README.md)
- `--explain` is off the table for data-handling reasons; the plain scan still works

---

## Notes

```bash
k8sgpt version
k8sgpt generate

k8sgpt auth add --backend openai --model gpt-3.5-turbo
k8sgpt auth list

k8sgpt analyze
k8sgpt analyse --explain
k8sgpt analyze --explain --filter=Pod --namespace=default
```

Integrations, including a Trivy-backed vulnerability analyser:

```bash
k8sgpt integrations list
k8sgpt integration activate trivy
k8sgpt analyze --filter VulnerabilityReport
```

> `analyze` runs locally. Only `--explain` sends anything to a model — worth knowing before
> pointing it at a production cluster.

---

[← Troubleshooting](../README.md)
