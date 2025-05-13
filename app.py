import os
import psycopg2
from flask import Flask, request, jsonify

app = Flask(__name__)

# Conectar ao banco de dados PostgreSQL usando variáveis de ambiente
try:
    conn = psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT", "5432")
    )
    cur = conn.cursor()
except Exception as e:
    print("Erro ao conectar ao banco de dados:", e)
    exit()

# Criar tabela se não existir
cur.execute("""
    CREATE TABLE IF NOT EXISTS rendimentos (
        id SERIAL PRIMARY KEY,
        descricao TEXT NOT NULL,
        valor NUMERIC NOT NULL
    )
""")
conn.commit()

#@app.route("/")
#def home():
    #return """
        #<h1>🧾 Carnê-Leão</h1>
        #<p>API ativa!</p>
        #<ul>
            #<li><a href='/listar'>/listar</a> – Ver todos os rendimentos</li>
            #<li>POST para <code>/inserir</code> com os campos <code>descricao</code> e <code>valor</code></li>
        #</ul>
    #"""

@app.route("/")
def index():
    return template("index.html")

@app.route("/inserir", methods=["POST"])
def inserir():
    try:
        descricao = request.form.get("descricao")
        valor = request.form.get("valor")
        if not descricao or not valor:
            return jsonify({"erro": "Campos 'descricao' e 'valor' são obrigatórios."}), 400

        cur.execute("INSERT INTO rendimentos (descricao, valor) VALUES (%s, %s)", (descricao, valor))
        conn.commit()
        return jsonify({"mensagem": "Rendimento inserido com sucesso!"})
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

@app.route("/listar", methods=["GET"])
def listar():
    try:
        cur.execute("SELECT * FROM rendimentos ORDER BY id DESC")
        dados = cur.fetchall()
        lista = [{"id": d[0], "descricao": d[1], "valor": float(d[2])} for d in dados]
        return jsonify(lista)
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
