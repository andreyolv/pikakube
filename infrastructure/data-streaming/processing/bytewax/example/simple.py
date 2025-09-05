from bytewax.dataflow import Dataflow
from bytewax.testing import TestingInput
from bytewax.connectors.stdio import StdOutput

flow = Dataflow()
flow.input("inp", TestingInput(range(10)))
flow.map(lambda item: item + 1)
flow.output("out", StdOutput())