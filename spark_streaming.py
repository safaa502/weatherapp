from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, DoubleType
from pyspark.sql.functions import col, from_json

KAFKA_BROKER = "kafka:9092"
TOPIC_NAME = "weather-data"

# Configuration Spark
spark = SparkSession.builder \
    .appName("Spark Kafka Stream") \
    .master("spark://spark-master:7077") \
    .getOrCreate()

# Connexion avec Kafka en streaming
kafka_stream = spark.readStream.format("kafka") \
    .option("kafka.bootstrap.servers", KAFKA_BROKER) \
    .option("subscribe", TOPIC_NAME) \
    .load()

# Schéma attendu pour les données
weather_schema = StructType([
    StructField("city", StringType()),
    StructField("temperature", DoubleType()),
    StructField("humidity", DoubleType()),
    StructField("timestamp", StringType())
])

# Décodage des messages JSON
transformed_stream = kafka_stream.selectExpr("CAST(value AS STRING) as json_string") \
    .withColumn("json_data", from_json(col("json_string"), weather_schema))

# Agrégation sur les moyennes de température par ville
agg_stream = transformed_stream.groupBy("json_data.city").agg(
    {"json_data.temperature": "avg"}
).withColumnRenamed("avg(json_data.temperature)", "avg_temperature")

# Écriture vers la console pour suivi en temps réel
query = agg_stream.writeStream \
    .outputMode("complete") \
    .format("console") \
    .start()

query.awaitTermination()
