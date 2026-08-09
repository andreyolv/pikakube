[← LLM](../README.md)

# llama.cpp

<https://github.com/ggml-org/llama.cpp>

---

The directory name `llama-ccp/` is a **typo** for `llama.cpp` — `ccp` rather than `cpp`. Noted,
not renamed; a rename touches the GitOps path and is not a documentation change.

---

## The problem it solves

Every other serving option in this folder assumes a GPU. llama.cpp assumes nothing. It is a
C/C++ inference engine with no Python runtime, no CUDA requirement and no framework underneath
it, and it will run a model on a laptop CPU, on a Mac's unified memory, on a Raspberry Pi, or on
a GPU if one happens to be there.

Two of its contributions matter beyond the project itself.

**GGUF** is the model file format it defines: weights, tokeniser, metadata and quantisation
parameters in one file that memory-maps directly. It has become the de facto format for local
model distribution — [Ollama](../ollama/README.md) uses llama.cpp underneath, and a large share
of the "local model" ecosystem is GGUF files.

**Quantisation is what makes any of this viable.** A model's weights are normally 16-bit floats.
Quantisation stores them at lower precision — commonly 4-bit — which cuts memory roughly
proportionally, at some cost in output quality. That is the whole reason a model that nominally
needs a data-centre GPU can answer questions on a laptop. The trade is real and not free:
smaller quantisations are faster and cheaper and progressively worse, and the degradation is not
uniform across tasks. Reasoning and code suffer before casual conversation does.

It also ships `llama-server`, an HTTP server with an OpenAI-compatible endpoint, so it can sit
behind the same clients and the same [AI gateway](../../ai-gateway/README.md) as anything else.

The honest positioning: llama.cpp is optimised for **making inference possible on modest
hardware**, not for maximising throughput on expensive hardware. On a GPU under concurrent load,
[vLLM](../vllm/README.md) wins and it is not close — continuous batching and PagedAttention are
throughput mechanisms that llama.cpp does not set out to match.

## When to use it

| Situation | Why llama.cpp |
|---|---|
| There is no GPU and there will not be one | it is the only option here that treats CPU as first class |
| Edge or on-premise nodes with modest hardware | small binary, no runtime, no accelerator assumption |
| Local development on a laptop, including Apple silicon | Metal support and unified memory work well |
| You need a specific GGUF quantisation | this is the project that defines them |
| Deployment must be a single binary | no Python environment to reproduce |

## When not to use it

| Situation | Use instead |
|---|---|
| Serving many concurrent users on a GPU | [vLLM](../vllm/README.md) — this is not the same job |
| You want convenience over control | [Ollama](../ollama/README.md), which wraps it |
| Quality is the binding constraint | heavy quantisation is the thing costing you quality; a bigger model on real hardware is the fix |
| The workload is throughput-bound | CPU inference is slow per token, and no amount of tuning changes the order of magnitude |

## Notes

The only thing recorded for llama.cpp in the original notes was the project URL:

- <https://github.com/ggml-org/llama.cpp> — the project. Note the organisation: `ggml-org`,
  after the `ggml` tensor library the project is built on and which GGUF is named for.

**Nothing is deployed.** There are no manifests in this folder. Its practical relevance to this
repository is indirect but real: [Ollama](../ollama/README.md), which *is* deployed, uses
llama.cpp underneath and serves GGUF models. Understanding quantisation levels and their quality
cost is therefore not optional trivia here — it is the mechanism behind the models actually
running on the cluster.

---

[← LLM](../README.md)
