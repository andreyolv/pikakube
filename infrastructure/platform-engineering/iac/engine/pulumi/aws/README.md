[← Pulumi](../README.md)

# pulumi-aws

<https://github.com/pulumi/pulumi-aws>

---

## The problem it solves

`pulumi-aws` is the AWS provider for [Pulumi](../README.md): the SDK that exposes AWS resources as
classes in Python, TypeScript, Go or C#. Constructing an object declares a resource; the engine
diffs the resulting graph against state and applies it.

Much of its coverage is bridged from the Terraform AWS provider, so resource names and argument
shapes are recognisable to anyone who has written HCL — `aws.s3.Bucket` rather than
`resource "aws_s3_bucket"`. That is useful in both directions: a Terraform example can usually be
translated mechanically, which is also how a lot of Pulumi AWS work actually gets done, given the
documentation complaint recorded in [`pulumi/`](../README.md).

This is Pulumi's core use case. Cloud infrastructure below the cluster is the layer where the
engine's advantages — typing, testing, reusable components — have somewhere to apply.

## When to use it

- the platform is on AWS and [Pulumi](../README.md) has already been chosen as the engine
- infrastructure code should be unit-testable and type-checked, and the team writes Python or
  TypeScript already
- the shape of the estate is genuinely computed — resources derived from data, varying by
  environment in ways `for_each` handles badly
- component abstractions will be shared as versioned packages across several projects

## When not to use it

- the platform is not on AWS
- the engine decision is still open; read [`engine/`](../../README.md) section 2 first, because this
  provider does not change the argument
- the estate is already HCL — running two engines against one cloud account means two state models
  and two ways for the same resource to have two owners
- nobody will write the tests that justify the choice, in which case the reviewability cost is paid
  for nothing

## Notes

The original note was the project link and one command:

- <https://github.com/pulumi/pulumi-aws>

```sh
pip install pulumi_aws
```

Note the underscore. The PyPI distribution is `pulumi-aws` and the import name is `pulumi_aws`;
`pip` accepts either spelling, and the recorded form matches what you `import`. Small, and the kind
of thing that costs ten minutes when the documentation is thin.

The example program, in full:

```python
import pulumi
import pulumi_aws as aws

bucket = aws.s3.Bucket("bucket")
```

Four lines, and they are a fair demonstration of both sides of the argument in
[`engine/`](../../README.md) section 2. It is shorter and more familiar than the HCL equivalent to
anyone who writes Python. It is also a program: `bucket` is a Python object whose attributes are
`Output` values, not strings, and the moment anything is done with them — a name interpolated into a
policy, an ARN passed to another resource — the asynchrony described in [`pulumi/`](../README.md)
section 2 becomes visible.

The resource is unconfigured: no name, no versioning, no encryption, no public-access block. That is
appropriate for a smoke test and it is not a starting point for anything real.

Nothing is provisioned. This folder is a "does it run" exercise, and the conclusion drawn from the
wider evaluation is recorded in [`pulumi/`](../README.md) — the tool works, the documentation was
the problem, and the platform's engine layer remains empty.

---

[← Pulumi](../README.md)
