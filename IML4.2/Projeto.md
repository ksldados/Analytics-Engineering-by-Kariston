# INTRODUÇÃO 

Podemos encontrar muitos problemas ao trabalhar em um projeto de aprendizado de máquina. É um desafio treinar e monitorar vários modelos. É possível que cada modelo tenha características ou parâmetros únicos. Avaliar e explorar esses modelos sem ferramentas adequadas de monitoramento de desempenho e controle de versão do modelo torna-se complicado. Compartilhar esses modelos com o restante da equipe para testes também é um desafio. Se tivermos uma ferramenta que possamos usar para acompanhar nossos modelos, isso se tornará mais conveniente. Uma plataforma que simplifica a colaboração das equipes para desenvolver pipelines eficazes de aprendizado de máquina automatizado.

Neste projeto, vamos usar aprendizado de máquina colaborativo, treinando, rastreando e compartilhando nossos modelos de aprendizado de máquina usando uma plataforma chamada “Layer”.

## Práticas recomendadas a serem lembradas ao trabalhar em um projeto de ML em equipe.

Central Data Storage:  Há necessidade de armazenamento centralizado de dados ao qual um membro da equipe possa obter acesso para salvar e usar o conjunto de dados para o projeto. Para economizar tempo durante todo o processo de limpeza para outros membros da equipe, todos os dados limpos e pré-processados ​​devem ser salvos em um único local.

Data Validation: As propriedades estatísticas dos dados podem variar ao longo do tempo à medida que mais e mais amostras são adicionadas. Isto é crítico, pois pode afetar a precisão do modelo ao longo do tempo.

Acessibilidade do modelo: O modelo treinado deve ser armazenado em algum lugar para carregar ao fazer previsões. Deve ser útil para outros membros da equipe usarem para experimentação em seus projetos.

Monitoramento do modelo: Conforme mencionado na validação de dados, as propriedades dos dados podem mudar ao longo do tempo, afetando a precisão do modelo. Portanto, o desempenho do modelo deve ser monitorado continuamente para detectar a degradação do seu desempenho.

Controle de versão do modelo: ao treinar o modelo, podemos usar diferentes recursos, modelos ou hiperparâmetros para criar diferentes modelos. Portanto, torna-se crucial rastrear estes modelos para avaliar o seu desempenho e melhorar a sua acessibilidade para quem os utiliza.


# O que é Layer?

Layer é uma plataforma para construir pipelines de aprendizado de máquina em nível de produção. Depois de enviar nossos dados e modelo para esta plataforma, podemos facilmente treinar e retreinar nossos modelos. Ele suporta perfeitamente o controle de versão do modelo e o rastreamento de desempenho. Podemos compartilhar dados e modelos, tornando-os uma plataforma simples de aprendizado de máquina colaborativo. Os membros da equipe podem revisar e avaliar os ciclos de desenvolvimento de modelos de seus pares usando o versionamento de modelos.

Devido à falta de coordenação, as equipes muitas vezes perdem tempo realizando trabalhos redundantes. O Layer funciona como um repositório central de dados e modelos, permitindo que os membros da equipe acessem os dados utilizados no processo sem precisar pré-processá-los novamente, reduzindo esforços repetitivos. O controle de versão automatizado permite voltar rapidamente para versões anteriores do modelo e recriar resultados adquiridos anteriormente.

Uma coisa maravilhosa sobre o Layer é que não precisamos modificar nossos métodos ou plataformas de programação atuais. Podemos usar os recursos do Layer com apenas algumas linhas de código.


# Implementação

Empregaremos o conjunto de dados de qualidade da água para treinar um modelo de classificação para sondar a potabilidade da água usando fatores como pH, dureza e outras propriedades químicas em nosso projeto de aprendizado de máquina. Durante o retreinamento do nosso modelo, iremos alterar alguns parâmetros. Na maioria dos casos, as versões mais antigas do modelo são perdidas durante este procedimento. Porém, neste caso, empregaremos a plataforma Layer para auxiliar no controle de versão do modelo e comparar o desempenho de diferentes versões do modelo.

Para instalar o Layer, use este código.

```
!pip instalar -U layer -q
```

Importando bibliotecas necessárias.

```
from layer.decorators import dataset, model,resources
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import pandas as pd
import numpy as np
import layer
from layer import Dataset
```

## Inicializando primeiro projeto no Layer

Vamos começar a trabalhar no projeto no Layer. Todo o seu projeto pode ser encontrado em https://app.layer.ai.

```
layer.init("new_project")
```

## Carregando os dados


Para carregar os dados no projeto Layer, usaremos o decorador @dataset e especificaremos o nome do conjunto de dados e o caminho para ele usando o decorador @resources.

```
@dataset("water_dataset")
@resources(path="./")
def create_dataset():
    data = pd.read_csv('water_potability.csv')
    return data
```


