[← Developer environment](../README.md)

# code-server

<https://github.com/coder/code-server>

<https://github.com/coder/coder>

---

## The problem it solves

code-server runs **VS Code as a server** and serves the editor over HTTP. The interface is the one
everyone knows, the terminal is a terminal, and extensions install as normal — but the process, the
filesystem and the toolchain are all on the remote machine. The browser is only a screen.

The consequences are the point:

| Consequence | Why it matters |
|---|---|
| **Source code never reaches the client** | the strongest argument in any regulated or BYOD setting |
| **The editor is inside the network** | in-cluster services resolve by DNS; no VPN, no port-forward |
| Any device with a browser works | tablets, borrowed machines, locked-down corporate laptops |
| The environment is defined once | rebuild the image rather than debug a laptop |
| Heavy work runs on real hardware | builds and test suites stop being limited by the thinnest laptop on the team |

Two products from the same organisation, and the difference decides which one you deploy:

| | What it is | Scope |
|---|---|---|
| **code-server** | one VS Code server process | a single user, one container |
| **Coder** | a platform that provisions and manages workspaces | teams — templates, users, lifecycle, auto-stop |

The manifests in this folder deploy **Coder**, not code-server — see the notes.

## When to use it

| Situation | Why |
|---|---|
| **Code must not be stored on endpoints** | it never is; the browser holds nothing |
| **Contractors or BYOD machines** | access is granted and revoked centrally |
| Development against in-cluster services | the workspace is already inside the network |
| Uniform environments across a team | one image, many identical workspaces |
| Working from a device that cannot run the toolchain | the toolchain is not on the device |

## When not to use it

| Situation | Use instead |
|---|---|
| **A local machine that works fine** | a [devcontainer](../devcontainer/README.md) — same reproducibility, no service to run |
| Latency-sensitive editing on a poor connection | local; keystroke latency is not something hardware fixes |
| Any work that has to happen offline | local |
| **Proprietary Microsoft extensions are required** | licensing restricts several to Microsoft-branded builds — see [VSCodium](../vscodium/README.md) |
| One developer, occasionally | [DevPod](../devpod/README.md) — remote machines without a platform to operate |

The extension marketplace point is a real constraint rather than a theoretical one. code-server
uses Open VSX by default; extensions such as the Microsoft C++, Python (proprietary parts) and
Remote Development packs are licensed for use only in Microsoft's own builds and are not there.

## Notes

### What is actually deployed here

The folder is named `code-server`, but the manifests install the **Coder** Helm chart — the
workspace platform, not the single-user editor. The two are easy to conflate because they come
from the same organisation.

| File | What it does |
|---|---|
| `helm/helmrepository.yaml` | Flux `HelmRepository` for `https://helm.coder.com/v2` |
| `helm/helmrelease.yaml` | the `coder` chart, version pinned, `Service` type `ClusterIP` |
| `namespace.yaml` | the `coder` namespace |
| `postgres/` | a PostgreSQL `Deployment`, `PersistentVolumeClaim`, `Service` and `Secret` |

Three things worth knowing about that shape:

**Coder requires PostgreSQL.** It is not an optional add-on — the control plane stores users,
templates and workspace state there. The `HelmRelease` wires it in through
`CODER_PG_CONNECTION_URL`, read from the `postgres` secret. That makes the database a hard
dependency: lose it and every workspace definition goes with it. Nothing in this folder backs it
up.

**The PostgreSQL deployment is a single pod with a PVC**, using `strategy: Recreate` — correct for
a database on a `ReadWriteOnce` volume, since a rolling update would deadlock on the volume. It is
fine for evaluation and is not a highly-available database.

**The database and user are named `pomerium`**, which is a copy-paste leftover from another
manifest. It works, because the connection string in the secret matches, but it is misleading to
anyone reading it later and is worth renaming.

`Service` type `ClusterIP` means this is not reachable from outside the cluster as configured; an
Ingress or gateway route in front of it is the missing piece, and it is the right place to put
authentication.

### The resource monitor extension

<https://marketplace.visualstudio.com/items?itemName=mutantdino.resourcemonitor>

Recorded in the original notes. It puts CPU, memory and disk usage in the editor's status bar.

In a normal VS Code install this is a nicety. In a browser-based editor it is closer to essential,
because the usual signals are gone: there is no local activity monitor for the machine you are
actually using, and a workspace container has CPU and memory *limits* that a laptop does not. When
a remote environment gets slow the question is always the same — is this the connection, or has
the container hit its limit? — and this extension is the cheapest way to answer it.

If the workspace image is built for the team, this is a reasonable extension to pre-install in it.

### Screenshot

[`vscode.PNG`](vscode.PNG) in this folder is a capture of the editor running.

---

[← Developer environment](../README.md)
