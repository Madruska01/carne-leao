import os
import psycopg2
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# Função para obter conexão com o banco de dados
def get_db():
    if "db" not in g:
        g.db = psycopg2.connect(
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT", "5432")
        )
    return g.db

# Fechar conexão ao final da requisição
@app.teardown_appcontext
def close_db(e=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()

# Criar a tabela na primeira requisição
def criar_tabela():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS rendimentos (
            id SERIAL PRIMARY KEY,
            descricao TEXT NOT NULL,
            valor NUMERIC NOT NULL
        )
    """)
    conn.commit()
    cur.close()

# Rotas
@app.route("/")
def home():
    return render_template("index.html")
    #"""
        #<h1>🧾 Carnê-Leão</h1>
        #<p>API ativa!</p>
        #<ul>
            #<li><a href='/listar'>/listar</a> – Ver todos os rendimentos</li>
            #<li>POST para <code>/inserir</code> com os campos <code>descricao</code> e <code>valor</code></li>
        #</ul>
    #"""

@app.route("/inserir", methods=["POST"])
def inserir():
    try:
        descricao = request.form.get("descricao")
        valor = request.form.get("valor")
        if not descricao or not valor:
            return jsonify({"erro": "Campos 'descricao' e 'valor' são obrigatórios."}), 400

        conn = get_db()
        cur = conn.cursor()
        cur.execute("INSERT INTO rendimentos (descricao, valor) VALUES (%s, %s)", (descricao, valor))
        conn.commit()
        cur.close()
        return jsonify({"mensagem": "Rendimento inserido com sucesso!"})
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

@app.route("/listar", methods=["GET"])
def listar():
    try:
        conn = get_db()
        cur = conn.cursor()
        cur.execute("SELECT * FROM rendimentos ORDER BY id DESC")
        dados = cur.fetchall()
        cur.close()
        lista = [{"id": d[0], "descricao": d[1], "valor": float(d[2])} for d in dados]
        return jsonify(lista)
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

# Executar localmente (não usado pelo Render)
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
