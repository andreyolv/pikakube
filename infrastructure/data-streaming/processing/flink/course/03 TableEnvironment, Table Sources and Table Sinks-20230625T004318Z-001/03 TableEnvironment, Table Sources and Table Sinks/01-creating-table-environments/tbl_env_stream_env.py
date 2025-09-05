from pyflink.datastream import StreamExecutionEnvironment
from pyflink.table import StreamTableEnvironment

############################################################
# create stream TableEnvironment from DataStream Environment
############################################################
ds_env = StreamExecutionEnvironment.get_execution_environment()
tbl_evn = StreamTableEnvironment.create(ds_env)

