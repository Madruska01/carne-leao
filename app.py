import os
import psycopg2
from flask import Flask, request, jsonify

app = Flask(__name__)

# Conexão com o banco de dados PostgreSQL
conn = psycopg2.connect(
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT", 5432)
)
cur = conn.cursor()

# Criação da tabela, se não existir
cur.execute("""
    CREATE TABLE IF NOT EXISTS rendimentos (
        id SERIAL PRIMARY KEY,
        descricao TEXT,
        valor NUMERIC
    )
""")
conn.commit()

@app.route("/")
def home():
    return """
    <h1>Bem-vindo ao sistema Carnê-Leão!</h1>
    <p>Use <code>/listar</code> para ver dados ou envie um POST para <code>/inserir</code>.</p>
    """

@app.route("/inserir", methods=["POST"])
def inserir():
    descricao = request.form["descricao"]
    valor = request.form["valor"]
    cur.execute("INSERT INTO rendimentos (descricao, valor) VALUES (%s, %s)", (descricao, valor))
    conn.commit()
    return "Inserido!"

@app.route("/listar")
def listar():
    cur.execute("SELECT * FROM rendimentos")
    dados = cur.fetchall()
    return jsonify(dados)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")

