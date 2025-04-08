from flask import Flask, render_template, request, jsonify
from flask_restful import Api
from resource.integrate import Score 

app = Flask(__name__)
api = Api(app)

# Register API endpoint
api.add_resource(Score, "/predict")

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        user_text = request.form.get("text")  # Use `.get()` to avoid KeyError
        if not user_text:
            return render_template("index.html", text=None, result={"error": "No text provided"})
        
        # Call the Flask API internally
        response = app.test_client().post(
            "/predict",
            json={"text": user_text},
        )
        result = response.get_json()  # Extract prediction and propensity
        return render_template("index.html", text=user_text, result=result)
    
    return render_template("index.html", text=None, result=None)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)





