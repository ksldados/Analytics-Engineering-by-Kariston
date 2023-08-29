# PROJETO - EXTRAÇÃO, TRANSFORMAÇÃO E CARREGAMENTO DE DADOS DE UMA API PÚBLICA USANDO AIRFLOW

Neste projeto, iremos extrair alguns registros da API https://randomuser.me/ utilizando-se a linguagem Python e depois vamos criar uma tabela em um banco de dados SQLIte e efetuar a carga dos dados em uma tabela. Todo este Pipeline será orquestrado via Apache Airflow.

Partindo do presuposto que nossa máquina local já está configurada e previamente instalada todas as dependências necessárias para uso do Apache Airflow e SQLite3, devemos rodar os seguintes comandos no nosso terminal:

```python
airflow db init
```

Agora criamos o usuário administrador para o banco de dados SQLite no Airflow fazendo isso:

```python
airflow users  create --role Admin --username admin --email admin --firstname admin --lastname admin --password admin
```

E então podemos inicializar o Apache Airflow em nossa máquina:

```python
airflow webserver -p 8080
```

Por último, inicializamos o Airflow Scheduler:

```python
airflow scheduler
```

Primeiramente, vamos criar um banco de dados no SQLite3, para isso, vamos utilizar o comando em uma janela do terminal:

```python
sqlite3 userdatabase.db
```
Para verificar que criamos com êxito, basta digitarmos o comando abaixo e nosso banco deverá aparecer.

