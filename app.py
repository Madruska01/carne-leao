
from flask import Flask, render_template, request, jsonify
from collections import defaultdict

app = Flask(__name__)

# Dados em memória (simulando um banco de dados)
rendimentos = defaultdict(float)
deducoes = defaultdict(lambda: defaultdict(float))

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/rendimentos", methods=["GET", "POST"])
def handle_rendimentos():
    if request.method == "POST":
        data = request.json
        mes = data["mes"]
        valor = float(data["valor"])
        rendimentos[mes] = valor
        return jsonify(success=True)
    return jsonify(rendimentos)

@app.route("/api/deducoes", methods=["GET", "POST"])
def handle_deducoes():
    if request.method == "POST":
        data = request.json
        mes = data["mes"]
        categoria = data["categoria"]
        valor = float(data["valor"])
        deducoes[mes][categoria] = valor
        return jsonify(success=True)
    return jsonify({mes: dict(cat) for mes, cat in deducoes.items()})

@app.route("/api/totais")
def get_totais():
    totais = {}
    for mes in rendimentos:
        bruto = rendimentos[mes]
        total_deducoes = sum(deducoes[mes].values())
        liquido = bruto - total_deducoes
        totais[mes] = {
            "bruto": bruto,
            "deducoes": total_deducoes,
            "liquido": liquido
        }
    return jsonify(totais)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
