from flask import Flask, Response, request
from flask_sqlalchemy import SQLAlchemy
import json
from validate_docbr import CPF
from datetime import datetime
from os import environ

# Substitua as informações abaixo pelos seus dados de conexão

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DB_URL')
db = SQLAlchemy(app)

#classe usuário
class Usuario(db.Model):
    __tablename__ = 'usuarios'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    cpf = db.Column(db.String(14))  # formato xxx.xxx.xxx-xx
    age = db.Column(db.String(10))  # formato dd/mm/yyyy
        
    def to_json(self):
        return {"id": self.id, "name": self.name, "cpf": self.cpf, "age": self.age}
#fim classe usuário

db.create_all()

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
       # print('Erro', e)
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

def gera_response(status, nome_do_conteudo, conteudo, mensagem=False):
    body = {}
    body[nome_do_conteudo] = conteudo

    if(mensagem):
        body["mensagem"] = mensagem

    return Response(json.dumps(body), status=status, mimetype="application/json")


def validar_dados_requisicao(data):
    if 'name' not in data or 'cpf' not in data or 'age' not in data:
        return False

    return True

def validate_cpf(cpf):
        cpf_validator = CPF()
        if not cpf_validator.validate(cpf):
            raise ValueError("CPF inválido")
        return True

def validate_age_format(age):
        try:
            datetime.strptime(age, '%d/%m/%Y')
            return True
        except ValueError:
            raise ValueError("Formato de data inválido. Use o formato dd/mm/yyyy")
app.run()