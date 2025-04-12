import os
from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy

# --- Configuração ---
app = Flask(__name__, template_folder='.') # Indica que o template (index.html) está na raiz
app.config['SECRET_KEY'] = os.urandom(24) # Chave secreta para segurança

# Configuração do Banco de Dados PostgreSQL
# Substitua 'sua_senha_segura', 'fernanda_user', 'fernanda_leads' pelos seus dados
# Formato: postgresql://usuario:senha@host:porta/nome_do_banco
DATABASE_URI = "postgresql://fernanda_user:sua_senha_segura@localhost:5432/fernanda_leads"
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # Desativa avisos desnecessários

db = SQLAlchemy(app)

# --- Modelo do Banco de Dados ---
class Lead(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    telefone = db.Column(db.String(20), nullable=False)
    mensagem = db.Column(db.Text, nullable=True) # Mensagem pode ser opcional
    # Adiciona um timestamp automaticamente quando um lead é criado
    timestamp = db.Column(db.DateTime, server_default=db.func.now())

    def __repr__(self):
        return f'<Lead {self.nome} - {self.email}>'

# --- Rotas (Endpoints da API) ---

# Rota para servir a página HTML principal
@app.route('/')
def index():
    # Renderiza o seu arquivo index.html
    return render_template('index.html')

# Rota para receber os dados do formulário via POST
@app.route('/api/lead', methods=['POST'])
def cadastrar_lead():
    data = request.get_json() # Pega os dados enviados como JSON

    if not data:
        return jsonify({"erro": "Nenhum dado recebido"}), 400

    nome = data.get('nome')
    email = data.get('email')
    telefone = data.get('telefone')
    mensagem = data.get('mensagem', '') # Pega a mensagem, ou string vazia se não existir

    # Validação básica (pode ser mais robusta)
    if not nome or not email or not telefone:
        return jsonify({"erro": "Nome, email e telefone são obrigatórios"}), 400

    try:
        novo_lead = Lead(
            nome=nome,
            email=email,
            telefone=telefone,
            mensagem=mensagem
        )
        db.session.add(novo_lead) # Adiciona o novo lead à sessão
        db.session.commit()     # Salva as mudanças no banco de dados

        return jsonify({"sucesso": "Lead cadastrado com sucesso!", "lead_id": novo_lead.id}), 201 # 201 Created

    except Exception as e:
        db.session.rollback() # Desfaz a transação em caso de erro
        print(f"Erro ao salvar no banco: {e}") # Log do erro no console do servidor
        return jsonify({"erro": "Ocorreu um erro interno ao salvar os dados."}), 500

# --- Execução ---
if __name__ == '__main__':
    with app.app_context():
        # Cria as tabelas no banco de dados se elas não existirem
        # Execute isso uma vez manualmente ou deixe aqui para garantir
        db.create_all()
    # Inicia o servidor Flask
    # debug=True recarrega automaticamente quando você salva o arquivo
    app.run(debug=True, port=5001) # Usando a porta 5001 para não conflitar com outras aplicações
    # Se você quiser rodar em produção, use um servidor WSGI como Gunicorn ou uWSGI