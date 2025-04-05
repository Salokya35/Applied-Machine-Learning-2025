from flask import Flask, request, jsonify
import joblib
from score import score

app = Flask(__name__)
model = joblib.load("spam_model.joblib")

@app.route('/score', methods=['POST'])  # MUST have leading slash
def score_text():
    data = request.get_json()  # Changed from request.json for better compatibility
    text = data.get("text", "")
    prediction, propensity = score(text, model, 0.5)
    return jsonify({
        "prediction": bool(prediction),
        "propensity": float(propensity)
    })

if __name__ == "__main__":
    from werkzeug.serving import make_server
    server = make_server('0.0.0.0', 5000, app)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.shutdown()