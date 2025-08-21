# app_combined_dbt_project.py

from flask import Flask, request, jsonify
from agent import ModelRouterAgent
from embed_search import EmbeddingSearch
from dbt_loader import build_knowledge, export_models_and_reports
import os
app = Flask(__name__)

project_path = "..path to the dbt_project"
exposures_file = os.path.join(project_path, "models", "gold", "exposures.yml")

knowledge = build_knowledge(project_path, exposures_file)
export_models_and_reports(knowledge, "models_and_reports.yaml")

print(knowledge["dbt_models"].keys())   # dbt models
print(knowledge["reports"].keys())      # reports/exposures

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
