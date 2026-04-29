from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    mfa_enabled = db.Column(db.Boolean, default=False)
    mfa_secret = db.Column(db.String(32), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "mfa_enabled": self.mfa_enabled,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }


class Aluno(db.Model):
    __tablename__ = "alunos"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    idade = db.Column(db.Integer, nullable=False)
    telefone = db.Column(db.String(20), nullable=False)

    pagamentos = db.relationship("Pagamento", backref="aluno", lazy=True)

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "email": self.email,
            "idade": self.idade,
            "telefone": self.telefone
        }


class Treino(db.Model):
    __tablename__ = "treinos"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.String(255), nullable=False)
    duracao = db.Column(db.String(50), nullable=False)
    nivel = db.Column(db.String(50), nullable=False)
    instrutor = db.Column(db.String(100), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "descricao": self.descricao,
            "duracao": self.duracao,
            "nivel": self.nivel,
            "instrutor": self.instrutor
        }


class Pagamento(db.Model):
    __tablename__ = "pagamento"

    id = db.Column(db.Integer, primary_key=True)
    aluno_id = db.Column(db.Integer, db.ForeignKey("alunos.id"), nullable=False)
    valor = db.Column(db.Float, nullable=False)
    data_pagamento = db.Column(db.String(20), nullable=False)
    status = db.Column(db.String(30), nullable=False)
    metodo = db.Column(db.String(50), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "aluno_id": self.aluno_id,
            "valor": self.valor,
            "data_pagamento": self.data_pagamento,
            "status": self.status,
            "metodo": self.metodo
        }
