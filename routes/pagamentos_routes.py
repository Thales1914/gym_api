
from flask import Blueprint, request, jsonify
from models import db, Pagamento, Aluno

pagamento_bp = Blueprint("pagamento_bp", __name__)


@pagamento_bp.route("/", methods=["POST"])
def criar_pagamento():
    dados = request.get_json()

    if not dados:
        return jsonify({"erro": "JSON não enviado"}), 400

    campos_obrigatorios = ["aluno_id", "valor", "data_pagamento", "status", "metodo"]
    for campo in campos_obrigatorios:
        if campo not in dados:
            return jsonify({"erro": f"Campo '{campo}' é obrigatório"}), 400

    aluno = Aluno.query.get(dados["aluno_id"])
    if not aluno:
        return jsonify({"erro": "Aluno não encontrado para vincular pagamento"}), 404

    novo_pagamento = Pagamento(
        aluno_id=dados["aluno_id"],
        valor=dados["valor"],
        data_pagamento=dados["data_pagamento"],
        status=dados["status"],
        metodo=dados["metodo"]
    )

    db.session.add(novo_pagamento)
    db.session.commit()

    return jsonify(novo_pagamento.to_dict()), 201


@pagamento_bp.route("/", methods=["GET"])
def listar_pagamentos():
    pagamentos = Pagamento.query.all()
    return jsonify([pagamento.to_dict() for pagamento in pagamentos]), 200


@pagamento_bp.route("/<int:id>", methods=["GET"])
def buscar_pagamento(id):
    pagamento = Pagamento.query.get(id)

    if not pagamento:
        return jsonify({"erro": "Pagamento não encontrado"}), 404

    return jsonify(pagamento.to_dict()), 200


@pagamento_bp.route("/<int:id>", methods=["PUT"])
def atualizar_pagamento(id):
    pagamento = Pagamento.query.get(id)

    if not pagamento:
        return jsonify({"erro": "Pagamento não encontrado"}), 404

    dados = request.get_json()
    if not dados:
        return jsonify({"erro": "JSON não enviado"}), 400

    if "aluno_id" in dados:
        aluno = Aluno.query.get(dados["aluno_id"])
        if not aluno:
            return jsonify({"erro": "Aluno não encontrado para vincular pagamento"}), 404
        pagamento.aluno_id = dados["aluno_id"]

    pagamento.valor = dados.get("valor", pagamento.valor)
    pagamento.data_pagamento = dados.get("data_pagamento", pagamento.data_pagamento)
    pagamento.status = dados.get("status", pagamento.status)
    pagamento.metodo = dados.get("metodo", pagamento.metodo)

    db.session.commit()
    return jsonify(pagamento.to_dict()), 200


@pagamento_bp.route("/<int:id>", methods=["DELETE"])
def deletar_pagamento(id):
    pagamento = Pagamento.query.get(id)

    if not pagamento:
        return jsonify({"erro": "Pagamento não encontrado"}), 404

    db.session.delete(pagamento)
    db.session.commit()

    return jsonify({"mensagem": "Pagamento removido com sucesso"}), 200