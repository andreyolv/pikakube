[← Data quality](../README.md)

# chispa

<https://github.com/MrPowers/chispa>

---

## What it is — and what it is not

**A testing library for PySpark, not a data-quality tool.**

That distinction matters enough to lead with, because chispa sits in
[`quality/`](../README.md) and answers a different question from everything else here:

| | chispa | The rest of this folder |
|---|---|---|
| Validates | **the transformation** | **the data** |
| Runs in | `pytest` | the pipeline |
| Against | fixtures you wrote | production data |
| Proves | the code does what you meant | today's data is sane |

Both are needed. Neither substitutes for the other, and conflating them is the anti-pattern named
in [`../README.md`](../README.md#7-anti-patterns): *testing code and calling it data quality*.

## The problem it solves

Comparing two Spark DataFrames in a test is otherwise miserable. `df1 == df2` does not do what you
want, `collect()` comparisons produce unreadable failures, and row ordering is not guaranteed.

```python
from chispa import assert_df_equality

def test_normalise_status():
    result = normalise_status(input_df)
    assert_df_equality(result, expected_df, ignore_row_order=True)
```

| Helper | What it does |
|---|---|
| `assert_df_equality` | full comparison — schema and data |
| `assert_column_equality` | one column, which is often the actual assertion |
| `assert_approx_df_equality` | floating-point tolerance |
| `ignore_row_order`, `ignore_column_order` | because neither is guaranteed |
| `ignore_nullable` | schema comparison without nullability noise |

**The failure output is the reason to use it.** A mismatch prints a side-by-side diff with the
differing rows highlighted, instead of two truncated lists that have to be compared by eye.

## When to use it

- **unit-testing PySpark transformations**
- refactoring a transformation and needing to prove the output is unchanged
- any test that compares DataFrames, where the alternative is hand-written comparison code

## When not to use it

- validating **production data** — [Deequ](../deequ/README.md) for Spark,
  [Soda](../soda/README.md) for the warehouse
- validating a DataFrame's shape at runtime — [Pandera](../pandera/README.md)
- non-Spark work

## Testing Spark, practically

The library is small; the surrounding practice is what makes tests useful:

| Practice | Why |
|---|---|
| **A session-scoped Spark fixture** | starting a session per test dominates the runtime |
| **Small fixtures** | three rows exercising the logic, not a sample of production |
| `ignore_nullable=True` | inferred schemas differ in nullability constantly, and it is rarely the point |
| `ignore_row_order=True` | Spark does not guarantee order; asserting on it is testing the wrong thing |
| Test the transformation, not the read | separate the I/O from the logic and test the logic |

The last row is the one that decides whether Spark code is testable at all. A function that reads
a path, transforms and writes cannot be unit-tested; the same logic as a
`DataFrame → DataFrame` function can be, in milliseconds.

## Notes

Mapped as the PySpark testing library, and it is worth keeping in this folder rather than moving
it elsewhere — precisely because the confusion it clears up is common. "We have data quality
covered, we have tests" is a sentence that means one of these two things and rarely both.

For this platform it applies to the
[Spark](../../../data-engineering/processing/spark/README.md) workloads and to the PySpark used
around [Soda](../soda/README.md) and the lakehouse — see
[`quality/soda/pyspark/`](../soda/README.md).

The four-way split from [`pandera/`](../pandera/README.md) is the summary worth carrying:

| Tool | Validates | Where |
|---|---|---|
| **chispa** | a transformation's output | a unit test |
| [Pandera](../pandera/README.md) | a DataFrame's shape | a function boundary |
| [Deequ](../deequ/README.md) | data at Spark scale | inside the job |
| [Soda](../soda/README.md) | a warehouse table | the pipeline |

---

[← Data quality](../README.md)
