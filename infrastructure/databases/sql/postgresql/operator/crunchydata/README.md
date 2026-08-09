[← PostgreSQL operators](../README.md)

# Crunchy Postgres Operator (PGO)

<https://github.com/CrunchyData/postgres-operator>
<https://access.crunchydata.com/documentation/postgres-operator/>

---

## What it is

One of the longest-running PostgreSQL operators, from Crunchy Data — with **commercial support**
behind it and a track record in regulated environments.

Feature-wise it covers the same ground as [CloudNativePG](../cnpg/README.md): failover, replication,
backup and PITR (via pgBackRest), monitoring, and TLS.

## When to use it

- **commercial support** is a requirement, which is the usual reason
- regulated environments where a vendor relationship matters for audit
- pgBackRest specifically is the backup standard already in use

## When not to use it

- CNCF governance and no external dependencies are preferred — [CloudNativePG](../cnpg/README.md)
- you want the simplest architecture; both are mature, and CNPG has fewer moving parts

## The honest comparison

Both are good. The decision is rarely technical:

| | CloudNativePG | Crunchy PGO |
|---|---|---|
| Governance | CNCF | vendor, with a commercial edition |
| Support | community | **commercial available** |
| Backup | Barman, native | pgBackRest |
| Momentum | currently the default choice | steady, long-established |

Choose Crunchy when someone needs to be accountable under contract. Choose CNPG when that is
not a requirement — which is most of the time, and is why it has become the default.

---

[← PostgreSQL operators](../README.md)
