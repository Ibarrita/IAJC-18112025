from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import requests

app = Flask(__name__)
app.secret_key = "s3cr3t4"
API = "https://api.spoonacular.com/recipes/complexSearch"
KEY = "bfb179e20d8e4eb9bafa8bf135f88bca"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/search", methods=["POST"])
def search():
    recipe_name = request.form.get("recipe", "").strip().lower()
    
    if not recipe_name:
        flash("Por favor, ingresa un alimento", "error")
        return redirect(url_for("index"))
    try:
        response = requests.get(f"{API}?apiKey={KEY}&query={recipe_name}&maxFat=25&number=1")
        
        if response.status_code == 200:
            recipe_data = response.json()
            results = recipe_data.get("results", [])
            if not results:
                flash("No se encontró el alimento", "error")
                return redirect(url_for("index"))
            resultados = results[0]
            recipe_info = {
                "title": resultados.get("title"),
                "image": resultados.get("image")
            }
            return render_template("alimento.html", recipe=recipe_info)
        else:
            flash("Error al contactar con la API", "error")
            return redirect(url_for("index"))
    except requests.exceptions.RequestException as e:
        flash("No se pudo contactar con la API", "error")
        return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)