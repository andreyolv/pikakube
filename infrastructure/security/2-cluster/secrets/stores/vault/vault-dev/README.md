[← Vault](../README.md)

# Vault (dev mode)

<https://developer.hashicorp.com/vault/docs/concepts/dev-server>
<https://github.com/hashicorp/vault-helm>

The same chart as [`../vault/`](../vault/README.md) with `server.dev.enabled: true`. In-memory,
permanently unsealed, root token `root`. For tutorials.

---

## The problem it solves

A real Vault has to be initialised, unsealed with three key shares, logged into, given a secrets
engine, and given a policy before it can do anything — the procedure recorded in
[`../vault/`](../vault/README.md#initialising-vault-step-by-step). That is the correct amount of ceremony
for a system holding production credentials and far too much when the goal is to learn the CLI or
test whether an integration works.

Dev mode removes all of it:

| Property | Consequence |
|---|---|
| In-memory storage | no PVC, no storage backend, no Raft cluster |
| Auto-initialised and auto-unsealed | it is usable the moment the pod is ready |
| Root token is `root` | no init output to save, no token to hunt for |
| A KV v2 engine pre-mounted at `secret/` | `vault kv put secret/foo bar=baz` works immediately |
| TLS disabled | `VAULT_ADDR=http://127.0.0.1:8200` and nothing else |

Everything is lost when the pod restarts. That is not a bug — it is what makes it safe to break.

Both this folder and [`../vault/`](../vault/README.md) deploy a `HelmRelease` named `vault` into the
namespace `vault`. They are two versions of the same thing and only one can be applied at a time.

## When to use it

- **Learning the CLI and the concepts.** Engines, policies, auth methods, leases — all of it behaves
  normally, and a mistake costs a pod restart.
- **Testing an integration.** Does the `ClusterSecretStore` reach it, does the `SecretProviderClass`
  mount, does the operator sync? Those are answered without an unseal ceremony in the loop.
- **CI, for integration tests.** A disposable Vault per test run is exactly this.
- **Local development clusters.** On a machine that gets rebooted, a Vault that unseals itself is the
  difference between working and not.
- **Demonstrating something.** Predictable state, predictable token, no setup.

## When not to use it

- **For anything you would be upset to lose.** In-memory means every pod restart — a node drain, an
  eviction, an OOM kill, a chart upgrade — wipes every secret. There is no recovery.
- **As "temporarily good enough".** Dev mode looks like a working Vault: it has a UI, an API, and
  every command works. That resemblance is the trap. A workload pointed at it will work perfectly
  until the pod restarts, and then fail in a way that looks like an authentication problem.
- **Where the root token matters.** It is literally `root`, printed in the pod log, and it bypasses
  every policy. Anyone who can reach the service is root.
- **To evaluate performance or HA behaviour.** Single node, memory-backed. It tells you nothing about
  how a real deployment behaves under load or during a failover.
- **To test the seal, unseal or recovery paths.** Those are the operationally hard parts of running
  Vault and dev mode skips all of them. An integration validated only against dev mode has never
  seen a sealed Vault, which is the failure it will actually meet.

## Notes

Every note from `tutorial`, translated and explained, plus the state of this folder.

### The root token

> The root token in dev mode is 'root', as can be seen in the pod log
> ```bash
> k port-forward service/vault 8200
> ```

Dev mode prints the token at startup, and it is always `root` unless overridden. Combined with a
port-forward, that is the entire access procedure — which is the point, and the reason this must not
be reachable from anywhere that matters.

### Setting up a KV engine

> In the same terminal:
> ```bash
> export VAULT_ADDR="http://127.0.0.1:8200"
> export VAULT_TOKEN="root"
>
> vault secrets enable -path=airflow -version=2 kv
> ```

"In the same terminal" matters because both environment variables must be set in the shell that runs
the subsequent commands — the CLI reads them, there is no config file involved.

`-version=2` is the versioned KV engine. It is worth being deliberate about: v2 keeps a history of
each secret and inserts `/data/` into the API path, which is why a Vault **policy** for a v2 secret
reads `path "airflow/data/connections/*"` while the **CLI** command reads
`vault kv get airflow/connections/...`. That mismatch is one of the most common Vault mistakes.

Note that `-path=airflow` here differs from the `pikakube` path used by the
[external-secrets ClusterSecretStore](../../../integrations/external-secrets/README.md) and from the
`andreyolv` path in [`../vault/`](../vault/README.md)'s `init.sh`. Three examples, three mounts,
built independently.

### Airflow connections and variables

> ```bash
> vault kv put airflow/connections/smtp_default conn_uri=smtps://user:host@relay.example.com:465
> vault kv get airflow/connections/smtp_default
>
> vault kv put airflow/variables/hello value=world
> vault kv get airflow/variables/hello
> ```

This is the real purpose of the folder. Airflow has a **Vault secrets backend**: configure it with a
mount point and two prefixes, and Airflow resolves connections and variables from Vault instead of
from its metadata database.

The layout is fixed by Airflow, not chosen here:

| Airflow concept | Vault path | Expected key |
|---|---|---|
| Connection | `<mount>/connections/<conn_id>` | `conn_uri` |
| Variable | `<mount>/variables/<key>` | `value` |

So `smtp_default` becomes the connection Airflow uses to send mail, expressed as a URI, and the key
name `conn_uri` is required — Airflow looks for exactly that.

Why this matters beyond Airflow: connections are the single largest concentration of credentials in a
data platform. Database passwords, S3 keys, SMTP credentials, API tokens — all of them, by default,
sitting in the Airflow metadata database as encrypted-with-one-Fernet-key rows. Moving them to Vault
means one system holds them, with audit and rotation.

### Environment separation

> when run locally: uses the airflow/connection/dev/
> when run in prod: uses the airflow/connections/prod/

Path-based environment separation: the same connection ID resolves to a different Vault path
depending on the environment, by configuring a different mount point or prefix per Airflow instance.

This is the correct shape, and it is worth naming why: it means a DAG references `postgres_default`
and never knows which database it got. The dev instance cannot reach production credentials because
its Vault policy does not grant the `prod/` path — the separation is enforced by Vault's
authorisation, not by convention in the DAG.

Note the typo in the original: `connection/dev/` singular versus `connections/prod/` plural. Airflow
expects the plural form on both.

### Verifying against the metadata database

> ```bash
> psql -U airflow -d airflow
> \c
> \dt
> SELECT * FROM connection;
> SELECT * FROM variable;
> ```

Connect to Airflow's PostgreSQL database and list the `connection` and `variable` tables.

The point of this check is what you should **not** find. With the Vault backend working, connections
resolved from Vault do not appear in these tables — Airflow queries the secrets backend first and
falls back to the database. Rows still present are ones that have not been migrated, and they are the
remaining plaintext-ish credentials in the platform.

`\c` shows the current connection, `\dt` lists tables — the usual `psql` orientation commands.

### How it is deployed here

`helm/helmrelease.yaml`, chart `vault` 0.30.0, differing from [`../vault/`](../vault/README.md) in
exactly the ways you would expect:

| Setting | Value |
|---|---|
| `server.dev.enabled` | `true` — the whole point |
| `server.ingress` | UI at `vault.127.0.0.1.nip.io`, with mkcert TLS and Forecastle annotations |
| `server.postStart` | runs `/vault/userconfig/init/vault-init.sh` from a ConfigMap |
| `injector.enabled`, `csi.enabled` | `false` |
| `serverTelemetry.serviceMonitor` | commented out |
| storage settings | none — there is nothing to persist |

`configmap-example.yaml` is **entirely commented out**. Uncommented, it would create the `vault-init`
ConfigMap the `postStart` hook expects, mounting a script that waits five seconds, enables a KV v2
engine at `pikakube`, and writes two example variables.

That is a genuinely good pattern for dev mode — the instance comes up pre-populated, so a
`ClusterSecretStore` pointing at `pikakube` has something to read immediately. As it stands the
`postStart` references a file that no ConfigMap provides, so either the hook fails or the ConfigMap
is expected from elsewhere. Worth resolving: either uncomment it or drop the `postStart`.

---

[← Vault](../README.md)
