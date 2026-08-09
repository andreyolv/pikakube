[← RabbitMQ](../README.md)

# RabbitMQ — Helm chart

<https://github.com/rabbitmq/rabbitmq-server>
<https://github.com/qweeze/rstream>
<https://github.com/pika/pika>

Working examples in this folder: [`rabbit.ipynb`](rabbit.ipynb) ·
[`streams/producer.py`](streams/producer.py) · [`streams/consumer.py`](streams/consumer.py)

---

## The problem it solves

A [RabbitMQ](../README.md) cluster from a Helm chart, with no operator in the path.

Flux installs the Bitnami `rabbitmq` chart as a `HelmRelease`, the values live in Git, and that is
the whole deployment. It is the same shape as every other broker in this repository, which is its
main argument: nothing new to learn, one file to review.

What this shape gives you, and what it does not:

| | Chart | [Cluster operator](../rabbitmq-cluster-operator/README.md) |
|---|---|---|
| The cluster | a StatefulSet from chart values | a `RabbitmqCluster` resource |
| Several clusters | several `HelmRelease` objects | several CRs, one operator |
| **Queues, exchanges, users** | declared by the application or by hand | **Kubernetes resources** |
| Rolling upgrades | the chart's strategy | the operator's, which understands quorum membership |
| To learn | nothing | two CRD sets |

The chart gives you **a cluster**. It does not give you the topology inside it — that is the
operator's argument, and it is a real one.

## When to use it

- **one cluster**, with a configuration that does not change often
- GitOps where a `HelmRelease` plus values is the whole story
- experimenting with broker features — plugins are one line in values, as the stream plugins here show
- you would rather not run an operator to get one broker

## When not to use it

- queues, exchanges, users and policies should be **in Git** —
  [`rabbitmq-cluster-operator/`](../rabbitmq-cluster-operator/README.md), whose messaging topology
  operator is the reason to bother
- several clusters, or clusters created and destroyed regularly
- production credentials: the values here carry a username and password in plain text, which is
  fine for a lab and not for anything else

## Notes

### Deployment as configured here

The `HelmRelease` in this folder does three things worth knowing:

| Setting | Effect |
|---|---|
| `extraPlugins: "rabbitmq_stream rabbitmq_stream_management"` | enables **RabbitMQ Streams** and its management view |
| `service.extraPorts` → `5552` | exposes the stream protocol port, which is separate from AMQP's 5672 |
| `auth.username` / `auth.password` = `pikakube` | plain-text credentials — lab values, matching the example scripts |

Reaching the management UI is a port-forward, recorded in the values:

```
k port-forward svc/rabbitmq 15672
```

### Reading the effective configuration

Recorded command:

```
kubectl exec -it rabbitmq-0 -c rabbitmq -- cat /etc/rabbitmq/rabbitmq.conf
```

This is the fastest way to answer "did that value actually take effect". Chart values pass through
templating, a ConfigMap and the container before reaching the broker, so what is in `values.yaml`
and what the broker is running are not the same artifact — a plugin listed under `extraPlugins`, a
listener, a memory watermark. Reading the rendered `rabbitmq.conf` from inside the pod skips every
layer of indirection and shows the file the broker parsed.

Two details in the command: `-c rabbitmq` selects the container explicitly, because the pod has
sidecars (the metrics exporter, among others), and `rabbitmq-0` is the first StatefulSet ordinal —
worth checking another ordinal when a cluster looks inconsistent, since each node has its own file.

### Streams, with `rstream`

Recorded links:

- <https://github.com/qweeze/rstream> — the Python client for **RabbitMQ Streams**. It speaks the
  dedicated binary stream protocol on port 5552, not AMQP, which is why the chart has to expose
  that port separately. `pika` cannot do this.
- <https://github.com/qweeze/rstream/tree/master/docs/examples> — the upstream examples, and the
  source the local scripts follow.

The two scripts in [`streams/`](streams/producer.py) are working code against the cluster this
folder deploys:

| File | What it demonstrates |
|---|---|
| [`streams/producer.py`](streams/producer.py) | creates the stream `my-test-stream` with `exists_ok=True`, publishes **1,000,000** AMQP-format messages and times the run |
| [`streams/consumer.py`](streams/consumer.py) | subscribes with a callback, prints each message **with its offset**, and closes cleanly on `SIGINT` |
| [`streams/pyproject.toml`](streams/pyproject.toml) | the Poetry project — Python `^3.12`, `rstream ^0.20.6` |

Both connect to `localhost:5552` with the `pikakube` credentials, so they run against a
`port-forward` of the stream port.

The consumer printing an **offset** is the point of the exercise. A queue consumer has no offset —
it acknowledges and the message is gone. A stream consumer holds a position in a log that is still
there, so it can be replayed from a sequence number or a timestamp. That is the boundary blur
described in [`broker/`](../../README.md#7-rabbitmq-streams--the-blurred-boundary), demonstrated in
about thirty lines.

The million-message producer is also deliberate: streams are the high-throughput path in RabbitMQ,
and the timing print is there to make the difference against a classic queue measurable rather
than asserted.

### Classic queues, with `pika`

[`rabbit.ipynb`](rabbit.ipynb) is the AMQP 0-9-1 side, using
[pika](https://github.com/pika/pika): a `BlockingConnection` on port **5672**, a durable
`testqueue`, a publish through the **default exchange** (`exchange=''`, routing key = queue name),
a `passive=True` declare to read the message count without changing anything, and a
`basic_consume` loop.

Two things in it are worth carrying:

- `auto_ack=True` in the consumer is a lab convenience and a production anti-pattern — the message
  is gone the moment it is delivered, whether or not the work succeeded.
- the commented-out host, `rabbitmq.rabbitmq.svc.cluster.local`, is the in-cluster DNS name; the
  active `127.0.0.1` assumes a port-forward. Both are recorded, which is the useful part.

Side by side, the notebook and the stream scripts are the clearest illustration of the two models
living in one broker: `pika` on 5672 consumes and destroys, `rstream` on 5552 reads and rewinds.

---

[← RabbitMQ](../README.md)