Execute o código abaixo para construir o conjunto de dados em seu projeto no Layer.

```
layer.run([create_dataset])
```

Você pode navegar dentro do seu projeto para acessar o conjunto de dados.

![image](https://github.com/ksldados/Analytics-Engineering-by-Kariston/assets/114116067/2ae8ea5d-6848-4ddd-a406-7bc91ec7e79f)

# Treinamento do Modelo

À nossa função de treinamento train(), adicionaremos o decorador @model para registrá-lo no Layer. Para fazer isso, a função deve retornar o objeto modelo. A função layer.log() registra todos os parâmetros definidos no painel Layer.

```
@model(name='classification_model',dependencies=[Dataset('water_dataset')])
def train():
    import seaborn as sns
    import matplotlib.pyplot as plt
    from sklearn.metrics import accuracy_score
    from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
    from sklearn.metrics import average_precision_score, roc_auc_score, roc_curve,precision_recall_curve
    parameters = {
        "test_size": 0.20,
        "random_state": 20,
        "n_estimators": 150
    }
    layer.log(parameters)
    # load the dataset from layer
    df = layer.get_dataset("water_dataset").to_pandas()
    df.dropna(inplace=True)
    features_x = df.drop(["Potability"], axis=1)
    target_y = df["Potability"]
    X_train, X_test, y_train, y_test = train_test_split(features_x, target_y, test_size=parameters["test_size"], random_state=parameters["random_state"])
    random_forest = RandomForestClassifier(n_estimators=parameters["n_estimators"])
    random_forest.fit(X_train, y_train)
    
    y_pred = random_forest.predict(X_test)
    layer.log({"accuracy":accuracy_score(y_test, y_pred)})
    cm = confusion_matrix(y_test, y_pred, labels=random_forest.classes_)
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=random_forest.classes_)
    disp.plot()
    layer.log({"Confusion metrics" : plt.gcf()})
    probs = random_forest.predict(X_test)
    # Calculate ROC AUC
    auc = roc_auc_score(y_test, probs)
    layer.log({"AUC":f'{auc:.4f}'})
    sample_preds = X_test
    sample_preds["predicted"] = y_pred
    layer.log({"Sample predictions":sample_preds.head(100)})
    return random_forest
```

Para registrar o parâmetro e fazer upload do modelo treinado, passe a função de treinamento para Layer.

```
layer.run([train])
```

# Comparando os resultados do treinamento

Abra o projeto Layer lá; você verá os modelos carregados e os conjuntos de dados. Todos os parâmetros e gráficos que você registrou estarão lá, junto com a versão do modelo. Cada vez que você executa a função de treinamento, uma nova versão do modelo é carregada junto com todos os parâmetros registrados. Isso facilita a comparação do desempenho de todos os modelos e o uso da versão anterior.

Podemos comparar os parâmetros e resultados registrados, como tamanho dos dados de teste, hiperparâmetros, precisão e pontuação ROC-AUC.

![image](https://github.com/ksldados/Analytics-Engineering-by-Kariston/assets/114116067/ba4de919-9a4a-4f35-a922-3c5cc92312ad)

![image](https://github.com/ksldados/Analytics-Engineering-by-Kariston/assets/114116067/839fbe9a-d1d7-4872-9482-ffa36f980b7d)

A imagem abaixo mostra as previsões de amostra.

![image](https://github.com/ksldados/Analytics-Engineering-by-Kariston/assets/114116067/51c8b218-3c5e-4ad0-a8f9-4a83f47100f3)

Os gráficos registrados de diferentes versões do modelo também podem ser visualizados e comparados.

![image](https://github.com/ksldados/Analytics-Engineering-by-Kariston/assets/114116067/b9a46e72-467e-425e-ba9c-380dd3f0039e)

## Buscando um modelo de ML ideal no Layer
Depois de treinarmos e carregarmos o modelo para a plataforma Layer, podemos carregar a versão desejada do modelo para fazer previsões. Com a ajuda deste código, podemos obter a versão do modelo necessária no Layer.

```
import layer
model = layer.get_model("san22/new_project/models/classification_model:2.1").get_train()
```

Este objeto model pode ser um modelo regular para realizar previsões com base nos dados de entrada.

# Conclusão

Neste projeto, aprendemos sobre os vários problemas que as equipes podem encontrar no setor de aprendizado de máquina ao colaborar e gerenciar versões de modelos. Posteriormente, vimos algumas das melhores práticas para trabalhar em equipe em projetos de ML. No projeto, desenhamos um projeto Layer que considera todos os desafios que as equipes enfrentam em um projeto de ML. Conclusões importantes deste artigo:

- Aprendemos como usar Layer – uma plataforma colaborativa de ML.
- Usamos controle automatizado de versão do modelo com a ajuda desta plataforma.
- Ao registrar os parâmetros do modelo e os resultados, poderíamos comparar os resultados de diferentes versões do modelo.


