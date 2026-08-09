[← Dashboards](../README.md)

# Apache DevLake

<https://github.com/apache/incubator-devlake>
<https://github.com/apache/incubator-devlake-helm-chart>
<https://devlake.apache.org/>

---

> **Not an infrastructure tool.** Everything else in this folder visualises what the
> *platform* is doing. DevLake measures how the *team delivers software*. It is here because
> it produces dashboards; the subject is different.

## The problem it solves

Engineering delivery data is scattered across GitHub, Jira, CI and deployment tooling, and
nobody can answer basic questions: how long does a change take to reach production, how often
do we deploy, how often does a deploy fail, how long to recover.

DevLake ingests from those systems, normalises the data, and produces the
**[DORA metrics](https://dora.dev/)**:

| Metric | Question |
|---|---|
| Lead time for changes | commit to production, how long? |
| Deployment frequency | how often do we ship? |
| Change failure rate | how often does shipping break something? |
| Time to restore | how long to recover when it does? |

## When to use it

- you want DORA metrics from real data rather than from a survey
- delivery bottlenecks need evidence — "reviews take four days" is a different conversation with a number attached
- platform work needs to be justified in delivery terms

## When not to use it

- you are looking for cluster or application dashboards — that is [Grafana](../grafana/README.md)
- there is no intention to act on the numbers. DORA metrics used as a performance target for individuals reliably produce gaming rather than improvement

## Why it belongs in a platform repository

It closes a loop the rest of this folder does not: everything else measures whether the
system is healthy. This measures whether the **platform is making delivery faster** — which
is the question a platform team is ultimately funded to answer.

---

[← Dashboards](../README.md)
