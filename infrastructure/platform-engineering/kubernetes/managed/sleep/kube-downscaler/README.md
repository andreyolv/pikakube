[← Sleep](../README.md)

# kube-downscaler

<https://codeberg.org/hjacobs/kube-downscaler>

---

## The problem it solves

Scales Deployments, StatefulSets, CronJobs and other workloads down to zero outside a defined uptime
window, and back up again inside it. Schedules are expressed as annotations on the objects
themselves, or as defaults passed to the controller — for example "Mon-Fri 08:00-19:00 Europe/Lisbon"
— with per-object overrides where needed.

The model is deliberately simple: no CRDs, no new objects, just annotations and a controller that
reads them.

## When to use it

- Development, staging and QA namespaces with predictable working hours
- You want the schedule to live on the workload rather than in a separate object
- Force-up and force-down annotations for temporary overrides
- Minimal footprint — one controller, no custom resources

## When not to use it

- Production, or anything used outside the assumed window
- On a fixed-size cluster, where scaling pods to zero saves nothing
- Workloads that cannot tolerate being stopped and restarted
- Where you would rather the schedule were a declared object in Git — [kube-green](../kube-green/README.md) is that

## Notes

**Hosted on Codeberg, not GitHub** — <https://codeberg.org/hjacobs/kube-downscaler>. Worth noting
explicitly: it is the only tool in this part of the repository whose source is not on GitHub, which
makes it easy to conclude the project has disappeared when a search turns up only forks and mirrors.
Henning Jacobs, its author, moved a number of projects to Codeberg.

That also means the usual GitHub-shaped signals — stars, issue activity, the Insights tab — are not
where you would look for them. Check Codeberg before assuming the project is dead, and be aware that
several GitHub forks exist with varying degrees of maintenance.

**Deployed with a chart**, namespace manifest, and a committed `example/deployment.yaml` showing the
annotation model in practice — which is the part worth reading, because the annotation names and the
schedule syntax are the entire interface.

**How the schedule is expressed**, and the two things that catch people out:

- **Timezone belongs in the schedule string.** A window written without one is interpreted in UTC,
  and an "08:00-19:00" window is then wrong for most of the world and shifts relative to local office
  hours twice a year with daylight saving. Write the timezone explicitly.
- **Exclusions are as important as inclusions.** System namespaces, the GitOps controller's
  namespace, and anything with a CronJob scheduled inside the window all need excluding. The failure
  is silent: things simply do not run.

**The override matters more than the schedule.** A force-up annotation on a single Deployment is what
lets someone working late keep their environment, and having that documented is what stops the whole
policy being disabled the first time it inconveniences somebody.

The saving still depends entirely on nodes going away afterwards — see the
[parent](../README.md).

---

[← Sleep](../README.md)
