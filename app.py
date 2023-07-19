import os
import pandas as pd
import pickle
from sklearn.linear_model import LinearRegression
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import LabelEncoder, StandardScaler
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import joblib

load_dotenv('.env')

app = Flask(__name__)
code_backend_url = os.environ.get("CODE_BACKEND_URL")

df = pd.read_csv('std.csv')
df
df['Average Math'] = (df['Math Term 1'] +
                      df['Math Term 2'] + df['Math Term 3']) / 3
df['Average Chemistry'] = (df['Chemistry Term 1'] +
                           df['Chemistry Term 2'] + df['Chemistry Term 3']) / 3
df['Average Physics'] = (df['Physics Term 1'] +
                         df['Physics Term 2'] + df['Physics Term 3']) / 3

X = df[['Age', 'Gender', 'Region', 'District',
        'Language Spoken by Student', 'Attendance']]
y = df[['Average Math', 'Average Physics', 'Average Chemistry']]

categorical_cols = ['Gender', 'Region',
                    'District', 'Language Spoken by Student']

preprocessor = ColumnTransformer(
    transformers=[('encoder', OneHotEncoder(), categorical_cols)],
    remainder='passthrough'
)
X_encoded = preprocessor.fit_transform(X)

model = joblib.load("model.pkl")
model.fit(X_encoded, y)


CORS(app, resources={r"/": {"origins": code_backend_url}})


def subject_mark(sample_subject, prediction_list):
    subjects = ['Math', 'Physics', 'Chemistry']
    for subject, mark in zip(subjects, prediction_list[0]):
        if sample_subject == subject:
            print(f"Predicted mark in {subject}: {mark:.2f}")
            return mark


def language_spoken(region):
    if region == "Western":
        return "Runyankole"
    if region == "Central":
        return "Luganda"
    if region == "Eastern":
        return "Ateso"
    if region == "Northern":
        return "Acholi"


@app.route("/api/v1/predict", methods=["POST"])
def predict():
    prediction_request = request.json
    print(prediction_request)

    sample_input = pd.DataFrame({
        'Age': [prediction_request["age"]],
        'Gender': [prediction_request["gender"]],
        'Region': [prediction_request["region"]],
        'District': [prediction_request["district"]],
        'Language Spoken by Student': [language_spoken(prediction_request["region"])],
        'Attendance': [prediction_request["attendance"]]
    })
    sample_input_encoded = preprocessor.transform(sample_input)

    # Make a prediction
    prediction = model.predict(sample_input_encoded)
    print("Prediction:", prediction)

    subject_prediction_mark = round(subject_mark(
        prediction_request["subject"], prediction))

    print("subject_prediction_mark")
    print(subject_prediction_mark)

    return jsonify({"subject": prediction_request["subject"], "predicted_mark": subject_prediction_mark})


if __name__ == "__main__":
    port = os.environ.get("PORT")

    app.run(debug=True, host='0.0.0.0')

    # Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
