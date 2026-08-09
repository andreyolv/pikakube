[← Apps](../README.md)

# Streamlit

<https://github.com/streamlit/streamlit>

---

## The problem it solves

The team needs an internal tool — a dashboard, an exploration surface, a way to poke at a dataset
or compare model versions — and the options are a BI tool that cannot run Python, or a frontend
project nobody has time for.

Streamlit makes a **Python script a web application**. You write it top to bottom; every widget is
a function call that returns its current value; when anything changes, the script re-runs and the
page re-renders. Multi-page apps, layouts, dataframes, charts and file uploads are all in the box.

It is deliberately **general** where [Gradio](../gradio/README.md) is model-shaped. Gradio assumes
inputs → function → outputs. Streamlit assumes nothing: it is as comfortable being a data-quality
dashboard or an internal admin panel as a model demo. That generality is the reason to pick it and
the reason it is more scaffolding than Gradio for a single-model demo.

## When to use it

- Dashboards and exploration tools for the team — the case it is best at.
- Anything with several views, filters and a narrative, or genuinely multi-page.
- Internal tooling that is mostly reading data and rendering it: pipeline status, dataset
  profiling, model comparison across runs.
- When the logic is pandas-and-plots rather than a single inference call.
- When the audience is internal and the alternative is a spreadsheet that gets emailed around.

## When not to use it

- A single-model demo. [Gradio](../gradio/README.md) is less code and gives you an API endpoint as
  well.
- Anything a real user base depends on. It is a prototype-grade server; see
  [`../README.md`](../README.md#3-the-operational-caveats).
- Apps with real client-side interaction requirements. The rerun model puts every interaction
  through a server round trip.
- High-concurrency use. Every session is a server-side script execution holding memory.
- Anywhere it would be exposed without an authenticating proxy in front — see the notes.

## Notes

The original note for this folder was the repository link alone: <https://github.com/streamlit/streamlit>.
No commentary was recorded, and nothing is deployed. What follows is the operational context that
belongs with it.

**The rerun model is the thing to understand first.** Any widget interaction re-executes the entire
script from line one. This is what makes the programming model simple and it is also why an app
that loads a 4 GB model or runs a 30-second query feels broken — that work happens again on every
click. The fix is explicit caching (`st.cache_resource` for models and connections,
`st.cache_data` for dataframes). **Most "Streamlit is slow" reports are an uncached load in a
rerun.**

**Sessions and scaling.** Session state lives in the server process, per connected user, and the
browser holds a websocket. Two replicas without sticky sessions means a user's next interaction can
land on a pod that has never seen their session. One replica, sized deliberately, is the normal
answer; sticky sessions at the ingress if there must be more.

**Memory.** Each session holds its own state, and cached resources are per process rather than
shared across replicas. Memory grows with concurrent users, not with request rate — which means
the pod needs a limit chosen on purpose, not left off.

**Authentication.** Streamlit's open-source server has no meaningful authentication. As with the
MLflow UI in [`../../lifecycle/mlflow/`](../../lifecycle/mlflow/README.md), the pattern is an
authenticating proxy in front of it — documented under
`../../../security/2-cluster/identity-access/authentication/auth-proxy/`. A Streamlit app is
usually connected to a database or a data lake with credentials in its environment, so an open
Streamlit endpoint is an open endpoint to whatever it can read. That is a larger blast radius than
it looks.

**Keep the logic out of the app file.** The rerun model makes it tempting to put queries,
transformations and business rules inline. What results is a UI script that cannot be tested,
reused or run headless. Import a library; let the app be the view.

**Where it fits here.** Nothing is deployed. The obvious first use on this platform is a view over
the [MLflow](../../lifecycle/mlflow2/README.md) tracking data — comparing runs and registered
versions with the team's own framing rather than the built-in UI.

---

[← Apps](../README.md)
