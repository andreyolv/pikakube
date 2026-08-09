[← REST frameworks](../README.md)

# FastAPI

<https://github.com/fastapi/fastapi>

---

## The problem it solves

In most frameworks the same information is written three times: once as validation, once as
serialisation, and once as documentation. The three drift, and the one that drifts first is the
documentation, because it is the only one nothing tests.

FastAPI derives all three from the **type hints on the handler**. A Pydantic model in the signature
is the parser, the validator, the response schema and the OpenAPI definition at once. There is no
separate documentation artefact to maintain, so there is nothing to fall out of date.

```python
@app.post("/users")
def create_user(user: UserIn) -> UserOut:
    ...
```

That declaration alone produces request validation with structured `422` errors, response
filtering, and an OpenAPI document served at `/openapi.json`.

The second thing it brings is **ASGI**. It is built on Starlette, so `async` handlers, WebSocket
routes and streaming responses are available rather than being outside the model — see
[`framework/`](../README.md) section 2 for when that is a requirement and when it is a preference.

## When to use it

- a new Python service that will be maintained — the contract comes for free and stays true
- an **OpenAPI document is wanted** and nobody is going to hand-maintain one
- the handlers are I/O-bound: several upstream calls, waiting more than computing
- WebSocket, Server-Sent Events or streaming responses are needed alongside ordinary routes
- typed clients are to be generated for consumers from the schema

## When not to use it

- the work is **CPU-bound** — `async` adds complexity and gains nothing, and a blocking loop stalls
  the event loop anyway
- the dependencies are synchronous-only drivers and there is no appetite to move them; a blocking
  call in an `async` handler is worse than a WSGI worker
- a trivial endpoint where [Flask](../flask/README.md) is already understood by everyone and the
  service will never grow
- an admin UI over existing tables — that is Flask-AppBuilder, not this

## Notes

The original note recorded the project link only; nothing is deployed in this folder.

That marks the actual gap. **No OpenAPI document exists anywhere under
[`api/`](../../../README.md)**, so the tooling collected in
[`docs/api-contract/`](../../../../../docs/api-contract/README.md) — Swagger UI, Redoc — has
nothing to render. FastAPI is the cheapest way to connect the two folders, because the schema is a
by-product of writing the service rather than a task added to it.

Two things worth knowing before deploying it, since neither is obvious from the project's own
documentation:

- **It does not run itself.** FastAPI is the framework; **Uvicorn** is the ASGI server. In a
  container the command is `uvicorn`, or Gunicorn managing Uvicorn workers — not `python app.py`.
  This is the same distinction [Flask](../flask/README.md) gets wrong in its checked-in image.
- **The interactive docs are on by default** at `/docs` and `/redoc`. On an internal service that
  is useful; on anything exposed through an ingress it is a decision to make deliberately rather
  than discover.

---

[← REST frameworks](../README.md)
