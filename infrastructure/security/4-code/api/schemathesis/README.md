[← API security testing](../README.md)

# Schemathesis

<https://github.com/schemathesis/schemathesis>

---

## The problem it solves

Nobody writes enough API tests. The happy path gets a test; the negative cases, boundary values
and malformed inputs do not, because writing them is tedious and there are hundreds per endpoint.

Schemathesis removes the writing. It reads an **OpenAPI or GraphQL specification** and generates
test cases from it, then checks the responses against the same specification:

```bash
# generate and run tests against a live service, from its spec
schemathesis run http://localhost:8000/openapi.json --checks all
```

The mechanism is **property-based testing** (it is built on Hypothesis, the Python property-based
testing library). Rather than enumerating examples, it derives inputs from the declared types and
constraints and explores the space — including the values humans do not think to try: the
boundary of an integer range, an empty array where one item is expected, a string of 10,000
characters, a null in an optional field, malformed unicode, a wrong type entirely.

Then it asserts properties that are true regardless of what the API is *for*:

| Check | Why it is always a bug |
|---|---|
| **No 500 responses** | an unhandled exception. It leaks stack traces and is often a denial-of-service vector |
| **Response conforms to the declared schema** | if the API does not match its own contract, every client is written against a lie |
| Status code is one the spec documents | an undocumented status is an unhandled case |
| Content type matches | the same |
| Headers conform | the same |

The last property is the subtle and valuable one. **The API's own specification is the oracle.**
You do not need to know what a correct answer looks like; the contract already says.

When a failure is found, Hypothesis **shrinks** it — reducing the generated input to the minimal
case that still fails — so what lands in the report is "this endpoint returns 500 when `limit=0`"
rather than a wall of random data.

It runs as a CLI, as a pytest integration (so it lives inside the existing test suite), and as a
GitHub Action.

## When to use it

- **Any service with an OpenAPI specification.** This is the entire precondition, and where it is
  met the tool is close to free value
- **In CI, against an ephemeral instance**, on every build. It is a test, not a security scan, and
  it belongs with the tests
- **Spec-first development.** It verifies that the implementation actually honours the contract
  it publishes — which is the thing that silently stops being true
- **Alongside ZAP's API scan.** The two attack the same specification differently: Schemathesis
  checks conformance and robustness, ZAP sends attack payloads —
  [`../../dast/zaproxy/README.md`](../../dast/zaproxy/README.md)
- **Through pytest**, where custom checks and existing fixtures (authentication, database setup)
  are available

## When not to use it

- **There is no specification.** There is nothing to generate from. Writing the spec is the
  prerequisite — [`docs/api-contract/`](../../../../docs/api-contract/README.md)
- **The specification has drifted from the implementation.** Every finding will be a spec bug
  rather than a code bug, and the noise will bury the real results. Fix the drift first
- **Against production, or any shared environment with real data.** It generates requests from the
  spec, which includes `DELETE` and `POST` with generated identifiers. Use a disposable instance
- **For authorisation testing.** Schemathesis tests one identity against a contract. BOLA, BFLA
  and mass assignment need multiple identities and are invisible to it — see
  [`../README.md`](../README.md) section 3
- **Expecting security findings.** Its output is *bugs*: crashes and contract violations. Many
  have security consequences, but it is not a vulnerability scanner and should not be sold as one

## Notes

Original note recorded for this tool:

- <https://github.com/schemathesis/schemathesis> — the upstream project. The repository documents
  the CLI (`schemathesis run`, `--checks`, `--hypothesis-*` tuning), the pytest integration for
  writing custom checks and reusing fixtures, authentication options, stateful testing (following
  links between endpoints to build sequences rather than testing each in isolation), and the
  GitHub Action.

Two connections worth making explicit:

- **The specification is the input, so the specification is the dependency.** In this repository
  that material lives in [`docs/api-contract/`](../../../../docs/api-contract/README.md), which
  covers OpenAPI, AsyncAPI and the renderers around them. Schemathesis is the concrete answer to
  "why does the spec need to be accurate" — an inaccurate spec produces a failing test suite
  immediately, which is a much better feedback loop than documentation that is quietly wrong.
- **Stateful testing is underused.** Testing endpoints independently misses everything that
  depends on sequence — create, then read, then delete. Schemathesis can follow OpenAPI links to
  build those sequences, and that is where it starts finding logic problems rather than only
  input-handling ones.

---

[← API security testing](../README.md)
