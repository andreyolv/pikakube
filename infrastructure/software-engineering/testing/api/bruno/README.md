[← API testing](../README.md)

# Bruno

<https://github.com/usebruno/bruno>

---

## The problem it solves

**An API collection that lives in git and reviews like code.**

Every other client in this folder stores collections in a proprietary format, a local database, or
somebody's cloud account. Bruno stores them as **plain text files in a directory** — one `.bru` file
per request, in a folder structure you choose, committed alongside the code they test.

That single decision fixes the things that make API collections rot:

| Problem | Bruno's answer |
|---|---|
| The collection only exists on one laptop | it is a folder in the repository |
| Nobody can review a change to it | a normal diff in a pull request |
| Merge conflicts on a giant exported JSON | one small file per request |
| An account and a sync service to use a HTTP client | neither is required |
| Secrets end up in a vendor's workspace | environment files stay local; secrets come from the pipeline |

There is a GUI for writing and running requests interactively, and a CLI (`bru`) that runs the same
collection headlessly — so the collection someone explores with is literally the one CI executes.

## When to use it

- **a GitOps repository**, where everything else is already a reviewed file in git
- API tests that must run in CI from the same definition developers use locally
- teams that do not want an account, a licence or a cloud dependency for an HTTP client
- replacing Postman collections that keep drifting from the code
- offline or restricted environments, where cloud sync is not an option

## When not to use it

- **SOAP and WSDL** — it does not do this; use [SoapUI](../soapui/README.md)
- real-time collaborative workspaces, mock servers and generated API documentation — that is
  [Postman](../postman/README.md)'s territory
- **load testing** — a client sends requests serially; use [`load/`](../../load/README.md)
- as a substitute for tests written in code — black-box collections do not replace
  [`unit/`](../../unit/README.md)
- if the team's workflow genuinely depends on Postman-only features, switching costs more than it
  saves

## Notes

The recorded note is a single link — <https://github.com/usebruno/bruno> — and the choice of what
was recorded is the finding: **it is a GitHub repository.** Three of the four tools in this folder
are, and [Postman](../postman/README.md) is not. Bruno is open source, and the collection format is
open text rather than an export.

Nothing is deployed for Bruno in this repository, and nothing should be — it is a desktop
application plus a CLI. What belongs in a repository is the **collection**, in the application's
own repository next to the code, with the `bru` CLI wired into the pipeline.

Of the four clients here, Bruno is the one whose model matches the rest of pikakube: a directory of
text files, changed by pull request, applied by automation. That is the same shape as every Flux
manifest in this repository, which is a better reason to choose it than any feature comparison.

---

[← API testing](../README.md)
