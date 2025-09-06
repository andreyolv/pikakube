https://github.com/palantir/pyspark-style-guide

https://github.com/kubeflow/spark-operator

https://github.com/apache/spark
https://github.com/apache/spark-kubernetes-operator

https://github.com/japila-books/apache-spark-internals

https://github.com/datamechanics/delight
autenticação merda demais

DONE
 - Habilitar Spark Operator
 - Usar última versão do Spark no Operator
 - Integrar as SparkApplications como Tasks no Airflow.
 - Habilitar Spark History Server para centralizar logs das execuções do PySpark. Storage de logs foi um HDFS. (Delight legal mas autenticação merda)

https://blog.stackademic.com/understanding-apache-spark-deployment-modes-client-mode-cluster-mode-and-local-mode-bbfd1c7612fa

pra garantir exactly once semanticys é necessario checkpoint no spark, além de marmzenar estado de stateful tranformations como agregação temporal
     .option("asyncProgressTrackingEnabled", "true") nao suporta exactly once de acordo com https://spark.apache.org/docs/latest/streaming/performance-tips.html#limitations
https://spark.apache.org/docs/latest/streaming/performance-tips.html#continuous-processing apenas at least once
Sim, mesmo para queries stateless, você precisa usar checkpointing se quiser garantir exactly-once semantics no Spark Structured Streaming.

spark connector
"spark.submit.deployMode": "cluster"
https://lists.apache.org/thread/cq7y2xoq7kvdzbgf6z20nnfln01mkwdo
https://www.reddit.com/r/apachespark/comments/14bp1ub/spark_connect_on_kubernetes/
https://github.com/apache/spark/blob/master/core/src/main/scala/org/apache/spark/deploy/SparkSubmit.scala#L315

parametros spark
https://spark.apache.org/docs/latest/configuration.html#application-properties
https://spark.apache.org/docs/latest/submitting-applications.html#master-urls


https://github.com/apache/incubator-livy
