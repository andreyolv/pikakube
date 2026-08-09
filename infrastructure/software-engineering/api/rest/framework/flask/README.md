[← REST frameworks](../README.md)

# Flask

<https://github.com/pallets/flask>
<https://github.com/dpgaspar/Flask-AppBuilder>

---

## The problem it solves

A WSGI application with routing and request parsing, and nothing else decided for you. No ORM, no
authentication, no admin, no project layout. Everything beyond routing is a library you choose and
wire in yourself.

That is the entire proposition, and it cuts both ways. For a webhook receiver or a small internal
endpoint it is exactly right — the whole application is one file and there is nothing to learn
beyond the decorator. For a service that grows, every decision Django would have made arrives one
at a time, each as its own extension, and consistency across a team becomes a review problem
rather than a framework guarantee.

**[Flask-AppBuilder](https://github.com/dpgaspar/Flask-AppBuilder)** is the other end of that
spectrum: a layer on top of Flask that generates CRUD screens, menus, security and role-based
access from model definitions. It is what Superset and Airflow's classic UI are built on, which is
the strongest available evidence that it works for internal tooling. It is not a way to build an
API — it is a way to get an administrative interface over existing tables without writing one.

## When to use it

- a small service: a webhook receiver, a health endpoint, glue between two systems
- the work is **synchronous and I/O-light** — read a row, return JSON
- the team already knows it, and the service is not going to grow much
- an internal admin UI over existing models — that is Flask-AppBuilder
- learning or exercising something else, where the application is deliberately trivial

## When not to use it

- **WebSocket or Server-Sent Events** — WSGI cannot do it. That is
  [`websocket/`](../../../websocket/README.md) and an ASGI framework
- an OpenAPI contract is wanted and nobody will maintain it by hand — use
  [FastAPI](../fastapi/README.md), where the schema comes from the code
- many concurrent slow upstream calls — a blocking worker per request is the wrong model
- a large service that will be maintained for years, where "choose every extension yourself" turns
  into inconsistency across modules

## Notes

The original note recorded two references: **Flask** itself and **Flask-AppBuilder**, both covered
above. What follows is what is actually checked in beside them.

### What is in this folder

A minimal application, a `Dockerfile`, `requirements.txt` pinned to `flask==2.3.2`, and a
`.hadolint.yaml`. The application is a single `/` route returning a string — it exists to give the
container build something to run, not to demonstrate anything about API design.

### The container runs the development server

The image ends with:

```dockerfile
EXPOSE 5000
CMD ["python", "app.py"]
```

`app.py` calls `app.run()`, which is the **Werkzeug development server**. Flask prints a warning
about this on every start, and the warning is correct: it is single-process and single-threaded by
default, so a pod running this image serves **one request at a time**. It also has no worker
recycling, no request timeout and no protection against slow clients.

For exercising a build this is harmless. As a template it is the one thing to change first —
`gunicorn` in `requirements.txt` and a `CMD` that invokes it. The distinction between the framework
and the server it runs under is covered in [`framework/`](../README.md) section 3.

### The hadolint configuration contradicts itself

`.hadolint.yaml` is the most considered file here, and it contains a real misconfiguration:

```yaml
failure-threshold: warning
ignored:
- DL3026
trustedRegistries:
- techiescamp.com:5000
- "*.gcr.io"
- quay.io
```

**`DL3026` is the rule that enforces `trustedRegistries`** — it is the check that fails when a
`FROM` image comes from a registry not on the list. Ignoring it means the allowlist below is
declared and then never applied. The two settings cancel out, and the file reads as though a
registry policy is in force when nothing is enforcing it. Either remove `DL3026` from `ignored`, or
remove the `trustedRegistries` list so it does not imply a control that does not exist.

Note also that `docker.io` is commented out of the list while the `Dockerfile` uses
`FROM python:3.10-slim`, which resolves to Docker Hub — so if `DL3026` were re-enabled as written,
the build's own base image would fail the check. That is worth knowing before flipping it back on.

The `techiescamp.com:5000` entry is a tutorial's registry rather than anything in this repository,
which places the file's origin: it was copied from an example and adapted, and the contradiction
came with it.

One smaller inconsistency: `DL3015` is listed under `error`, `warning` **and** `style` in the
`override` block. A rule can only have one severity, so at most one of those three has any effect
and the other two are noise. `DL3015` is the "use `--no-install-recommends`" check, which this
`Dockerfile` never triggers, since it installs nothing through `apt`.

### `COPY /app .`

```dockerfile
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY /app .
```

The leading slash is misleading — Docker resolves source paths relative to the build context, so
`/app` means `./app` and this works. It reads as an absolute host path, which it is not. Writing it
as `COPY app/ .` says the same thing without the ambiguity.

The layer ordering above it is right, and worth keeping: dependencies are copied and installed
before the source, so a code change does not invalidate the `pip install` layer.

---

[← REST frameworks](../README.md)
