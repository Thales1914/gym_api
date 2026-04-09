from flask import Blueprint, request, jsonify
from models import db, Aluno

aluno_bp = Blueprint("aluno_bp", __name__)


def obter_json():
    dados = request.get_json(silent=True)
    if dados is None:
        dados = request.get_json(force=True, silent=True)
    return dados

@aluno_bp.route("/", methods=["POST"])
def criar_aluno():
    dados = obter_json()
    if not dados:
        return jsonify({"erro": "JSON não enviado"}), 400

    campos = ["nome", "email", "idade", "telefone"]
    for c in campos:
        if c not in dados:
            return jsonify({"erro": f"Campo '{c}' é obrigatório"}), 400

    aluno_existente = Aluno.query.filter_by(email=dados["email"]).first()
    if aluno_existente:
        return jsonify({"erro": "Já existe um aluno com esse email"}), 400

    novo = Aluno(
        nome=dados["nome"],
        email=dados["email"],
        idade=dados["idade"],
        telefone=dados["telefone"]
    )
    db.session.add(novo)
    db.session.commit()
    return jsonify(novo.to_dict()), 201

@aluno_bp.route("/", methods=["GET"])
def listar_alunos():
    alunos = Aluno.query.all()
    return jsonify([a.to_dict() for a in alunos]), 200

@aluno_bp.route("/<int:id>", methods=["GET"])
def buscar_aluno(id):
    a = Aluno.query.get(id)
    if not a:
        return jsonify({"erro": "Aluno não encontrado"}), 404
    return jsonify(a.to_dict()), 200

@aluno_bp.route("/<int:id>", methods=["PUT"])
def atualizar_aluno(id):
    a = Aluno.query.get(id)
    if not a:
        return jsonify({"erro": "Aluno não encontrado"}), 404

    dados = obter_json()
    if not dados:
        return jsonify({"erro": "JSON não enviado"}), 400

    a.nome = dados.get("nome", a.nome)
    a.email = dados.get("email", a.email)
    a.idade = dados.get("idade", a.idade)
    a.telefone = dados.get("telefone", a.telefone)

    db.session.commit()
    return jsonify(a.to_dict()), 200

@aluno_bp.route("/<int:id>", methods=["DELETE"])
def deletar_aluno(id):
    a = Aluno.query.get(id)
    if not a:
        return jsonify({"erro": "Aluno não encontrado"}), 404

    if a.pagamentos:
        return jsonify({
            "erro": "Aluno possui pagamentos vinculados e não pode ser removido"
        }), 409

    db.session.delete(a)
    db.session.commit()
    return jsonify({"mensagem": "Aluno removido com sucesso"}), 200
