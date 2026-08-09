[← Developer environment](../README.md)

# Devcontainer

<https://github.com/devcontainers/spec>

<https://github.com/devcontainers/cli>

<https://containers.dev/>

---

## The problem it solves

A devcontainer is a **development environment declared in a file and committed to the repository**.
`devcontainer.json` says which image or Compose file to use, which extensions the editor should
install, which ports to forward, and which commands to run once the container exists. Opening the
project builds it and drops you inside.

What that replaces:

| Before | After |
|---|---|
| A setup section in the README that went stale | a file the tooling actually executes |
| "Which version of Python are you on?" | the image tag |
| A language upgrade touching every machine | one commit |
| CI and laptop drifting apart | the same base image in both |
| An editor configured differently by each person | extensions listed in the definition |

The property that matters most: **`devcontainer.json` is an open specification**, not a VS Code
feature. VS Code, GitHub Codespaces, [DevPod](../devpod/README.md) and the `devcontainer` CLI all
consume the same file. Writing the definition is portable work; adopting a tool without one is
lock-in.

## When to use it

| Situation | Why |
|---|---|
| **Any project more than one person will touch** | the setup stops being tribal knowledge |
| A toolchain that is awkward to install | it installs once, in an image |
| Several projects needing different versions of the same tool | isolated per project, no version manager juggling |
| Onboarding that currently takes days | it becomes "open the folder" |
| **Before adopting any remote environment tool** | it is the input format all of them read |
| Services alongside the code — a database, a broker | Docker Compose, in the same definition |

## When not to use it

| Situation | Use instead |
|---|---|
| A single-file script | a virtual environment; the container is overhead |
| Work needing tight host integration — GPUs, USB, hardware keys | local, or accept the plumbing |
| Docker Desktop is unavailable or unlicensed | check first; the whole model assumes a container runtime |
| An editor without support | the [`devcontainer` CLI](https://github.com/devcontainers/cli) builds and runs it without an editor |
| **VSCodium as the editor** | the Dev Containers extension is Microsoft-licensed — see [VSCodium](../vscodium/README.md) |

Performance is worth knowing about in advance: on macOS and Windows, bind-mounted source
directories are noticeably slower than native, because the filesystem crosses a VM boundary. For a
large repository with a heavy test suite this is felt on every run. Named volumes for dependency
directories are the usual mitigation.

## Notes

### The example in this folder

A working definition, backed by Docker Compose, building the
[Flask sample](flask/README.md) in this folder.

[`devcontainer.json`](devcontainer.json):

| Key | Value | What it does |
|---|---|---|
| `dockerComposeFile` | `docker-compose.yaml` | build from Compose rather than a single image |
| `service` | `flask-app` | which service in the Compose file the editor attaches to |
| `workspaceFolder` | `/app` | the path opened inside the container — matches the image's `WORKDIR` |
| `forwardPorts` | `[5000]` | container port 5000 appears on localhost |
| `customizations.vscode.extensions` | `dbaeumer.vscode-eslint` | installed automatically into the container's editor |
| `postCreateCommand` | `bin/sh sleep 100000` | runs once after the container is created |

The commented-out lines in the file record the two alternatives that were tried first: a
prebuilt `image` (`mcr.microsoft.com/devcontainers/typescript-node`) and a direct `build` pointing
at `flask/Dockerfile`. Those are the three ways to specify a devcontainer — image, Dockerfile,
Compose file — and the file preserves all three, which makes it a useful thing to read.

**Why Compose is the interesting choice.** With `image` or `build` you get one container. With
`dockerComposeFile` you can add a database, a broker or a cache as further services and they come
up with the environment — which is the point at which a devcontainer replaces a page of setup
instructions rather than one line of it. The Compose file here defines only `flask-app`, so that
capability is available but not yet used.

`workspaceFolder` matching the `WORKDIR` in [`flask/Dockerfile`](flask/Dockerfile) (`/app`) is not
decoration — a mismatch means the editor opens a directory the application is not running from.

### Rough edges in the example, and what they teach

This is an experiment rather than a finished template, and the sharp edges are instructive:

| Detail | Issue |
|---|---|
| `"name": "TESTE ANDREY"` | placeholder name; the container name is what appears in the editor's UI |
| `postCreateCommand: "bin/sh sleep 100000"` | missing the leading `/` on `/bin/sh`, and `sh` takes `-c` before a command — as written this does not do what it reads as |
| `dbaeumer.vscode-eslint` | an ESLint extension in a Python container; carried over from the commented-out `typescript-node` image |
| No `ports` in the Compose file | correct, in fact — `forwardPorts` is the devcontainer mechanism and is the right layer for it |

The `postCreateCommand` one is worth understanding rather than just fixing. A devcontainer built
from Compose needs its service to **stay running**, or the container exits and the editor has
nothing to attach to. The usual idiom is `sleep infinity` as the service's `command` in the
Compose file, which keeps the container alive while the editor runs processes inside it. Putting a
sleep in `postCreateCommand` is aiming at that problem from the wrong place: `postCreateCommand`
is meant for one-off setup — installing dependencies, running migrations — and the editor waits
for it to finish before the environment is ready.

`postCreateCommand` runs **once**, when the container is created. The related hooks, since the
distinction causes confusion: `onCreateCommand` runs earliest and is where prebuild work belongs,
and `postStartCommand` runs on every start rather than only the first.

---

[← Developer environment](../README.md)
