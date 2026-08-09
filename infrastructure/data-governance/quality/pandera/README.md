[← Data quality](../README.md)

# Pandera

<https://github.com/unionai-oss/pandera>

---

## The problem it solves

**Schema validation as code**, right next to the DataFrame — and typed, so the editor and the type
checker know about it too.

```python
import pandera as pa
from pandera.typing import DataFrame, Series

class Orders(pa.DataFrameModel):
    order_id: Series[str] = pa.Field(unique=True)
    customer_id: Series[str] = pa.Field(nullable=False)
    amount: Series[float] = pa.Field(ge=0)
    status: Series[str] = pa.Field(isin=["pending", "shipped", "cancelled"])

@pa.check_types
def transform(df: DataFrame[Orders]) -> DataFrame[Orders]:
    ...
```

The decorator validates on the way in and on the way out. The schema is a **type annotation**,
which means the function signature states what it accepts and what it produces — and that is
checked at runtime rather than being a comment.

| Capability | Detail |
|---|---|
| **Typed schemas** | `DataFrameModel` classes, checked by decorators |
| **Function boundaries** | validate inputs and outputs, where the contract actually is |
| Backends | pandas, Polars, PySpark, Dask, Modin |
| Custom checks | ordinary Python functions |
| Hypothesis testing | statistical checks between groups |
| **Synthesis** | generate test data *from* the schema |

Data synthesis is the underrated one: a schema that describes valid data can also produce it, so
tests get realistic fixtures without anyone writing them.

## When to use it

- **pandas or Polars** transformations, in Python
- validation belongs at **function boundaries** — this is where it is strongest
- the team wants types and editor support rather than a separate config file
- generating test fixtures from the schema is useful

## When not to use it

- checks should be readable by analysts — [Soda](../soda/README.md)'s YAML
- the data is in a warehouse and never becomes a DataFrame
- Spark at volume — [Deequ](../deequ/README.md)'s single-pass metrics
- profiling and data docs — [Great Expectations](../great-expectations/README.md)

## Where it fits differently from the others

The distinction worth holding, because it is not a smaller version of the other tools:

| | Pandera | Soda / Deequ / GE |
|---|---|---|
| Validates | a **DataFrame in memory** | a **dataset at rest** |
| Position | inside the code, at a function boundary | in the pipeline, against a source |
| Failure | an exception, immediately | a failed check, reported |
| Feels like | **type checking** | **testing** |

That makes it complementary rather than competing. Pandera catches a transformation producing the
wrong shape *at the moment it happens*, with a stack trace pointing at the function. Soda catches
the table being wrong after the pipeline finished.

The strongest combination in a Python pipeline is both: Pandera at the function boundaries, and a
dataset-level check before publishing.

## Anti-patterns specific to it

| Anti-pattern | Why | Instead |
|---|---|---|
| Validating in production loops | it costs a pass over the DataFrame each time | at boundaries, not inside iteration |
| A schema per intermediate step | churn, and most steps are not contracts | validate where data crosses a boundary |
| `lazy=False` for exploratory work | it stops at the first error | `lazy=True` collects them all |
| Using it as the only quality layer | it sees the DataFrame, not the published table | pair with a dataset-level check |

`lazy=True` is worth knowing about early: by default validation raises on the first failure, and
lazy mode reports every violation at once — which is the difference between one debugging cycle
and ten.

## Notes

Mapped as the Python-native schema option. For this platform it is the tool that fits **inside**
Python code rather than around it, which places it closer to
[chispa](../chispa/README.md) than to [Soda](../soda/README.md) in role — both operate on the
transformation rather than on the published data.

The four tools in this folder, separated by what they actually validate:

| Tool | Validates | Where |
|---|---|---|
| **Pandera** | a DataFrame's shape | at a function boundary |
| [chispa](../chispa/README.md) | a transformation's output | in a unit test |
| [Deequ](../deequ/README.md) | data, at Spark scale | inside the job |
| [Soda](../soda/README.md) | a table in the warehouse | in the pipeline |

Confusing those four is how a platform ends up with three tools doing one job and no coverage of
the other three.

---

[← Data quality](../README.md)
