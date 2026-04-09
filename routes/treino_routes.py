from flask import Blueprint, request, jsonify
from models import db, Treino

treino_bp = Blueprint("treino_bp", __name__)


def obter_json():
    dados = request.get_json(silent=True)
    if dados is None:
        dados = request.get_json(force=True, silent=True)
    return dados

@treino_bp.route("/", methods=["POST"])
def criar_treino():
    try:
        dados = obter_json()
    except Exception:
        return jsonify({"erro": "JSON inválido"}), 400
    
    if not dados:
        return jsonify({"erro": "JSON não enviado"}), 400

    campos_obrigatorios = ["nome", "descricao", "duracao", "nivel", "instrutor"]
    for campo in campos_obrigatorios:
        if campo not in dados:
            return jsonify({"erro": f"Campo '{campo}' é obrigatório"}), 400

    try:
        novo_treino = Treino(
            nome=dados["nome"],
            descricao=dados["descricao"],
            duracao=dados["duracao"],
            nivel=dados["nivel"],
            instrutor=dados["instrutor"]
        )
        db.session.add(novo_treino)
        db.session.commit()
        return jsonify(novo_treino.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"erro": "Erro ao criar treino", "detalhes": str(e)}), 500

@treino_bp.route("/", methods=["GET"])
def listar_treinos():
    try:
        treinos = Treino.query.all()
        return jsonify([treino.to_dict() for treino in treinos]), 200
    except Exception as e:
        return jsonify({"erro": "Erro ao listar treinos", "detalhes": str(e)}), 500

@treino_bp.route("/<int:id>", methods=["GET"])
def buscar_treino(id):
    treino = Treino.query.get(id)
    if not treino:
        return jsonify({"erro": "Treino não encontrado"}), 404
    return jsonify(treino.to_dict()), 200

@treino_bp.route("/<int:id>", methods=["PUT"])
def atualizar_treino(id):
    treino = Treino.query.get(id)
    if not treino:
        return jsonify({"erro": "Treino não encontrado"}), 404

    try:
        dados = obter_json()
    except Exception:
        return jsonify({"erro": "JSON inválido"}), 400
    
    if not dados:
        return jsonify({"erro": "JSON não enviado"}), 400

    treino.nome = dados.get("nome", treino.nome)
    treino.descricao = dados.get("descricao", treino.descricao)
    treino.duracao = dados.get("duracao", treino.duracao)
    treino.nivel = dados.get("nivel", treino.nivel)
    treino.instrutor = dados.get("instrutor", treino.instrutor)

    try:
        db.session.commit()
        return jsonify(treino.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"erro": "Erro ao atualizar treino", "detalhes": str(e)}), 500

@treino_bp.route("/<int:id>", methods=["DELETE"])
def deletar_treino(id):
    treino = Treino.query.get(id)
    if not treino:
        return jsonify({"erro": "Treino não encontrado"}), 404
    
    try:
        db.session.delete(treino)
        db.session.commit()
        return jsonify({"mensagem": "Treino removido com sucesso"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"erro": "Erro ao deletar treino", "detalhes": str(e)}), 500
