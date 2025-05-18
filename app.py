from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = "cuenta-regresiva-clave"

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        fecha_str = request.form.get("fecha")
        hora_str = request.form.get("hora")
        if fecha_str and hora_str:
            try:
                objetivo = datetime.strptime(f"{fecha_str} {hora_str}", "%Y-%m-%d %H:%M")
                session["objetivo"] = objetivo.strftime("%Y-%m-%d %H:%M:%S")
                return redirect(url_for("contador"))
            except ValueError:
                return render_template("index.html", error="Formato inválido de fecha u hora.")
    return render_template("index.html")

@app.route("/contador")
def contador():
    objetivo_str = session.get("objetivo")
    if not objetivo_str:
        return redirect(url_for("home"))
    return render_template("contador.html", objetivo=objetivo_str)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
