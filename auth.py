from functools import wraps
from flask import request, jsonify

USUARIO = "admin"
SENHA = "1234"

def requer_auth(f):
    @wraps(f)
    def decorador(*args, **kwargs):
        auth = request.authorization
        if not auth or auth.username != USUARIO or auth.password != SENHA:
            return jsonify({"erro": "Autenticação necessária"}), 401
        return f(*args, **kwargs)
    return decorador