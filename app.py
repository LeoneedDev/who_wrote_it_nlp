from flask import Flask, request, jsonify
import os
from joblib import load

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class Genders(enumerate):
    MALE = "m"
    FEMALE = "f"


app = Flask(__name__)

model = load(os.path.join(BASE_DIR, "model.joblib"))


@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json(force=True, silent=True)
    if data is None:
        return jsonify({"error": "Invalid or missing JSON body"}), 400

    # TODO: Pass data to the model and return the result, e.g.:
    # result = model(data.get("text", ""))
    # return jsonify({"response": result})

    return jsonify({"response": None})


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200


if __name__ == "__main__":
    # Development server — for production use a WSGI server such as Gunicorn
    app.run(host="0.0.0.0", port=5000)
