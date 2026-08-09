[← API](../README.md)

# WebSocket

<https://github.com/python-websockets/websockets>

---

## The problem it solves

HTTP request/response gives the server no way to speak first. If the client needs to know something
the moment it happens, the only options left are polling — asking repeatedly and getting "nothing
yet" almost every time — or long polling, which holds a request open and reissues it after every
message.

WebSocket starts as an ordinary HTTP request carrying an `Upgrade` header, and after the handshake
the connection stops being request/response and becomes a **persistent, full-duplex channel**.
Either side sends a message whenever it has one, with no per-message HTTP overhead and no round
trip to ask.

That is the whole capability, and it is genuinely different from everything else under
[`api/`](../README.md). It is also the reason WebSocket is the most operationally awkward protocol
in this folder: it converts a stateless service into a stateful one, and every piece of
infrastructure between the client and the pod has an opinion about long-lived connections.

**[websockets](https://github.com/python-websockets/websockets)**, the library recorded here, is the
Python implementation used in this folder. It is asyncio-based, implements the protocol including
the closing handshake and ping/pong keepalives correctly, and provides both a server and a client
API. It is a protocol library rather than a web framework — for a service that also serves HTTP
routes, an ASGI framework such as [FastAPI](../rest/framework/fastapi/README.md) handles both.

## When to use it

- **the server pushes and the client also sends** — chat, collaborative editing, multiplayer state,
  interactive terminals
- low latency in both directions matters, and per-message HTTP overhead is significant
- the alternative is polling frequently enough that most responses are empty
- a long-lived session with state that both sides update

## When not to use it

- **the client only receives.** Use **Server-Sent Events**: one-directional over plain HTTP, it
  passes through proxies that mangle upgrades, and the browser reconnects on its own
- updates are infrequent enough that polling every 30 seconds is fine — that is one HTTP request,
  against a stateful connection to maintain
- the message has no waiting recipient. That is a queue, not a socket — see
  [`messaging/`](../../messaging/README.md)
- the traffic must cross infrastructure that does not handle upgrades or long idle periods, and
  that cannot be changed

## Notes

The original note recorded the **websockets** library, covered above. This folder holds more than a
reference: a server, a client, a container image, a build script and Kubernetes manifests. The
server is the asyncio example from the library's documentation — accept a name, reply with a
greeting — and the client is its counterpart.

The build script is the useful part of the workflow, and it records how images reach the local
cluster:

```bash
docker build -t $TAG .
docker tag $TAG $REPONAME/$TAG
kind load docker-image $REPONAME/$TAG --name pikakube
```

`kind load docker-image` sideloads a locally built image into the kind nodes, so no registry is
involved. That is the correct pattern for a local cluster and is worth reusing.

### Two defects in the checked-in deployment

Both are recorded here rather than fixed, because both are exactly the kind of thing that only
appears once something is genuinely deployed — which is the reason this folder is worth more than
the ones holding a link.

**The server binds to `localhost`.** The application calls `serve(hello, "localhost", 8080)`. Inside
a container, `localhost` is the loopback interface of that container, so the listener is
unreachable from outside the pod no matter what the `Service` says. The `Service` and the
`Deployment` are correct; traffic still cannot arrive. The bind address has to be `0.0.0.0` for a
containerised listener — this is one of the most common causes of a pod that appears healthy and
serves nothing.

**The liveness probe targets an endpoint that does not exist.** The `Deployment` declares:

```yaml
livenessProbe:
  httpGet:
    path: /healthz
    port: 8080
  periodSeconds: 1
```

The application is a WebSocket handler and serves no HTTP routes, so `/healthz` cannot answer. The
library supports this — a `process_request` callback can respond to plain HTTP requests before the
upgrade, which is how a health endpoint is normally added to a WebSocket server — but this
application does not implement one. As written, the probe fails and Kubernetes restarts the
container in a loop.

`periodSeconds: 1` compounds it. Probing every second is far more aggressive than a liveness check
needs to be, and it leaves no room for a slow response before the failure threshold is reached.
Ten seconds is a more usual starting point, and `initialDelaySeconds` is worth setting so startup
is not counted as a failure.

### What has not been exercised

The `Service` is `ClusterIP`, so nothing here has been through an ingress — and the ingress is
where WebSocket actually becomes difficult:

- **Idle timeouts.** Proxy defaults are measured in seconds to a minute. A connection that is open
  but quiet gets closed unless the timeout is raised, and application-level ping/pong keepalives are
  the usual defence.
- **Rolling deploys disconnect everyone.** A pod terminating takes its connections with it. Clients
  must reconnect with exponential backoff **and jitter** — without jitter, every client returns at
  the same instant and overwhelms the pods that just came up.
- **Sticky routing.** Connection state lives in one pod. If that state matters, it either has to
  move to a shared store or the client has to tolerate being reconnected to a different replica.

That work sits at the boundary with [`network/`](../../../network/README.md) and is the natural
next step for this folder.

One last gap worth naming: there is **no contract**. Nothing anywhere describes which messages this
socket accepts or emits. That is the standard WebSocket failure and the reason **AsyncAPI** exists
— see [`docs/api-contract/`](../../../docs/api-contract/README.md).

---

[← API](../README.md)
