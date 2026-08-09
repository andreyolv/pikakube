[← LLM](../README.md)

# Ollama

<https://github.com/ollama/ollama>
<https://github.com/otwld/ollama-helm>

Subfolder: [`open-webui/`](open-webui/README.md) — the chat interface in front of it

---

## The problem it solves

Getting a local model running used to mean choosing a runtime, finding weights, picking a
quantisation, converting the format, and writing a serving script. Ollama collapses all of that
into `ollama run <model>`. It pulls the weights, picks a sensible quantisation, loads them,
starts an HTTP server and drops you into a prompt.

What it actually provides:

| Feature | What it removes |
|---|---|
| A model registry with a pull/run interface | finding and converting weights by hand |
| Automatic quantisation selection | guessing which GGUF variant fits the hardware |
| Model lifecycle — load on demand, unload when idle | manual process management |
| An HTTP API, including an OpenAI-compatible surface | writing a serving wrapper |
| `Modelfile` | a repeatable way to pin a model with its system prompt and parameters |

It uses [llama.cpp](../llama-ccp/README.md) underneath and serves GGUF models, so its
capabilities and its quantisation trade-offs are that project's.

**Ollama is a developer-experience tool, not a production inference server.** That is not a
criticism — it is what it optimises for, and it is the best thing in this folder at it. But the
distinction decides where it belongs:

| | Ollama | [vLLM](../vllm/README.md) |
|---|---|---|
| Concurrency model | serves requests, but not built around batching throughput | continuous batching, the core design |
| Memory | loads and unloads models on demand | pre-reserves, sized deliberately |
| Multi-GPU sharding | not the target | tensor and pipeline parallelism |
| Optimised for | one user getting started in a minute | many users, cost per token |

Under concurrent load the gap is large, and it is architectural rather than a matter of tuning.

## When to use it

| Situation | Why Ollama |
|---|---|
| Local development against a real model | one command, no setup |
| An internal, low-traffic assistant | convenience outweighs throughput at this scale |
| Comparing several models quickly | pull, run, discard |
| A default backend so other components have something to talk to | this is exactly its role here — see the notes |
| No provider key, and data must stay in the cluster | self-hosted end to end |

## When not to use it

| Situation | Use instead |
|---|---|
| A user-facing product path | [vLLM](../vllm/README.md) |
| Concurrency beyond a handful of users | vLLM; the difference shows up immediately |
| Models too large for one GPU | vLLM with sharding, and `LeaderWorkerSet` for multi-node |
| Predictable latency matters | on-demand load/unload means a cold request can wait for a model to load |
| Cost per token is being measured | you are optimising the wrong layer |

## Notes

Recorded in the original notes, with what each one means:

- <https://github.com/ollama/ollama> — the project.
- <https://github.com/otwld/ollama-helm> — the community Helm chart, and the one deployed here.
  Note "community": it is not maintained by the Ollama project, which is worth knowing when a
  chart option and an Ollama feature disagree.
- <https://github.com/deepseek-ai/DeepSeek-V3> — recorded alongside them. A large open-weights
  model. Its presence in these notes reads as "a model worth watching" rather than anything
  deployed; at full size it is far beyond a single-node Ollama deployment, so treating it as a
  candidate here would mean sharded serving on real GPUs, not this.

The recorded commands, and what each one is for:

```
ollama run qwen3:8b     # pull if needed, load, and open an interactive prompt
ollama list             # models present on disk
ollama ps               # models currently loaded in memory, and on what
ollama stop qwen3:8b    # unload from memory; the weights stay on disk
ollama rm qwen3:8b      # delete the weights from disk
nvidia-smi              # GPU utilisation and memory, from outside Ollama
```

Two of these are more useful than they look. **`ollama ps` versus `ollama list`** is the
distinction between what is on disk and what is occupying memory — the answer to "why is the GPU
full when I am not using it", since a model stays loaded for a while after its last request.
And **`nvidia-smi` is the check that Ollama is using the GPU at all**: it will fall back to CPU
silently if the driver, the container runtime or the device plugin is not set up, and the only
symptom is that everything is slow. Run it before concluding a model is bad.

`qwen3:8b` is the model in the recorded commands. The `:8b` is the parameter count — the tag
selects both the size and the quantisation variant, which is the main lever for fitting a model
onto the hardware available.

**What is deployed here.** The `ollama` chart at version `0.21.1` from the `HelmRepository` at
`https://otwld.github.io/ollama-helm/`, into the `ollama` namespace, with empty values — chart
defaults.

**It is a dependency of other things in this repository, which raises the stakes.**
[kagent](../../agents/kagent/README.md) is configured with Ollama as its default model provider,
pointing at `http://ollama.ollama.svc.cluster.local:11434` with the `llama3.2` model. So the
cluster's agent platform runs on a developer-experience inference server with default chart
values. That works, and it is the right way to prove the path end to end without a provider key.
It is also the specific place where the Ollama-versus-vLLM distinction stops being theoretical:
whatever the agents can reliably do is capped by a small model, and whatever concurrency they
can sustain is capped by this server.

**Empty values leaves two questions open**: whether model storage is persistent — without it,
every restart re-pulls every model — and whether a GPU is requested at all, which the chart
controls and which `nvidia-smi` inside the pod will settle in one command.

---

[← LLM](../README.md)
