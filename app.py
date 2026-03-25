import http

from flask import Flask, request, jsonify
import os
from enum import Enum
from joblib import load
from sklearn.decomposition import TruncatedSVD
from sklearn.pipeline import Pipeline, FeatureUnion
from util.preprocessing import TweetPreprocessor
from sklearn.feature_extraction.text import TfidfVectorizer


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PIPELINE_PARAMS = {}


class Genders(Enum):
    MALE = "m"
    FEMALE = "f"


app = Flask(__name__)
model_path = os.path.join(BASE_DIR, os.getenv("MODEL_PATH", "model.joblib"))
model = load(model_path)
if model is None:
    raise RuntimeError(f"Failed to load model from {model_path}")


@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json(silent=True)
    if data is None:
        return jsonify({"error": "Invalid or missing JSON body"}), http.HTTPStatus.BAD_REQUEST

    raw_text = data.get("text")
    if not isinstance(raw_text, str) or not raw_text.strip():
        return jsonify({"error": "Field 'text' is required and must be a non-empty string"}), http.HTTPStatus.BAD_REQUEST

    try:
        pipeline = Pipeline([
            ("preprocessor", TweetPreprocessor()),
            ("features", FeatureUnion([
                ("tfidf_word", TfidfVectorizer(analyzer="word")),  # type: ignore
                ("tfidf_char", TfidfVectorizer(analyzer="char")),
            ])),
            ("svd", TruncatedSVD(random_state=int(os.getenv("RANDOM_SEED", 880055535)))),
        ])
        pipeline.set_params(**PIPELINE_PARAMS)

        text = pipeline.fit_transform([raw_text])
        pred = model.predict([text])
        label: int = pred[0]
        label_str: str = "F" if label == 0 else "M"

        return jsonify({"response": label_str}), http.HTTPStatus.OK
    except Exception:
        return jsonify({"error": "Prediction failed"}), http.HTTPStatus.INTERNAL_SERVER_ERROR


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
