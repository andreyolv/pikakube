pra garantir exactly once semanticys é necessario checkpoint no spark, além de marmzenar estado de stateful tranformations como agregação temporal
     
.option("asyncProgressTrackingEnabled", "true") nao suporta exactly once de acordo com https://spark.apache.org/docs/latest/streaming/performance-tips.html#limitations

https://spark.apache.org/docs/latest/streaming/performance-tips.html#continuous-processing apenas at least once

Sim, mesmo para queries stateless, você precisa usar checkpointing se quiser garantir exactly-once semantics no Spark Structured Streaming.
