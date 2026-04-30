import jwt
from functools import wraps
from flask import request, jsonify, current_app, g
from models import User


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if "Authorization" in request.headers:
            auth_header = request.headers["Authorization"]
            if auth_header.startswith("Bearer "):
                token = auth_header.split(" ", 1)[1]

        if not token:
            return jsonify({"erro": "Token de acesso não fornecido"}), 401

        try:
            payload = jwt.decode(
                token,
                current_app.config["SECRET_KEY"],
                algorithms=["HS256"]
            )
            current_user = User.query.get(payload["user_id"])

            if not current_user:
                return jsonify({"erro": "Usuário não encontrado"}), 401

            g.current_user = current_user

        except jwt.ExpiredSignatureError:
            return jsonify({"erro": "Token expirado, faça login novamente"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"erro": "Token inválido"}), 401

        return f(*args, **kwargs)

    return decorated
