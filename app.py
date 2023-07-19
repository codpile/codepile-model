import os
import pandas as pd
import numpy as np
import pickle
from sklearn.linear_model import LinearRegression
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
# from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.preprocessing import LabelEncoder, StandardScaler
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import joblib

load_dotenv('.env')

app = Flask(__name__)
code_backend_url = os.environ.get("CODE_BACKEND_URL")
# model = pickle.load(open('model.pkl', 'rb'))
# model = joblib.load('model.pkl')


# Load the training data
df_train = pd.read_csv('std.csv')

# Extract the input features and target variables from the training data
X_train = df_train[['Age', 'Gender', 'Region', 'District',
                    'Language Spoken by Student', 'Attendance']]
y_train = df_train[['Average Math', 'Average Physics', 'Average Chemistry']]

# Define the categorical columns for one-hot encoding
categorical_cols = ['Gender', 'Region',
                    'District', 'Language Spoken by Student']

# Initialize the ColumnTransformer with the desired transformations
preprocessor = ColumnTransformer(
    transformers=[('encoder', OneHotEncoder(), categorical_cols)],
    remainder='passthrough'
)

# Fit the ColumnTransformer on the training data
preprocessor.fit(X_train)

# # Save the fitted preprocessor for later use
# joblib.dump(preprocessor, 'preprocessor.pkl')
# # Load the fitted preprocessor (if needed in a different script)
# preprocessor = joblib.load('preprocessor.pkl')

CORS(app, resources={r"/": {"origins": code_backend_url}})


@app.route("/api/v1/predict", methods=["POST"])
def predict():
    print("request.json")
    print(request.json)

    print("model")
    print(model)

    # Sample input data
    sample_input = pd.DataFrame({
        'Age': [16],
        'Gender': ['Female'],
        'Region': ['Eastern'],
        'District': ['Mbarara'],
        'Language Spoken by Student': ['Runyankole'],
        'Attendance': [0.87]
    })

    # Transform the sample input using the fitted ColumnTransformer
    sample_input_encoded = preprocessor.transform(sample_input)

    # Load the trained model
    model = joblib.load('model.pkl')

    # Make predictions using the model
    prediction = model.predict(sample_input_encoded)

    print("Prediction made")
    print(prediction)

    return jsonify({"status": "success"})


if __name__ == "__main__":
    port = os.environ.get("PORT")

    app.run(debug=True, host='0.0.0.0')
