FROM apache/airflow:2.10.5-python3.12

# =========================================================
# USUARIO ROOT
# =========================================================

USER root

# =========================================================
# INSTALAR JAVA + UTILIDADES
# =========================================================

RUN apt-get update && \
    apt-get install -y \
    openjdk-17-jdk \
    wget \
    curl && \
    apt-get clean

# =========================================================
# INSTALAR SPARK 3.5.1 + HADOOP 3
# =========================================================

RUN wget https://archive.apache.org/dist/spark/spark-3.5.1/spark-3.5.1-bin-hadoop3.tgz && \
    tar -xvzf spark-3.5.1-bin-hadoop3.tgz && \
    mv spark-3.5.1-bin-hadoop3 /opt/spark && \
    rm spark-3.5.1-bin-hadoop3.tgz

# =========================================================
# INSTALAR HADOOP AWS PARA S3A
# =========================================================

RUN wget https://repo1.maven.org/maven2/org/apache/hadoop/hadoop-aws/3.3.4/hadoop-aws-3.3.4.jar \
    -P /opt/spark/jars/

# =========================================================
# INSTALAR AWS SDK PARA S3A
# =========================================================

RUN wget https://repo1.maven.org/maven2/com/amazonaws/aws-java-sdk-bundle/1.12.262/aws-java-sdk-bundle-1.12.262.jar \
    -P /opt/spark/jars/
# =========================================================
# VARIABLES DE ENTORNO
# =========================================================

ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64

ENV SPARK_HOME=/opt/spark

ENV PATH=$PATH:/opt/spark/bin

# =========================================================
# INSTALAR DEPENDENCIAS PYTHON
# =========================================================

COPY requirements.txt /tmp/requirements.txt

USER airflow

RUN pip install --no-cache-dir \
    -r /tmp/requirements.txt

# =========================================================
# USUARIO FINAL
# =========================================================

USER airflow
