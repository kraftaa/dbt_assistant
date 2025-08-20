# app_combined.py

from flask import Flask, request, jsonify
from agent import ModelRouterAgent
from embed_search import EmbeddingSearch

app = Flask(__name__)

agent = ModelRouterAgent("models_and_reports.yaml", use_hf_model=True)
searcher = EmbeddingSearch("models_and_reports.yaml")

@app.route("/query", methods=["POST"])
def query():
    data = request.get_json()
    user_query = data.get("query", "")

    if not user_query:
        return jsonify({"error": "No query provided."}), 400

    llm_response = agent.route_query(user_query)
    embed_results = searcher.search(user_query, top_k=2)

    return jsonify({
        "llm_suggestion": llm_response,
        "embedding_matches": embed_results
    })

if __name__ == "__main__":
    app.run(debug=True, port=5000)
