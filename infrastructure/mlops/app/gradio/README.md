[← Apps](../README.md)

# Gradio

<https://github.com/gradio-app/gradio>

---

## The problem it solves

You have a model and no way to show it to anybody. A notebook is not a demo, and a screenshot is
not evidence.

Gradio turns a Python **function** into a web interface. You declare what goes in and what comes
out — an image, a piece of text, an audio clip, a file, a chat turn — and it renders the widgets,
serves the page and wires them to the function. No HTML, no JavaScript, no build step.

Its design is function-shaped, and that has two consequences that matter more than the UI:

- **It is the right shape for a model demo.** Inputs → inference → outputs is exactly what a model
  is. There is no impedance mismatch to work around.
- **You get an API for free.** Because the function's inputs and outputs are declared, Gradio also
  exposes the same call as an HTTP endpoint with a generated client. The demo is simultaneously a
  callable service, which is a much bigger deal than it sounds — it means the demo can be scripted,
  tested and benchmarked.

It is also the ecosystem default: **most Hugging Face Spaces are Gradio apps**, and a large share
of published models ship with a Gradio demo. If you want your model to look like every other model
people have tried, this is the shape they expect.

## When to use it

- Showing what one model does, to people who will not run code.
- Chat interfaces over a model — the chat components are first-class and this is now one of the
  most common uses.
- Anything image, audio or video: the typed media components handle upload, preview and playback
  without work.
- Collecting human feedback or labels on model output — flagging is built in.
- When you want the demo and a callable endpoint to be the same artefact.
- Publishing to Hugging Face Spaces, where it is the path of least resistance.

## When not to use it

- **Dashboards.** Several charts, filters, a narrative, multiple pages — that is
  [Streamlit](../streamlit/README.md)'s shape, and fighting Gradio into it is unpleasant.
- Anything a real user base depends on. It is a prototype-grade server; see
  [`../README.md`](../README.md#3-the-operational-caveats).
- Complex multi-step flows with real application state. It can be done with `Blocks` and it stops
  being the easy path.
- Anywhere it would be exposed without an authenticating proxy in front — see the notes.

## Notes

The original note for this folder was the repository link alone: <https://github.com/gradio-app/gradio>.
No commentary was recorded, and nothing is deployed. What follows is the operational context that
belongs with it.

**`share=True` is the thing to be careful about.** One keyword argument creates a public tunnel to
the app running on your machine, reachable by anyone with the URL, for a limited time. It is
genuinely useful for a quick review and it is also the single easiest way to put an internal model
and whatever data it loads on the public internet. It should never appear in anything deployed.

**Authentication.** Gradio has a basic built-in auth option (a username/password callback). It is
not an identity system — no SSO, no groups, no audit trail. The correct pattern is an
authenticating proxy in front of the app, the same shape as the `oauth2_proxy` sidecar used for the
MLflow UI in [`../../lifecycle/mlflow/`](../../lifecycle/mlflow/README.md), documented under
`../../../security/2-cluster/identity-access/authentication/auth-proxy/`.

**Sessions and scaling.** Per-user state lives in the server process, and the app talks over
websockets. A second replica without sticky sessions breaks sessions unpredictably. One replica,
sized for the model, is the normal answer.

**Queueing.** Gradio has a built-in queue for concurrent requests, and it matters as soon as
inference is slower than a click. Without it, concurrent users appear to hang; with it, they wait
visibly. It is the correct answer to "the app freezes under load" — not more replicas.

**Model loading.** Load the model once, outside the request function. A model loaded inside the
handler is loaded per call.

**Where it fits here.** Nothing is deployed. If it were, the model should be pulled from the
registry in [`../../lifecycle/mlflow2/`](../../lifecycle/mlflow2/README.md) by version, rather
than baked into the image — that is the point of having a registry.

---

[← Apps](../README.md)
