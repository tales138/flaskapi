from flask import Flask, Response, request
from flask_sqlalchemy import SQLAlchemy
import json
from validate_docbr import CPF
from os import environ



app = Flask(__name__)#inicialização do flask

#configurações de banco de dados
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DB_URL')

#inicialização do ORM SQLAlchemy
db = SQLAlchemy(app)

#classe usuário para modelar a estrutura dos dados
class Usuario(db.Model):
    __tablename__ = 'usuarios'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    cpf = db.Column(db.String(14))  # formato xxx.xxx.xxx-xx
    age = db.Column(db.String(3))  # xxx

    #retorna os dados do usuário no formato JSON    
    def to_json(self):
        return {"id": self.id, "name": self.name, "cpf": self.cpf, "age": self.age}

db.create_all()#linha de código deletável caso deseje conectar com um banco de dados já existente

# Método para buscar e retornar todos os usuários 
@app.route("/usuarios", methods=["GET"])
def seleciona_usuarios():
    usuarios_objetos = Usuario.query.all()
    usuarios_json = [usuario.to_json() for usuario in usuarios_objetos]

    return gera_response(200, "usuarios", usuarios_json)

# Método buscar um único usuário por id
@app.route("/usuario/<id>", methods=["GET"])
def seleciona_usuario(id):
    usuario_objeto = Usuario.query.filter_by(id=id).first()
    usuario_json = usuario_objeto.to_json()

    return gera_response(200, "usuario", usuario_json)


# Método para cadastrar um único usuário
@app.route("/usuario", methods=["POST"])
def cria_usuario(): 
    try:
        data = request.get_json()

        if(validar_dados_requisicao(data)):
            usuario = Usuario(name=data["name"], cpf=data["cpf"],age=data["age"])
            
        if(validate_age_format(data["age"]) and validate_cpf(data["cpf"])): 
            db.session.add(usuario)
            db.session.commit()
            return gera_response(201, "usuario", usuario.to_json(), "Usuario criado com sucesso")
    except Exception as e:
        return gera_response(400, "usuario", {}, "Erro ao cadastrar usuario")
    

# Método para atualizar os dados de um usuário
@app.route("/usuario/<id>", methods=["PUT"])
def atualiza_usuario(id):
    usuario_objeto = Usuario.query.filter_by(id=id).first()
    body = request.get_json()
    try:
        if(validar_dados_requisicao(body) and validate_cpf(body['cpf']) and validate_age_format(body['age'])):
            usuario_objeto.name = body['name']
            usuario_objeto.cpf = body['cpf']
            usuario_objeto.age = body['age']

        db.session.add(usuario_objeto)
        db.session.commit()
        return gera_response(200, "usuario", usuario_objeto.to_json(), "Dados atualizados com sucesso")
    except Exception as e:
        return gera_response(400, "usuario", {}, "Erro ao atualizar dados do usuario")


# Método para deletar um usuário
@app.route("/usuario/<id>", methods=["DELETE"])
def deleta_usuario(id):
    usuario_objeto = Usuario.query.filter_by(id=id).first()
    try:
        db.session.delete(usuario_objeto)
        db.session.commit()
        return gera_response(200, "usuario", usuario_objeto.to_json(), "Deletado com sucesso")
    except Exception as e:
        print('Erro', e)
        return gera_response(400, "usuario", {}, "Erro ao deletar")

# metódo para gerar um resposta para as requisições para a API
def gera_response(status, nome_do_conteudo, conteudo, mensagem=False):
    body = {}
    body[nome_do_conteudo] = conteudo

    if(mensagem):
        body["mensagem"] = mensagem

    return Response(json.dumps(body), status=status, mimetype="application/json")


# método para validar se os dados enviados na requisição estão de acordo com o padrão exigido
def validar_dados_requisicao(data):
    if 'name' not in data or 'cpf' not in data or 'age' not in data:
        return False

    return True

#método para validar cpf. Utiliza a biblioteca validate_docbr
def validate_cpf(cpf):
        cpf_validator = CPF()
        if not cpf_validator.validate(cpf):
            raise ValueError("CPF inválido")
        return True

#método para validar se o usuário tem uma idade possível 
def validate_age_format(age):
        try:
           if(age > 0 and age < 150):
            return True
        except ValueError:
            raise ValueError("Idade fora do padrão")
app.run()