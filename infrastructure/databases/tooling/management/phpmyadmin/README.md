[← Management interfaces](../README.md)

# phpMyAdmin

<https://github.com/phpmyadmin/phpmyadmin>

---

## What it is

The MySQL web interface. It has existed since 1998, it is on effectively every shared host on the
internet, and it works.

There is nothing novel about it and that is the point: browse databases, run queries, edit rows,
import and export. Anyone who has touched MySQL has used it, so there is no adoption cost at all.

| Capability | Detail |
|---|---|
| Schema browsing | databases, tables, columns, indexes |
| SQL editor | with query history |
| Data editing | grid editing and row insertion |
| **Import and export** | SQL, CSV, and a long list of formats |
| Users and privileges | MySQL user management |
| Server status | variables, processes, replication |

## When to use it

- **MySQL or MariaDB**, and someone needs a web interface
- familiarity is the deciding factor — nobody needs to learn it
- import and export through a UI is genuinely part of the workflow

## When not to use it

- **a mixed estate** — [CloudBeaver](../cloudbeaver/README.md) covers MySQL alongside everything
  else, with one access model
- MySQL is a **source system** the platform reads from rather than serves, which is the position
  here — see [`sql/mysql/`](../../../sql/mysql/README.md)
- **the access question has not been answered** — see
  [`../README.md`](../README.md#deciding-whether-to-deploy-one-at-all)

## The security note, which is specific to this tool

phpMyAdmin deserves more caution than the others in this folder, and not because it is badly
built.

It is one of the most widely deployed web applications in existence, which makes it one of the
most **scanned for**. Automated bots probe for `/phpmyadmin` continuously across the internet, and
its long history includes a corresponding history of disclosed vulnerabilities.

| Concern | What to do |
|---|---|
| **Never public** | internal ingress only, with authentication in front of it |
| **Not on a predictable path** | `/phpmyadmin` is the first thing scanned |
| **Keep it current** | this is not optional for a tool with this exposure profile |
| Credentials | a scoped MySQL user, read-only by default — never `root` |
| Which server | a replica for anything exploratory |
| `NetworkPolicy` | it should reach MySQL and nothing else |

None of that is unique advice; it is simply more load-bearing here than for a tool nobody is
looking for.

## Notes

Mapped as the MySQL entry in this folder, deployed via Helm as a `HelmRelease`.

For this platform its practical relevance is limited by the same fact that shapes
[`sql/mysql/`](../../../sql/mysql/README.md): **MySQL appears here as a source**, not as something
the platform serves. Inspecting a source database is usually done from the extraction side rather
than through a UI the platform hosts.

If a management UI is deployed at all, [CloudBeaver](../cloudbeaver/README.md) is the
recommendation — it covers MySQL along with PostgreSQL and MongoDB, with a single user model, which
is what makes it safe rather than merely convenient.

---

[← Management interfaces](../README.md)
