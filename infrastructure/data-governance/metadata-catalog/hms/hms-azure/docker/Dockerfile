FROM cloudcheflabs/hivemetastore:v3.3.5
# https://github.com/cloudcheflabs/dataroaster/blob/master/components/hive/hive-metastore/docker/Dockerfile

ENV HADOOP_AZURE_VERSION=3.3.5
ENV HADOOP_HOME="/opt/hadoop"

RUN apt-get update && apt-get install -y wget

WORKDIR $HADOOP_HOME/share/hadoop/common/lib
RUN wget https://repo1.maven.org/maven2/org/apache/hadoop/hadoop-azure/${HADOOP_AZURE_VERSION}/hadoop-azure-${HADOOP_AZURE_VERSION}.jar

WORKDIR $HADOOP_HOME/opt/hive-metastore/lib
RUN wget https://repo1.maven.org/maven2/org/apache/hadoop/hadoop-azure/${HADOOP_AZURE_VERSION}/hadoop-azure-${HADOOP_AZURE_VERSION}.jar
