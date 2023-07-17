import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv('.env')

app = Flask(__name__)
CORS(app, resources={r"/predict": {"origins": "https://make-predictions.com"}})


@app.route("/predict", methods=["GET"])
def predict():
    # Perform prediction logic here
    data = request.json()

    # Example response
    response = {"result": "Prediction result"}

    return jsonify(response)

    print("Prediction server running")


if __name__ == "__main__":
    port = os.environ.get("PORT")

    print("port number")
    print(port)
    app.run(port=port)
