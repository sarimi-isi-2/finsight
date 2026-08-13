from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return jsonify({
        "message": "FinSight AI Service Running"
    })

@app.route("/api/v1/categorize", methods=["POST"])
def categorize():
    data = request.get_json()

    description = data.get("description", "").lower()

    if "makan" in description or "resto" in description:
        category = "Food"
    elif "grab" in description or "gojek" in description:
        category = "Transport"
    elif "listrik" in description:
        category = "Bills"
    else:
        category = "Other"

    return jsonify({
        "description": description,
        "category": category
    })

if __name__ == "__main__":
    app.run(debug=True, port=5000)