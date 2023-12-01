# crudlapisco
desafio bolsista backend lapisco

Desafio proposto:

Implementar um CRUD de usuários utilizando uma API. 

Requisitos:
4 endpoints principais: criação,leitura,atualização e deleção.
Usar o banco de dados PostgreSQL com Docker compose.

Descrição da API:

-API denvolvida em Python com o Framework Flask.
 Endpoints:

 /usuarios [method = GET]
retorna os dados de  todos os usuários cadastrados no sistema no formato JSON

/usuario/<id> [method = GET]

retorna os dados de um únicos usuário cadastrado no sistema no formato JSON

obrigatório o ID do usuário

/usuario [method = POST]
cria um novo usuário

Obrigatório enviar uma requisição com nome:string, cpf: string, age: string.
*O CPF deve ser válido. Caso contrário o cadastro não será relizado

*A idade deve ser factível: 0< age <150

*Ausência de dados na requisição impossibilita o cadastro.

/usuario/<id> [method = PUT]
Atualiza os dados de um usuário específico, tornando-se necessãrio o envio de todos os dados obrigatórios para concuslao da operação

*A idade deve ser factível: 0< age <150


/usuario/<id> [method = DELETE]
*Usado para deletar um usuário do banco de dados

 Os dados de um usuário específico, tornando-se necessãrio o envio de todos os dados obrigatórios para concuslao da operação


Configuração do ambiente: 

As dependências externas da aplicação estão listadas no arquivo requirements.txt:

flask (Framework para incializar a API)

psycopg2-binary(Biblioteca que permite a conexao com o POSTGRESQL)

Flask-SQLAlchemy(ORM para gerenciar o acesso ao banco de dados)

validate_docbr(biblioteca para validação de cpf)

O arquivo docker-compose define configurações padrão para inicializar a aplicação com o Docker.

É importante,no entanto, que antes de instanciar os conteiners, você o edite com:
*Suas credenciais do PostgreSQL
*Defina o nome dos containers que irão rodar o banco de dados e a aplicação flask (caso deseje)
*Se desejar que a aplicação esteja disponível em um endereço ou porta diferente,altere essas configurações no docker-compose.yml
*Verifique qual a versão do PostgreSQL que você deseja trbalhar e se necessário altere no arquivo.


O aaquivo Dockerfile recebe (requirements.txt) com dependências necessárias para a aplicação, além de definir configurações básicas de aplicação flask.

Após verificar esses requisitos, excecute os seguintes comandos para inciar a aplicação:
1 - docker compose up -d flask_db

2 - docker ps -a

3 - docker compose build

4 - docke compose up --build flask_app

* Se desejar um gerenciador gráfico para o PostgreSQL, use o Dbeaver

* Se desejar analisar as respostas da API antes de intregrar com sua aplicação cliente, use Postman para testar as requisições





