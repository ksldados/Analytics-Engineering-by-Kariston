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

Pronto. Agora já temos nossa API e Banco de Dados configurados. Vamos começar a escrever nossa DAG contendo os jobs de ETL dos dados da API.

Desta forma, precisaremos dos seguintes imports:

![image](https://github.com/ksldados/Projetos-de-Machine-Learning-Engineering-by-Kariston/assets/114116067/e1a181f9-7418-4c00-9be2-f57091a1bd3c)


Precisaremos de um DAG object para alinhar nossas tasks. Aqui passamos uma string que define o dag_id, que serve como um identificador exclusivo para a DAG. Também passamos um dicionário de argumentos padrão e definimos um 'schedule_interval' de 1 dia para o DAG.

![image](https://github.com/ksldados/Projetos-de-Machine-Learning-Engineering-by-Kariston/assets/114116067/ad7224d4-ab41-4de7-a331-ca55607ac28a)

![image](https://github.com/ksldados/Projetos-de-Machine-Learning-Engineering-by-Kariston/assets/114116067/43f62577-a3f6-49eb-9d5f-a7b5163cc1f7)

Criaremos agora um operador para criar uma tabela no nosso Banco de Dados do SQLite. Cada operador deve ter um unico task_id. SqliteOperator tem também um sqlite_conn_id e parâmetros sql. Nós vamos usar o 'db_sqlite' criado anteriormente como o 'sqlite_conn_id'.

No código SQL se a tabela 'users' não existe ainda; Ela criará a 'users' com os campos firstname, lastname, country, gender, age e email.

![image](https://github.com/ksldados/Projetos-de-Machine-Learning-Engineering-by-Kariston/assets/114116067/92996bf2-f556-4b75-8c4c-5d5c03e80f65)






