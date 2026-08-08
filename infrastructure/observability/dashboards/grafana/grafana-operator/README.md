[← Dashboards](../../README.md)

# Grafana Operator

<https://github.com/grafana/grafana-operator>

---

## The problem it solves

Grafana clicked together in a UI has no history, no review and no reproducibility — and
disappears when the pod is recreated without persistence.

The operator makes Grafana declarative: `Grafana`, `GrafanaDashboard`, `GrafanaDatasource`
and `GrafanaFolder` become CRDs reconciled from Git. Dashboards go through pull requests
like any other change, and a rebuilt cluster comes back with the same ones.

## When to use it

- GitOps — dashboards and datasources should live in the repository
- multiple clusters that must present the same dashboards
- dashboards need review before they change

## When not to use it

- a single throwaway cluster where clicking is genuinely faster
- you need **app plugins**, which the operator cannot install — see below

---

## Notes

### App plugins cannot be installed through the operator

<https://github.com/grafana/grafana-operator/issues/1392>
<https://github.com/grafana/grafana-operator/issues/2460>

This is a real constraint on what can be provisioned declaratively. Panel plugins are one
thing; **app** plugins are not covered, so anything depending on one has to be handled
outside the operator.

Plugin tooling: <https://github.com/grafana/plugin-tools>

### Datasource API

```
https://127.0.0.1:3000/api/datasources
```

Useful for confirming what the operator actually reconciled, as opposed to what the CRD says.

---

[← Dashboards](../../README.md)
