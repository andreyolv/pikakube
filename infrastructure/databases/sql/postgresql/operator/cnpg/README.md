[← PostgreSQL operators](../README.md)

# CloudNativePG

<https://github.com/cloudnative-pg/cloudnative-pg>
<https://github.com/cloudnative-pg/charts>
<https://cloudnative-pg.io/documentation/>

Related: [postgres-containers](https://github.com/cloudnative-pg/postgres-containers) ·
[cnpg-i](https://github.com/cloudnative-pg/cnpg-i) ·
[plugin-barman-cloud](https://github.com/cloudnative-pg/plugin-barman-cloud) ·
[Barman](https://github.com/EnterpriseDB/barman)

---

## Why it is the default

CloudNativePG runs Postgres on Kubernetes **without Patroni, without etcd and without a
separate consensus layer**. Coordination uses the Kubernetes API itself.

That is the architectural difference from the generation before it, and it matters: fewer
components, fewer failure modes, and nothing extra to operate alongside the database.

| Capability | Detail |
|---|---|
| **Failover** | automatic, coordinated through the Kubernetes API |
| Replication | streaming replicas managed by the operator |
| **Backup and PITR** | to object storage, via Barman — a first-class feature, not a sidecar |
| Rolling upgrades | minor versions, with controlled switchover |
| Connection routing | `-rw`, `-ro` and `-r` services, so clients do not track the primary |
| TLS | certificates issued and rotated |
| Monitoring | a Prometheus endpoint built in |

The three services are worth knowing: applications connect to `-rw` for writes and `-ro` for
reads, and failover changes which pod is behind them without the application noticing.

## When to use it

- **the default** for PostgreSQL on Kubernetes
- backup to object storage with point-in-time recovery is required
- CNCF governance, and no appetite for extra coordination components

## When not to use it

- commercial support is a requirement — [Crunchy](../crunchydata/README.md)
- you want pooling, extensions and monitoring bundled and opinionated — [StackGres](../stackgres/README.md)
- an existing [Zalando](../zalando/README.md) estate that works

## What to verify before depending on it

**Restore, actually performed.** Not "backups are configured" — a real restore, into a real
cluster. And the operator has to be scaled to zero first, or it recreates an empty volume
before the restore lands. That procedure is recorded in
[Velero](../../../../../site-reliability-engineering/backup/velero/README.md).

**PITR, not just full backups.** Recovering to the moment *before* a bad migration is the
requirement that matters, and it is a different configuration from nightly backups.

## Monitoring

- [Grafana dashboards](https://github.com/cloudnative-pg/grafana-dashboards)
- [Dashboard 20417](https://grafana.com/grafana/dashboards/20417-cloudnativepg/)

The operator exposes Prometheus metrics natively, which means the
[postgres-exporter](../../../../../observability/metrics/exporters/postgres-exporter/README.md) may be
redundant — worth checking coverage before running both.

## Examples

<https://github.com/cloudnative-pg/cloudnative-pg/blob/main/docs/src/samples.md>

---

## Notes

Open issues worth reading before depending on specific behaviour:

- <https://github.com/cloudnative-pg/cloudnative-pg/issues/6111>
- <https://github.com/cloudnative-pg/cloudnative-pg/issues/7923>
- <https://github.com/cloudnative-pg/cloudnative-pg/issues/10536>
- <https://github.com/cloudnative-pg/cloudnative-pg/issues/2574>
- <https://github.com/cloudnative-pg/cloudnative-pg/issues/4210>

`cnpg-i` is the plugin interface, and `plugin-barman-cloud` is the backup implementation moving
into it — relevant when planning an upgrade path, since backup configuration is shifting from
in-tree to plugin-based.

---

[← PostgreSQL operators](../README.md)
