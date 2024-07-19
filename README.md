# Projeto de Processamento de Dados com Kafka e PySpark

Este repositório contém scripts para enviar e processar dados em tempo real usando Kafka e PySpark. O projeto é dividido em três scripts principais:

1. **`exec.py`** - Script para executar múltiplos scripts em paralelo.
2. **`kafka_carregar_dados.py`** - Script para gerar e enviar dados fictícios para um tópico Kafka.
3. **`streaming_learning.py`** - Script para processar dados de um tópico Kafka e fazer previsões com um modelo River, utilizando PySpark.

No arquivo **`kafka_carregar_dados.py`**, os dados gerados divergem, sintam-se livres para alterar as funções dos dados gerados. É interessante que sejam realizados testes com diferentes modelos
para que sejam encontrados os melhores resultados de acordo com as funções selecionadas.

## Pré-requisitos

Antes de executar os scripts, você deve ter o Kafka e o Spark instalados e em execução no seu ambiente local. Além disso, é necessário ter os seguintes pacotes Python instalados:

- `kafka-python`
- `pyspark`
- `river`

Você pode instalar essas dependências usando o `pip`:

```
pip install kafka-python pyspark river
```

Certifique-se também de que o Kafka está rodando na porta `localhost:9092`.

## Por que River ao invés de TF?

Optamos pelo River em vez do TensorFlow para este projeto por várias razões:

Processamento de Fluxo de Dados: O River é uma biblioteca especializada em aprendizado de máquina para fluxo de dados (streaming). Ela é projetada para lidar com dados que chegam continuamente, o que é ideal para cenários de streaming em tempo real, como o nosso caso com o Kafka e o PySpark.

Eficiência e Simplicidade: River oferece uma abordagem mais eficiente e direta para modelos de aprendizado online, onde o modelo é atualizado continuamente com novos dados. Isso é particularmente útil para ambientes de produção em tempo real onde a simplicidade e a velocidade são cruciais.

Menor Sobrecarga: Em comparação com o TensorFlow, que é mais pesado e complexo, o River tem uma sobrecarga menor e é mais fácil de integrar e gerenciar para tarefas específicas de streaming e aprendizado incremental.

## Contribuição
Se você tiver sugestões ou encontrar problemas, fique à vontade para abrir uma issue ou enviar um pull request.

