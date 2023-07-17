import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv('.env')

app = Flask(__name__)
code_backend_url = os.environ.get("CODE_BACKEND_URL")

CORS(app, resources={r"/": {"origins": code_backend_url}})


@app.route("/api/v1/predict", methods=["POST"])
def predict():
    print("request.json")
    print(request.json)

    response = {"result": "Prediction result"}

    print("Prediction server running")
    return jsonify(response)


if __name__ == "__main__":
    port = os.environ.get("PORT")

    app.run(debug=False, host='0.0.0.0')
