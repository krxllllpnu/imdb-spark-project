FROM spark:3.5.9-python3

WORKDIR /app
ENV PYTHONUNBUFFERED=1 \
    PYSPARK_PYTHON=python3 \
    SPARK_LOCAL_IP=127.0.0.1

COPY --chown=spark:spark main.py /app/main.py

ENTRYPOINT ["/opt/spark/bin/spark-submit", "--master", "local[2]", "/app/main.py"]
