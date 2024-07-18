from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, isnan
from pyspark.sql.types import StructType, StructField, FloatType, IntegerType
import json
import os
from river import linear_model, preprocessing, metrics
from kafka import KafkaProducer
from river import neural_net as nn
from river import optim

# Configuração de pacotes adicionais para PySpark
os.environ['PYSPARK_SUBMIT_ARGS'] = '--packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.0.1 pyspark-shell'

class StreamProcessor:

    def __init__(self):
        # Inicialização da sessão Spark
        self.spark = SparkSession.builder \
            .appName("KafkaSparkStreamingWithRiver") \
            .config("spark.sql.streaming.forceDeleteTempCheckpointLocation", "true") \
            .config("spark.sql.warehouse.dir", "file:///C:/temp/spark-warehouse") \
            .config("spark.hadoop.fs.file.impl", "org.apache.hadoop.fs.LocalFileSystem") \
            .config("spark.hadoop.fs.AbstractFileSystem.file.impl", "org.apache.hadoop.fs.local.LocalFs") \
            .getOrCreate()

        # Definição do esquema dos dados
        self.schema = StructType([
            StructField("feature1", FloatType(), True),
            StructField("feature2", FloatType(), True),
            StructField("label", FloatType(), True)
        ])

        # Inicialização do produtor Kafka
        self.producer = KafkaProducer(
            bootstrap_servers='localhost:9092',
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )

        # Definir modelo River e métrica
        self.scaler = preprocessing.StandardScaler()
        self.model = self.scaler | linear_model.SoftmaxRegression()
        self.metric = metrics.RMSE()

    def process_batch(self, batch_df, batch_id):
        print("Processando lote:", batch_id)
        
        # Verificar se há dados no batch_df
        if batch_df.isEmpty():
            print("Sem dados para processar.")
            return

        # Filtrar dados nulos ou NaN
        batch_df = batch_df.filter(~isnan(col("feature1")) & ~isnan(col("feature2")) & col("feature1").isNotNull() & col("feature2").isNotNull())

        # Iterar sobre cada linha do lote
        for row in batch_df.collect():
            x = {'feature1': row['feature1'], 'feature2': row['feature2']}
            y = row['label']

            # Verificação adicional para garantir que y não seja None e seja um tipo válido
            if y is None or not isinstance(y, (int, float)):
                print(f"Label invalida: {row}")
                continue

            y = int(y)  

            # Treinamento do modelo
            try:
                self.model.learn_one(x, y)
            except Exception as e:
                print(f"Erro ao treinar o modelo: {e}")
                continue

            # Previsão
            try:
                y_pred = self.model.predict_one(x)
            except Exception as e:
                print(f"Erro ao prever com o modelo: {e}")
                continue

            self.metric.update(y, y_pred)
            print(f"RMSE: {self.metric.get()}")

            # Enviar previsão para o tópico Kafka
            prediction_data = {
                'features': x,
                'label': y,
                'prediction': y_pred,
                'metric': self.metric.get()
            }
            self.producer.send('predicoes', value=prediction_data)

            print(f'Previsao concluida: {prediction_data}')

    def start_streaming(self):
        # Criar diretório de checkpoint se não existir
        checkpoint_location = "C:/temp/spark-checkpoint"
        os.makedirs(checkpoint_location, exist_ok=True)
        
        # Ler dados do Kafka
        kafka_df = self.spark.readStream \
            .format("kafka") \
            .option("kafka.bootstrap.servers", "localhost:9092") \
            .option("subscribe", "dados_teste") \
            .option("failOnDataLoss", "false") \
            .load()

        # Decodificar dados do Kafka
        value_df = kafka_df.selectExpr("CAST(value AS STRING)")

        # Converter para DataFrame estruturado
        json_df = value_df.select(from_json(col("value"), self.schema).alias("data")).select("data.*")

        # Filtrar dados nulos ou NaN
        json_df = json_df.filter(~isnan(col("feature1")) & ~isnan(col("feature2")) & col("feature1").isNotNull() & col("feature2").isNotNull())

        # Aplicar a função de processamento a cada lote de dados
        query = json_df.writeStream \
            .foreachBatch(self.process_batch) \
            .option("checkpointLocation", checkpoint_location) \
            .option("failOnDataLoss", "false") \
            .start()
        
        query.awaitTermination()

# Instanciar e iniciar o processamento
if __name__ == "__main__":
    try:
        stream_processor = StreamProcessor()
        stream_processor.start_streaming()
    except Exception as e:
        print(f"Erro no processamento do stream: {e}")
