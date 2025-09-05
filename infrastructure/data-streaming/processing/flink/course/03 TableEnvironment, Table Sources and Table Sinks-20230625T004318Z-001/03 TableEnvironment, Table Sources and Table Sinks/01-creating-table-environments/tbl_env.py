from pyflink.table import EnvironmentSettings, TableEnvironment

############################################################
# create batch TableEnvironment
############################################################
batch_settings = EnvironmentSettings.new_instance()\
                                    .in_batch_mode()\
                                    .use_blink_planner()\
                                    .build()
batch_tbl_env = TableEnvironment.create(batch_settings)


############################################################
# create stream TableEnvironment
############################################################
stream_settings = EnvironmentSettings.new_instance()\
                                      .in_streaming_mode()\
                                      .use_blink_planner()\
                                      .build()
stream_tbl_env = TableEnvironment.create(stream_settings)


