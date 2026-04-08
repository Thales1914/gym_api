models.py

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


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
    __tablename__ = "pagamentos"

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