# app.py

from flask import Flask, request, jsonify
from agent import ModelRouterAgent

app = Flask(__name__)
agent = ModelRouterAgent("models_and_reports.yaml", use_hf_model=True)

@app.route("/query", methods=["POST"])
def query():
    data = request.get_json()
    user_query = data.get("query", "")

    if not user_query:
        return jsonify({"error": "No query provided."}), 400

    response = agent.route_query(user_query)
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True, port=5000)