```python
.databases
```
Agora, vamos até o nosso Airflow via browser (geralmente fica no endereço http://0.0.0.0:8080/home) e vamos configurar as conexões com a API e Banco de Dados SQLite. Para isto, após abrir os Airflow, clique na parte superior da tela em Admin > Connections.
Uma tela semelhante a imagem abaixo deverá abrir. Então, clique no íncone de "+".

![image](https://github.com/ksldados/Projetos-de-Machine-Learning-Engineering-by-Kariston/assets/114116067/0048e901-ef68-4b12-8070-71f2c7b0a76e)

Preencha os campos como segue a imagem abaixo para configurarmos a conexão com a API https://randomuser.me. 

![image](https://github.com/ksldados/Projetos-de-Machine-Learning-Engineering-by-Kariston/assets/114116067/677bd399-6827-40fe-9448-8895f8de0a15)

Preenchido os campos, clique em "Save".

Agora, vamos configurar a conexão com o banco de dados SQLite que criamos anteriormente. Para isto, clique no íncone de "+" e preencha os campos conforme imagem abaixo, mudando somente o diretório onde consta seu db criado.

![image](https://github.com/ksldados/Projetos-de-Machine-Learning-Engineering-by-Kariston/assets/114116067/9494fa0d-e5cc-4906-8c66-0d9a31e08860)

Pronto. Agora já temos nossa API e Banco de Dados configurados. 

# Construção do Pipeline 

O pipeline consistirá as seguintes etapas, basicamente:

![image](https://github.com/ksldados/Projetos-de-Machine-Learning-Engineering-by-Kariston/assets/114116067/2cbb9eeb-8d6a-4c8b-9706-f0213ab4c682)

Escreveremos um job que fará todo esse trabalho de forma automatizada. Vamos começar a escrever nossa DAG contendo os jobs de ETL dos dados da API.

Desta forma, precisaremos dos seguintes imports:

![image](https://github.com/ksldados/Projetos-de-Machine-Learning-Engineering-by-Kariston/assets/114116067/e1a181f9-7418-4c00-9be2-f57091a1bd3c)


Precisaremos de um DAG object para alinhar nossas tasks. Aqui passamos uma string que define o dag_id, que serve como um identificador exclusivo para a DAG. Também passamos um dicionário de argumentos padrão e definimos um 'schedule_interval' de 1 dia para o DAG.

![image](https://github.com/ksldados/Projetos-de-Machine-Learning-Engineering-by-Kariston/assets/114116067/ad7224d4-ab41-4de7-a331-ca55607ac28a)

![image](https://github.com/ksldados/Projetos-de-Machine-Learning-Engineering-by-Kariston/assets/114116067/43f62577-a3f6-49eb-9d5f-a7b5163cc1f7)

Criaremos agora um operador para criar uma tabela no nosso Banco de Dados do SQLite. Cada operador deve ter um unico task_id. SqliteOperator tem também um sqlite_conn_id e parâmetros sql. Nós vamos usar o 'db_sqlite' criado anteriormente como o 'sqlite_conn_id'.

No código SQL se a tabela 'users' não existe ainda; Ela criará a 'users' com os campos firstname, lastname, country, gender, age e email.

![image](https://github.com/ksldados/Projetos-de-Machine-Learning-Engineering-by-Kariston/assets/114116067/92996bf2-f556-4b75-8c4c-5d5c03e80f65)

Nesta etapa verificará se a API está funcionando com o 'endpoint' customizado [https://randomuser.me/api/](https://randomuser.me/api), vamos usar api/ no parâmetro endpoint.

![image](https://github.com/ksldados/Projetos-de-Machine-Learning-Engineering-by-Kariston/assets/114116067/36f546d6-49e7-4bcb-ba47-65321c63c481)

Usando o SimpleHttpOperator nós enviamos um requisito GET HTTP  para a conexão user_api que criamos antes. Com o response_filter nós convertemos o JSON string em um campo 'response.text' que é um python object.

![image](https://github.com/ksldados/Projetos-de-Machine-Learning-Engineering-by-Kariston/assets/114116067/f65c7f36-1ded-4b25-a7c6-0ed426a022a4)

Com o uso do PythonOperator, nós vamos manter somente os campos desejados do python object que nós obtivemos via API anteriormente. E vamos salvar os dados num arquivo .csv

Definimos o objeto 'Task Instance (ti)' como um parâmetro da função python e pegamos os resultados das 'task_ids' com users = ti.xcom_pull(task_ids=['extracting_user']).

![image](https://github.com/ksldados/Projetos-de-Machine-Learning-Engineering-by-Kariston/assets/114116067/b8869fab-c79e-4a3d-9dd0-b9989078ea44)

![image](https://github.com/ksldados/Projetos-de-Machine-Learning-Engineering-by-Kariston/assets/114116067/63ec7484-ba83-4c16-9319-058b9f68362d)


Podemos agora usar o BashOperator para armazenar a tabela criada e carregada com os dados dentro do nosso Banco de Dados SQLite 'userdatabase.db' criado anteriormente.

![image](https://github.com/ksldados/Projetos-de-Machine-Learning-Engineering-by-Kariston/assets/114116067/63dc179b-360d-474d-ae83-6ecb1e0a20f3)

Por último, definimos o workflow das tasks:

![image](https://github.com/ksldados/Projetos-de-Machine-Learning-Engineering-by-Kariston/assets/114116067/d003cedb-f978-4452-9c70-3297094ac541)

Para analisar os resultados, recomenda-se usar o software 'DB Browser for SQLite'. Para isto, basta instalar a aplicação e executar em seguida e deverá ter algo semelhante a isto:

![image](https://github.com/ksldados/Projetos-de-Machine-Learning-Engineering-by-Kariston/assets/114116067/90d32c6e-60ad-439c-b9b9-d5d5e77b263c)

Clique em "Open Database" e navegue até o arquivo criado anteriormente 'userdatabase.db'. Então, deverá ter algo como:

![image](https://github.com/ksldados/Projetos-de-Machine-Learning-Engineering-by-Kariston/assets/114116067/ff928965-b76f-45b2-9e70-58c52f2dec0d)

Para consultar os dados, clique em "Execute SQL" e então digite o código:

```sql
SELECT * FROM users
```

![image](https://github.com/ksldados/Projetos-de-Machine-Learning-Engineering-by-Kariston/assets/114116067/1841f329-9aa4-4832-9076-55554772511c)

## REPOSTA USANDO SQL PARA ATINGIR AS MÉTRICAS

Para responder as métricas conforme as perguntas de negócio, deve-se escrever os códigos no DB Browser como segue abaixo:

1 - Totalde pessoas com o mesmo nome por país

```sql
SELECT country,
COUNT(*) - COUNT(DISTINCT firstname) +1 as qtde_pessoas_mesmo_nome
FROM users
GROUP BY 1;
```

![image](https://github.com/ksldados/Projetos-de-Machine-Learning-Engineering-by-Kariston/assets/114116067/cbf91ab9-f0bf-4b0e-9597-b4f1ab516185)


2 - Distribuição de pessoas por gênero por país

```sql
SELECT gender,country,
COUNT(*) as qtde_pessoas_por_genero
FROM users
GROUP BY 1,2;
```

![image](https://github.com/ksldados/Projetos-de-Machine-Learning-Engineering-by-Kariston/assets/114116067/e5225d36-e94f-4f8b-b2fc-2685c35bd8bc)



3 - Quantas pessoas da distribuição do ítem 2 possuí + de 50

```sql
SELECT gender,country,
COUNT(*) as qtde_pessoas_por_genero
FROM users
WHERE age >= 50
GROUP BY 1,2;
```

![image](https://github.com/ksldados/Projetos-de-Machine-Learning-Engineering-by-Kariston/assets/114116067/19ee70dc-82c7-4843-9758-21626a3ed638)
