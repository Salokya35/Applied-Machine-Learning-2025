from flask import request, jsonify
from flask_restful import Resource
from src.predict import MODEL_PATH, score, load_model_vectoriser 


class Score(Resource):
    def post(self):
        # Load model and vectorizer
        model, vectoriser = load_model_vectoriser(MODEL_PATH)

        # Extract input text from request
        data = request.get_json()
        text = data.get("text") if data else None

        if not text:
            return jsonify({"error": "No text provided"}), 400

        # Get prediction and propensity score
        prediction, propensity = score(text, model, vectoriser, threshold=0.5)
        return jsonify({"prediction": prediction, "propensity": propensity})
