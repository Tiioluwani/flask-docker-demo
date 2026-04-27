"""
Flask web app with a scikit-learn linear regression prediction endpoint.
The model is trained on dummy data at startup.
"""

import numpy as np
from flask import Flask, jsonify, request
from sklearn.linear_model import LinearRegression

app = Flask(__name__)

APP_NAME = "flask-sklearn-demo"
APP_VERSION = "1.0.0"

# ---------------------------------------------------------------------------
# Train a simple linear regression model on startup.
# Dummy data: y = 3*x1 + 2*x2 + noise
# ---------------------------------------------------------------------------
_rng = np.random.default_rng(42)
_X_train = _rng.uniform(0, 10, size=(200, 2))
_y_train = 3 * _X_train[:, 0] + 2 * _X_train[:, 1] + _rng.normal(0, 0.5, 200)

model = LinearRegression()
model.fit(_X_train, _y_train)


@app.route("/", methods=["GET"])
def index():
    """Return basic app metadata."""
    return jsonify(
        {
            "app": APP_NAME,
            "version": APP_VERSION,
            "status": "ok",
        }
    )


@app.route("/predict", methods=["POST"])
def predict():
    """
    Accept a JSON body with a 'features' list and return a prediction.

    Expected request body:
        { "features": [x1, x2] }

    The model was trained on two-feature data, so the list must contain
    exactly two numbers.
    """
    body = request.get_json(silent=True)

    if not body or "features" not in body:
        return jsonify({"error": "'features' key is required"}), 400

    features = body["features"]

    if not isinstance(features, list) or len(features) != 2:
        return jsonify({"error": "'features' must be a list of exactly 2 numbers"}), 400

    if not all(isinstance(v, (int, float)) for v in features):
        return jsonify({"error": "all values in 'features' must be numbers"}), 400

    # Reshape to (1, n_features) as required by scikit-learn
    X = np.array(features).reshape(1, -1)
    prediction = model.predict(X)[0]

    return jsonify({"prediction": round(float(prediction), 4)})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
