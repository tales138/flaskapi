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
*A idade deve ser factível: 0<age<150
*Ausência de dados na requisição impossibilita o cadastro.

/usuario/<id> [method = PUT]
Atualiza os dados de um usuário específico, tornando-se necessãrio o envio de todos os dados obrigatórios para concuslao da operação
*A idade deve ser factível: 0<age<150


/usuario/<id> [method:DELETE]
*Usado para deletar um usuário do banco de dandos
 Os dados de um usuário específico, tornando-se necessãrio o envio de todos os dados obrigatórios para concuslao da operação


Confifuração do ambiente: 
