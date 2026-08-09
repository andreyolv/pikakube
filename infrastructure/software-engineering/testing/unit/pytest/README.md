[← Unit and integration testing](../README.md)

# pytest

<https://github.com/pytest-dev/pytest>

---

## The problem it solves

**Running Python tests, with as little ceremony as possible between the intention and the test.**

A pytest test is a function whose name starts with `test_`, containing a plain `assert`. No base
class, no `self.assertEqual`, no registration. When the assertion fails, pytest rewrites it to show
the actual values on both sides — which is the difference between "AssertionError" and knowing what
went wrong without opening a debugger.

Three features carry most of the value:

| Feature | What it is for |
|---|---|
| **Fixtures** | setup and teardown as dependency injection — a test declares what it needs as an argument, and pytest builds it, with `function`, `class`, `module` or `session` scope |
| **Parametrisation** | `@pytest.mark.parametrize` turns one test into many cases; edge cases become rows in a list instead of copied functions |
| **Markers** | labels that make subsets selectable — `pytest -m "not integration"` is the difference between a suite run constantly and one run daily |

The plugin ecosystem is the other reason it is the default: `pytest-cov` for coverage, `pytest-xdist`
for parallel execution, `pytest-mock`, `pytest-asyncio`, and the
[testcontainers](../testcontainers/README.md) integration that supplies real dependencies as
fixtures.

## When to use it

- **any Python test suite** — it is the de facto standard, and there is no real competitor
- unit tests, and equally the integration tests in this folder
- as the runner underneath [testcontainers](../testcontainers/README.md), with the container as a
  session-scoped fixture
- migrating from `unittest`: pytest runs `unittest` test cases as they are, so adoption is
  incremental

## When not to use it

- **another language** — Go, JavaScript and the rest have their own runners; the *approach* in
  [`unit/`](../README.md) carries across, the tool does not
- **load testing** — [`load/`](../../load/README.md); [Locust](../../load/locust/README.md) is
  Python, but it is not a test runner
- exercising APIs interactively — [`api/`](../../api/README.md)
- as the whole of the testing strategy: pytest runs whatever is written, and writing only end-to-end
  tests with it produces the inverted pyramid described in [`testing/`](../../README.md)

## Notes

The recorded note is a single link — <https://github.com/pytest-dev/pytest> — and there is nothing
else to compare it against, which is itself the point. In Python, this is the default. `unittest` is
in the standard library and is used mainly where a dependency cannot be added.

Nothing is deployed for pytest, and nothing should be: it is a development dependency of the
application, managed by whatever this repository's
[Python dependency tooling](../../../language/python/README.md) settles on.

The conventions that make a suite stay usable, all of them cheap to adopt on day one:

- **Mark integration tests**, so the fast suite can be run without them. Registering markers in
  `pyproject.toml` avoids the warnings that make people add filters.
- **Put shared fixtures in `conftest.py`**, at the narrowest scope that works.
- **Use `tmp_path`, not a hardcoded temporary directory.** It is per-test and cleaned up.
- **Session-scope expensive fixtures.** A [testcontainers](../testcontainers/README.md) Postgres
  started once per session and rolled back per test is fast; one started per test is not.
- **Do not chase a coverage percentage.** `pytest-cov` produces a useful report and a poor gate —
  see [`unit/`](../README.md) section 5.

---

[← Unit and integration testing](../README.md)
