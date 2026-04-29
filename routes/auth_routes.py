import io
import base64
from datetime import datetime, timedelta

import jwt
import pyotp
import qrcode
import bcrypt
from flask import Blueprint, request, jsonify, current_app

from models import db, User
from auth_middleware import token_required

auth_bp = Blueprint("auth_bp", __name__)


# ──────────────────────────────────────────────
#  Helper functions
# ──────────────────────────────────────────────

def obter_json():
    dados = request.get_json(silent=True)
    if dados is None:
        dados = request.get_json(force=True, silent=True)
    return dados


def hash_password(password):
    """Hash a password using bcrypt."""
    return bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt()
    ).decode("utf-8")


def check_password(password, password_hash):
    """Verify a password against its bcrypt hash."""
    return bcrypt.checkpw(
        password.encode("utf-8"),
        password_hash.encode("utf-8")
    )


def generate_token(user_id, secret_key, expires_hours=1):
    """Generate a JWT access token."""
    payload = {
        "user_id": user_id,
        "exp": datetime.utcnow() + timedelta(hours=expires_hours),
        "iat": datetime.utcnow()
    }
    return jwt.encode(payload, secret_key, algorithm="HS256")


def generate_qr_base64(provisioning_uri):
    """Generate a base64-encoded PNG QR code from a TOTP provisioning URI."""
    qr = qrcode.make(provisioning_uri)
    buffer = io.BytesIO()
    qr.save(buffer, format="PNG")
    buffer.seek(0)
    return base64.b64encode(buffer.getvalue()).decode("utf-8")


# ──────────────────────────────────────────────
#  Registration & Login
# ──────────────────────────────────────────────

@auth_bp.route("/register", methods=["POST"])
def register():
    """Register a new user with username, email, and password."""
    dados = obter_json()
    if not dados:
        return jsonify({"erro": "JSON não enviado"}), 400

    campos = ["username", "email", "password"]
    for c in campos:
        if c not in dados:
            return jsonify({"erro": f"Campo '{c}' é obrigatório"}), 400

    # Check for existing username or email
    if User.query.filter_by(username=dados["username"]).first():
        return jsonify({"erro": "Username já está em uso"}), 409

    if User.query.filter_by(email=dados["email"]).first():
        return jsonify({"erro": "Email já está em uso"}), 409

    novo_user = User(
        username=dados["username"],
        email=dados["email"],
        password_hash=hash_password(dados["password"])
    )

    db.session.add(novo_user)
    db.session.commit()

    return jsonify({
        "mensagem": "Usuário registrado com sucesso",
        "user": novo_user.to_dict()
    }), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    """
    Authenticate a user.

    - If MFA is disabled: returns a JWT token on valid credentials.
    - If MFA is enabled and no totp_code provided: returns mfa_required flag.
    - If MFA is enabled and totp_code provided: verifies TOTP, then returns JWT.
    """
    dados = obter_json()
    if not dados:
        return jsonify({"erro": "JSON não enviado"}), 400

    username = dados.get("username")
    password = dados.get("password")
    totp_code = dados.get("totp_code")

    if not username or not password:
        return jsonify({"erro": "Username e password são obrigatórios"}), 400

    user = User.query.filter_by(username=username).first()
    if not user or not check_password(password, user.password_hash):
        return jsonify({"erro": "Credenciais inválidas"}), 401

    # ── MFA flow ──
    if user.mfa_enabled:
        if not totp_code:
            return jsonify({
                "mensagem": "MFA é obrigatório para este usuário",
                "mfa_required": True
            }), 200

        totp = pyotp.TOTP(user.mfa_secret)
        if not totp.verify(totp_code):
            return jsonify({"erro": "Código MFA inválido"}), 401

    # ── Generate token ──
    token = generate_token(user.id, current_app.config["SECRET_KEY"])

    return jsonify({
        "mensagem": "Login realizado com sucesso",
        "token": token,
        "user": user.to_dict()
    }), 200


# ──────────────────────────────────────────────
#  MFA Management (all require authentication)
# ──────────────────────────────────────────────

@auth_bp.route("/mfa/enable", methods=["POST"])
@token_required
def mfa_enable():
    """
    Step 1 of MFA setup: generates a TOTP secret and returns
    the provisioning URI + QR code. MFA is NOT active yet —
    the user must confirm with /mfa/verify.
    """
    from flask import g
    user = g.current_user

    if user.mfa_enabled:
        return jsonify({"erro": "MFA já está ativado para este usuário"}), 400

    # Generate a new TOTP secret
    secret = pyotp.random_base32()
    user.mfa_secret = secret
    db.session.commit()

    # Build the provisioning URI (works with Google Authenticator, Authy, etc.)
    provisioning_uri = pyotp.TOTP(secret).provisioning_uri(
        name=user.email,
        issuer_name="GymAPI"
    )

    # Generate QR code as base64
    qr_base64 = generate_qr_base64(provisioning_uri)

    return jsonify({
        "mensagem": "Escaneie o QR code com seu aplicativo autenticador e confirme com /auth/mfa/verify",
        "provisioning_uri": provisioning_uri,
        "qr_code_base64": f"data:image/png;base64,{qr_base64}"
    }), 200


@auth_bp.route("/mfa/verify", methods=["POST"])
@token_required
def mfa_verify():
    """
    Step 2 of MFA setup: confirms the TOTP code from the
    authenticator app and activates MFA on the account.
    """
    from flask import g
    user = g.current_user

    if user.mfa_enabled:
        return jsonify({"erro": "MFA já está ativado"}), 400

    if not user.mfa_secret:
        return jsonify({"erro": "Primeiro habilite o MFA via /auth/mfa/enable"}), 400

    dados = obter_json()
    if not dados or "totp_code" not in dados:
        return jsonify({"erro": "Campo 'totp_code' é obrigatório"}), 400

    totp = pyotp.TOTP(user.mfa_secret)
    if not totp.verify(dados["totp_code"]):
        return jsonify({"erro": "Código MFA inválido, tente novamente"}), 400

    user.mfa_enabled = True
    db.session.commit()

    return jsonify({
        "mensagem": "MFA ativado com sucesso!",
        "user": user.to_dict()
    }), 200


@auth_bp.route("/mfa/disable", methods=["POST"])
@token_required
def mfa_disable():
    """
    Disables MFA on the account. Requires the current password
    and a valid TOTP code for security.
    """
    from flask import g
    user = g.current_user

    if not user.mfa_enabled:
        return jsonify({"erro": "MFA não está ativado"}), 400

    dados = obter_json()
    if not dados:
        return jsonify({"erro": "JSON não enviado"}), 400

    password = dados.get("password")
    totp_code = dados.get("totp_code")

    if not password or not totp_code:
        return jsonify({"erro": "Campos 'password' e 'totp_code' são obrigatórios"}), 400

    if not check_password(password, user.password_hash):
        return jsonify({"erro": "Senha incorreta"}), 401

    totp = pyotp.TOTP(user.mfa_secret)
    if not totp.verify(totp_code):
        return jsonify({"erro": "Código MFA inválido"}), 401

    user.mfa_enabled = False
    user.mfa_secret = None
    db.session.commit()

    return jsonify({
        "mensagem": "MFA desativado com sucesso",
        "user": user.to_dict()
    }), 200


@auth_bp.route("/me", methods=["GET"])
@token_required
def get_current_user():
    """Returns the authenticated user's profile."""
    from flask import g
    return jsonify({"user": g.current_user.to_dict()}), 200
