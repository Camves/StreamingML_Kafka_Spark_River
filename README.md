# Projeto de Processamento de Dados com Kafka e PySpark

Este repositório contém scripts para enviar e processar dados em tempo real usando Kafka e PySpark. O projeto é dividido em três scripts principais:

1. **`exec.py`** - Script para executar múltiplos scripts em paralelo.
2. **`kafka_producer.py`** - Script para gerar e enviar dados fictícios para um tópico Kafka.
3. **`spark_streaming.py`** - Script para processar dados de um tópico Kafka e fazer previsões com um modelo River, utilizando PySpark.

## Pré-requisitos

Antes de executar os scripts, você deve ter o Kafka e o Spark instalados e em execução no seu ambiente local. Além disso, é necessário ter os seguintes pacotes Python instalados:

- `kafka-python`
- `pyspark`
- `river`

Você pode instalar essas dependências usando o `pip`:

```bash
pip install kafka-python pyspark river

Aqui está a parte formatada para você copiar e colar diretamente no GitHub:

markdown
Copiar código
Certifique-se também de que o Kafka está rodando na porta `localhost:9092`.

## Scripts

### `exec.py`

Este script executa os scripts `kafka_producer.py` e `spark_streaming.py` em paralelo. Para usá-lo, execute:

```bash
python exec.py
kafka_producer.py
Este script cria e envia dados fictícios para um tópico Kafka chamado dados_teste. Os dados incluem características (feature1, feature2) e um rótulo (label). Para executá-lo, use:

bash
Copiar código
python kafka_producer.py
spark_streaming.py
Este script lê os dados do tópico Kafka dados_teste, processa esses dados usando PySpark e um modelo River, e envia previsões para um tópico Kafka chamado predicoes. Para executá-lo, use:

bash
Copiar código
python spark_streaming.py
Escolha do River em vez do TensorFlow
Optamos pelo River em vez do TensorFlow para este projeto por várias razões:

Processamento de Fluxo de Dados: O River é uma biblioteca especializada em aprendizado de máquina para fluxo de dados (streaming). Ela é projetada para lidar com dados que chegam continuamente, o que é ideal para cenários de streaming em tempo real, como o nosso caso com o Kafka e o PySpark.

Eficiência e Simplicidade: River oferece uma abordagem mais eficiente e direta para modelos de aprendizado online, onde o modelo é atualizado continuamente com novos dados. Isso é particularmente útil para ambientes de produção em tempo real onde a simplicidade e a velocidade são cruciais.

Menor Sobrecarga: Em comparação com o TensorFlow, que é mais pesado e complexo, o River tem uma sobrecarga menor e é mais fácil de integrar e gerenciar para tarefas específicas de streaming e aprendizado incremental.

Adequação ao Projeto: Para o nosso objetivo de processar dados em streaming e realizar previsões rápidas, o River fornece as funcionalidades necessárias sem a complexidade adicional do TensorFlow. O TensorFlow seria mais apropriado para modelos de aprendizado profundo e redes neurais complexas, que não são o foco principal deste projeto.

Contribuição
Se você tiver sugestões ou encontrar problemas, fique à vontade para abrir uma issue ou enviar um pull request.

Licença
Este projeto está licenciado sob a Licença MIT. Veja o arquivo LICENSE para mais detalhes.
