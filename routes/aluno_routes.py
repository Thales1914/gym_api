from flask import Blueprint, request, jsonify
from models import db, Aluno

aluno_bp = Blueprint("aluno_bp", __name__)


@aluno_bp.route("/", methods=["POST"])
def criar_aluno():
    dados = request.get_json()

    if not dados:
        return jsonify({"erro": "JSON não enviado"}), 400

    campos_obrigatorios = ["nome", "email", "idade", "telefone"]
    for campo in campos_obrigatorios:
        if campo not in dados:
            return jsonify({"erro": f"Campo '{campo}' é obrigatório"}), 400

    aluno_existente = Aluno.query.filter_by(email=dados["email"]).first()
    if aluno_existente:
        return jsonify({"erro": "Já existe um aluno com esse email"}), 400

    novo_aluno = Aluno(
        nome=dados["nome"],
        email=dados["email"],
        idade=dados["idade"],
        telefone=dados["telefone"]
    )

    db.session.add(novo_aluno)
    db.session.commit()

    return jsonify(novo_aluno.to_dict()), 201


@aluno_bp.route("/", methods=["GET"])
def listar_alunos():
    alunos = Aluno.query.all()
    return jsonify([aluno.to_dict() for aluno in alunos]), 200


@aluno_bp.route("/<int:id>", methods=["GET"])
def buscar_aluno(id):
    aluno = Aluno.query.get(id)

    if not aluno:
        return jsonify({"erro": "Aluno não encontrado"}), 404

    return jsonify(aluno.to_dict()), 200


@aluno_bp.route("/<int:id>", methods=["PUT"])
def atualizar_aluno(id):
    aluno = Aluno.query.get(id)

    if not aluno:
        return jsonify({"erro": "Aluno não encontrado"}), 404

    dados = request.get_json()
    if not dados:
        return jsonify({"erro": "JSON não enviado"}), 400

    aluno.nome = dados.get("nome", aluno.nome)
    aluno.email = dados.get("email", aluno.email)
    aluno.idade = dados.get("idade", aluno.idade)
    aluno.telefone = dados.get("telefone", aluno.telefone)

    db.session.commit()
    return jsonify(aluno.to_dict()), 200


@aluno_bp.route("/<int:id>", methods=["DELETE"])
def deletar_aluno(id):
    aluno = Aluno.query.get(id)

    if not aluno:
        return jsonify({"erro": "Aluno não encontrado"}), 404

    db.session.delete(aluno)
    db.session.commit()

    return jsonify({"mensagem": "Aluno removido com sucesso"}), 200