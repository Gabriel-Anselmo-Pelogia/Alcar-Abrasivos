from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    nome = None

    if request.method == "POST":
        nome = request.form.get("nome")

    return render_template("index.html", nome=nome)

@app.route("/dashboard")
def dashboard():
    dados = [10, 20, 30, 40]
    labels = ["Jan", "Fev", "Mar", "Abr"]

    return render_template(
        "dashboard.html",
        dados=dados,
        labels=labels
    )

if __name__ == "__main__":
    app.run(debug=True)
