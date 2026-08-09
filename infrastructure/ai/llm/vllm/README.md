[← LLM](../README.md)

# vLLM

<https://github.com/vllm-project/vllm>

---

## The problem it solves

Serving a language model naively wastes almost all of the GPU you paid for. Two specific
inefficiencies do most of the damage, and vLLM's reputation rests entirely on fixing them.

**Requests arrive at different times and finish at different times.** Static batching waits for
a batch to fill, runs it, and waits for the slowest sequence in it to finish before starting
anything else. Short requests sit behind long ones, and the GPU idles between batches. vLLM uses
**continuous batching**: a finished sequence leaves the batch and a waiting request joins it at
the next token step. The batch is never drained and refilled — it is continuously topped up.

**The KV cache is allocated wastefully.** Every token generated must keep its attention
key/value tensors for the rest of the sequence, and a naive implementation reserves a
contiguous block sized for the maximum possible length. Most sequences never reach it, so most
of the reserved memory is never used, and fragmentation wastes more. **PagedAttention** applies
the operating-system idea of paging: the KV cache is stored in fixed-size non-contiguous blocks
with a block table mapping them, so memory is allocated as tokens are actually produced.

The consequence of the second one is the more interesting: because blocks are indirected through
a table, **blocks can be shared**. Several sequences with the same prefix — the same system
prompt, the same few-shot examples, the same document — point at the same physical blocks
instead of holding identical copies. That is prefix caching, and for workloads with a large
shared prompt it is a substantial win on both memory and time-to-first-token.

The practical result: far higher throughput per GPU than a naive server, which is the same thing
as a lower cost per token. It is also the reason vLLM is the **production default** for
self-hosted serving, and why alternatives generally have to explain themselves.

Around the core it provides the parts that make it a server rather than a library: an
OpenAI-compatible HTTP API — so any client and any [AI gateway](../../ai-gateway/README.md)
already speaks to it — tensor and pipeline parallelism for models too large for one GPU, support
for quantised weights, and metrics.

## When to use it

| Situation | Why vLLM |
|---|---|
| Serving a model to more than one concurrent user | continuous batching is exactly this case |
| GPU cost per token matters | throughput per GPU is the lever, and this is the lever |
| Many requests share a long prefix — RAG, fixed system prompts | prefix caching turns the shared part into a lookup |
| The model does not fit on one GPU | tensor parallelism, and multi-node with LeaderWorkerSet |
| Clients already speak the OpenAI API | drop-in server, no client changes |

## When not to use it

| Situation | Use instead |
|---|---|
| A developer laptop, or "let me try a model" | [Ollama](../ollama/README.md) — vLLM is a server, not a convenience |
| No GPU available | [llama.cpp](../llama-ccp/README.md) — vLLM is built for GPU |
| A handful of requests per day | the GPU idles at a fixed hourly cost; a hosted API is cheaper |
| Very heterogeneous small models, one per tenant | one process per model does not amortise; think about the total GPU count first |
| The model architecture is unusual or brand new | check support before committing; coverage is broad but not universal |

The economics deserve one blunt sentence. A GPU costs the same whether it is busy or idle, so
self-hosting only beats a hosted API above a utilisation threshold. vLLM lowers that threshold
substantially — it does not remove it. Work out the crossover before assuming self-hosting is
cheaper.

## Notes

The only thing recorded for vLLM in the original notes was the project URL:

- <https://github.com/vllm-project/vllm> — the project. Originated at UC Berkeley, now a
  PyTorch Foundation project.

**Nothing is deployed.** There are no manifests in this folder. What is deployed for model
serving in this repository is [Ollama](../ollama/README.md), which is the developer-experience
option and not a production server — see the parent folder for what that gap means.

Two things to know before deploying it, neither of which is a vLLM problem specifically:

**Cold start is brutal.** Weights have to be pulled and loaded into GPU memory. For a large
model that is minutes, and it happens on every pod restart, every rollout and every node
replacement. Plan for warm capacity rather than assuming Kubernetes can reschedule an inference
pod the way it reschedules a stateless API.

**GPU memory is the sizing constraint, and it is not just the weights.** The KV cache grows with
concurrency and context length, and vLLM pre-reserves a fraction of GPU memory for it. Getting
that fraction wrong is the difference between out-of-memory under load and a GPU that is
half-empty. Both are visible before production if the numbers are worked out first.

For models too large for a single node, the multi-node serving pattern is
`LeaderWorkerSet` — a leader pod coordinating worker pods that hold the remaining shards,
treated as one replica. That lives in
[`devops/advanced-workloads/lws/`](../../../devops/advanced-workloads/lws/README.md) in this
repository, and it is the piece that makes sharded serving a Kubernetes workload rather than a
manually assembled cluster.

---

[← LLM](../README.md)
