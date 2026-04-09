from flask import Blueprint, request, jsonify
from models import db, Treino

treino_bp = Blueprint("treino_bp", __name__)

@treino_bp.route("/", methods=["POST"])
def criar_treino():
    try:
        dados = request.get_json()
    except Exception:
        return jsonify({"erro": "JSON inválido"}), 400
    
    if not dados:
        return jsonify({"erro": "JSON não enviado"}), 400

    campos = ["nome", "descricao", "duracao", "nivel", "instrutor"]
    for c in campos:
        if c not in dados:
            return jsonify({"erro": f"Campo '{c}' é obrigatório"}), 400

    try:
        novo = Treino(
            nome=dados["nome"],
            descricao=dados["descricao"],
            duracao=dados["duracao"],
            nivel=dados["nivel"],
            instrutor=dados["instrutor"]
        )
        db.session.add(novo)
        db.session.commit()
        return jsonify(novo.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"erro": "Erro ao criar treino", "detalhes": str(e)}), 500

@treino_bp.route("/", methods=["GET"])
def listar_treinos():
    try:
        treinos = Treino.query.all()
        return jsonify([t.to_dict() for t in treinos]), 200
    except Exception as e:
        return jsonify({"erro": "Erro ao listar treinos", "detalhes": str(e)}), 500

@treino_bp.route("/<int:id>", methods=["GET"])
def buscar_treino(id):
    t = Treino.query.get(id)
    if not t:
        return jsonify({"erro": "Treino não encontrado"}), 404
    return jsonify(t.to_dict()), 200

@treino_bp.route("/<int:id>", methods=["PUT"])
def atualizar_treino(id):
    t = Treino.query.get(id)
    if not t:
        return jsonify({"erro": "Treino não encontrado"}), 404

    try:
        dados = request.get_json()
    except Exception:
        return jsonify({"erro": "JSON inválido"}), 400
    
    if not dados:
        return jsonify({"erro": "JSON não enviado"}), 400

    t.nome = dados.get("nome", t.nome)
    t.descricao = dados.get("descricao", t.descricao)
    t.duracao = dados.get("duracao", t.duracao)
    t.nivel = dados.get("nivel", t.nivel)
    t.instrutor = dados.get("instrutor", t.instrutor)

    try:
        db.session.commit()
        return jsonify(t.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"erro": "Erro ao atualizar treino", "detalhes": str(e)}), 500

@treino_bp.route("/<int:id>", methods=["DELETE"])
def deletar_treino(id):
    t = Treino.query.get(id)
    if not t:
        return jsonify({"erro": "Treino não encontrado"}), 404
    
    try:
        db.session.delete(t)
        db.session.commit()
        return jsonify({"mensagem": "Treino removido com sucesso"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"erro": "Erro ao deletar treino", "detalhes": str(e)}), 500
