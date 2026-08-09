[← API testing](../README.md)

# Postman

<https://www.postman.com/>

---

## The problem it solves

**Everything around an API, for a team, in one product.**

Postman stopped being an HTTP client a long time ago. It is a platform: collections, shared team
workspaces, environments, mock servers, generated documentation, scheduled monitors, and Newman as
the CLI runner for pipelines.

For an organisation where several teams work on the same APIs, that breadth is a genuine answer to a
real problem. Nothing else in this folder offers real-time shared workspaces, a hosted mock server
derived from a collection, or documentation published from the same source.

It is also **the only tool in this folder that is not open source.** That is the reason its note is a
link to `postman.com` rather than to a GitHub repository — there is no repository to link.

## When to use it

- **a large team collaborating on APIs in real time**, where shared workspaces are the point
- **mock servers** generated from a collection, so a consumer can build before the provider exists
- published API documentation kept in step with the requests
- monitors — scheduled runs of a collection against a deployed environment
- an existing Postman estate: the migration cost is real and the tool is not bad

## When not to use it

- **when collections must live in git and be reviewed** — the default is a cloud workspace, and
  export-and-commit is a habit that lasts about two sprints; use [Bruno](../bruno/README.md)
- when a cloud dependency or a per-seat licence is not acceptable
- when the environment is offline or restricted
- SOAP and WSDL — [SoapUI](../soapui/README.md)
- **load testing** — it sends requests serially; use [`load/`](../../load/README.md)
- as a replacement for tests written in code — [`unit/`](../../unit/README.md)

## Notes

The recorded note for this tool is a **bare website link**: <https://www.postman.com/> — and unlike
[Bruno](../bruno/README.md), [Insomnia](../insomnia/README.md) and [SoapUI](../soapui/README.md),
which are all recorded as GitHub repositories, there is no source repository to record.

**Postman is the only non-open-source tool in this folder.** That is not a disqualification, but in
this repository it is a decision with consequences:

| Consequence | Detail |
|---|---|
| Licensing | per seat, beyond the free tier |
| Data location | collections live in Postman's cloud unless deliberately kept local |
| Reviewability | a change to a collection is not a diff anyone approves |
| Lock-in | the collection format is Postman's, and the surrounding features are not portable |

The last two are the ones that matter for pikakube specifically. Every other artefact in this
repository is a text file in git, changed by pull request. An API contract test held in a SaaS
workspace is the one thing nobody can review, and it is the one most likely to drift from the
service it describes.

**Newman** is the mitigation if Postman is already in use: export the collection into the
application's repository and let CI run it. That recovers reviewability at the cost of a manual
export step, which someone has to remember.

If the choice is still open, [Bruno](../bruno/README.md) gives the same collection-and-CLI model with
the files in git and no account. Choose Postman for the collaboration features, knowingly — not
because it is the client everyone already has installed.

---

[← API testing](../README.md)
