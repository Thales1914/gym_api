import os
from flask import Flask
from flask_cors import CORS
from models import db
from routes.aluno_routes import aluno_bp
from routes.treino_routes import treino_bp
from routes.pagamentos_routes import pagamento_bp
from routes.auth_routes import auth_bp

app = Flask(__name__)
CORS(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///gymapi.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-secret-key-mude-em-producao-12345")

db.init_app(app)

with app.app_context():
    db.create_all()

app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(aluno_bp, url_prefix="/alunos")
app.register_blueprint(treino_bp, url_prefix="/treinos")
app.register_blueprint(pagamento_bp, url_prefix="/pagamentos")


@app.route("/")
def home():
    return {
        "mensagem": "GymAPI funcionando com sucesso!"
    }


if __name__ == "__main__":
    app.run(debug=True)