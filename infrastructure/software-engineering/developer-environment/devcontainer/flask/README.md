[← Devcontainer](../README.md)

# Flask sample

<https://github.com/pallets/flask>

---

## The problem it solves

Nothing, on its own. This is the **application the devcontainer in the parent folder builds** — the
smallest thing that can be containerised, opened in an editor and served, so that the devcontainer
mechanics are demonstrated rather than described.

Three files:

| File | What it is |
|---|---|
| [`app/app.py`](app/app.py) | one Flask route returning `Hello World The Plumbers` |
| [`requirements.txt`](requirements.txt) | `flask==2.3.2`, pinned |
| [`Dockerfile`](Dockerfile) | `python:3.10-slim`, dependencies installed, port 5000 exposed |

The [parent `docker-compose.yaml`](../docker-compose.yaml) builds this directory as the
`flask-app` service, and [`devcontainer.json`](../devcontainer.json) attaches the editor to it.

## When to use it

| Situation | Why |
|---|---|
| **Verifying the devcontainer works at all** | a known-good target that fails for its own reasons, not the app's |
| Learning the Compose-based devcontainer shape | small enough to hold in your head |
| A starting point for a real service | replace `app.py`, keep the structure |

## When not to use it

| Situation | Use instead |
|---|---|
| **Anything reaching production** | this is a development server — see the notes |
| A real Flask application in this repository | `api/rest/framework/flask/`, which is the same framework treated properly |
| Learning Flask itself | the framework's own tutorial; this is here for the container, not the code |

## Notes

### The Dockerfile

The layering is right, and worth naming because it is the same discipline the
[uv Dockerfile](../../../language/python/dependency-management/uv/README.md) applies:

```
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY /app .
```

Dependencies are installed **before** the source is copied, so editing `app.py` does not invalidate
the install layer. `--no-cache-dir` keeps pip's download cache out of the image. `flask==2.3.2` is
pinned exactly, which is the minimum bar for a reproducible build — though a single pinned direct
dependency still leaves every transitive one floating, which is what a lock file exists to fix.

`COPY /app .` copies the `app/` directory's *contents* into `/app`, which is why the `CMD` is
`python app.py` rather than `python app/app.py`. The leading slash is redundant but harmless — it
is resolved against the build context, not the host root.

### Two things that will bite in a real service

**`app.run()` binds to `127.0.0.1` by default.** Inside a container that means the loopback
interface *of the container*, so nothing outside it can connect — including a forwarded port. A
containerised Flask app needs `app.run(host="0.0.0.0")`, or an equivalent flag. This is the single
most common reason a container that looks healthy answers nothing.

**`app.run()` is the development server.** It is single-threaded by default and Flask itself prints
a warning against using it in production. A real deployment runs a WSGI server — Gunicorn, or
uWSGI — as the container's entrypoint. For a devcontainer sample that is fine and intentional; the
development server is what you want when the point is reloading code you are editing.

### Why the version pins are worth a second look

`python:3.10-slim` and `flask==2.3.2` were current when this was written and both are now behind.
That is not a defect in a sample, but it is the argument for the discipline documented in
[`language/python/dependency-management/`](../../../language/python/dependency-management/README.md):
a pinned base image and a pinned dependency are a snapshot of a moment, and without a lock file and
a deliberate update path they age silently until something forces the issue.

---

[← Devcontainer](../README.md)
