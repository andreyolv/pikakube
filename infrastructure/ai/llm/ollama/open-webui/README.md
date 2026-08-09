[← Ollama](../README.md)

# Open WebUI

<https://github.com/open-webui/open-webui>
<https://github.com/open-webui/helm-charts>

---

## The problem it solves

A model server exposes an HTTP API. People do not use an HTTP API. Without a front end, a
self-hosted model is available to whoever will write a `curl` command, which is not the audience
that justifies running it.

Open WebUI is the chat interface for that gap — a self-hosted front end that talks to
[Ollama](../README.md) and to any OpenAI-compatible endpoint, which includes
[vLLM](../../vllm/README.md) and anything behind an
[AI gateway](../../../ai-gateway/README.md). It provides the things people expect from a chat
product and would otherwise have to build:

| Capability | Why it matters here |
|---|---|
| Chat UI with conversation history | the thing that makes a model usable by non-engineers |
| Multiple backends, side by side | compare models without changing anything server-side |
| Accounts, groups and role-based access | who may use which model is a question you will be asked |
| Document upload with retrieval | the most common first request after "can we chat with it" |
| Model presets and system prompts | a shared, named configuration rather than everyone's private prompt |

Its strategic value is narrower than the feature list suggests: it makes a self-hosted model
**demonstrable**. The difference between "we run a model on the cluster" and "here is the link"
is most of the difference between an experiment and something a team uses.

The trade to be aware of is that it becomes a real application very quickly. It holds user
accounts, conversation history and uploaded documents. That is a database, a storage volume,
authentication and a retention policy — an application to operate, not a viewer.

## When to use it

| Situation | Why Open WebUI |
|---|---|
| A self-hosted model needs to be usable by people | it is the shortest path from endpoint to product |
| Several models should be compared by their actual users | backend switching in the UI |
| A private alternative to a hosted chat product is the goal | nothing leaves the cluster |
| Access control by team is required | groups and RBAC are built in |

## When not to use it

| Situation | Use instead |
|---|---|
| The model backs an application, not humans | call the API; a UI is not on the path |
| Nobody will own the accounts, storage and upgrades | do not deploy it — it is an application, not a dashboard |
| Chat history is sensitive and retention is undecided | decide that first; it stores everything by default |
| You only need a quick check that the model responds | `curl`, or `ollama run` |

## Notes

Recorded in the original notes:

- <https://github.com/open-webui/open-webui> — the project.
- <https://github.com/open-webui/helm-charts> — the official Helm charts.

**What is deployed here.** The `open-webui` chart at version `3.6.0`, into the `open-webui`
namespace, with empty values — chart defaults.

**There is a defect in the source configuration.** The `HelmRepository` for this chart points at
`https://otwld.github.io/ollama-helm/` — which is the community *Ollama* chart repository used
by the [parent folder](../README.md), not the Open WebUI chart repository linked above. The two
`HelmRepository` resources have different names but the same URL, which is the signature of a
copy-paste. Unless that repository happens to also serve an `open-webui` chart at 3.6.0, Flux
will not find the chart and the release will not reconcile. This should be checked against the
official `open-webui/helm-charts` repository and corrected — recorded here rather than fixed,
because this is a documentation pass and the fix is a manifest change.

**Empty values leaves the same questions as everywhere else in this folder**, and they matter
more here because this component holds state: persistence for the database and uploaded
documents, whether authentication is enabled, and which backend URL it points at. A chat UI that
loses every conversation on a pod restart will be abandoned faster than it was deployed.

---

[← Ollama](../README.md)
