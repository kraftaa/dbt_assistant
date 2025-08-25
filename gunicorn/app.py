# app.py
from flask import Flask, request, jsonify
import sys
import os
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from embed_search import EmbeddingSearch
from agent import ModelRouterAgent
from build_knowledge  import build_knowledge, export_models_and_reports
# from parser_example
import json

app = Flask(__name__)

from pathlib import Path

# Paths
# project_path = "/Users/maria/Documents/GitHub/sparkle-dbt"
# exposures_file = Path(project_path) / "models" / "gold/exposures.yml"

# Load models + exposures into memory
# knowledge = build_knowledge(project_path, exposures_file)

# Save to yaml
# export_models_and_reports(knowledge, "models_and_reports2.yaml")

# print("✅ Exported knowledge to models_and_reports2.yaml")
search_engine = EmbeddingSearch("models_and_reports.yaml")
agent = ModelRouterAgent("models_and_reports.yaml", use_hf_model=True)
@app.route("/")
def index():
    return "API is running!"

@app.route("/search", methods=["GET", "POST"])
def run_search():
    if request.method == "POST":
        query = request.json.get("query")
    else:
        query = request.args.get("query", "")
    # embed_results = search_engine.search(query, top_k=3)
    # llm_response = agent.route_query(query, embed_results)
    matches = search_engine.search(query, top_k=3)
    # context_text = "\n".join(
    #     f"- {m['name']}: {m['description']}" for m in matches
    # )
    llm_response = agent.route_query(query, matches)

    # llm_response = agent.route_query(
    #     f"User query: {query}\n\nRelevant models:\n{context_text}"
    # )

    return jsonify({
        "llm_suggestion": llm_response,
        "embedding_matches": matches
    })


    # llm_response_text = agent.route_query(query, embed_results)
    # try:
    #     llm_response_json = json.loads(llm_response_text)
    # except json.JSONDecodeError:
    #     llm_response_json = {"error": "LLM output was not valid JSON", "raw_output": llm_response_text}
    #
    # return jsonify({
    #     "llm_suggestion": llm_response_json,
    #     "embedding_matches": embed_results
    # })

    # embed_results = search_engine.search(query, top_k=3)
    # llm_response = agent.route_query(query)
    #
    # return jsonify({
    #     "llm_suggestion": llm_response,
    #     "embedding_matches": embed_results
    # })
    # return jsonify({"results": results})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
# export FLASK_APP=app.py
# export FLASK_ENV=development
# flask run --port 5000
# FLASK_APP=app flask run --host=0.0.0.0 --port=5000

# python app.py
#  or
# gunicorn --bind 0.0.0.0:5000 --workers 1 --threads 2 app:app
# gunicorn --bind 0.0.0.0:5000 --workers 1 --threads 2 --preload app:app
# curl -X POST http://localhost:5000/search \
#                               -H "Content-Type: application/json" \
#                                  -d '{"query": "i need columns from model ..."}' | jq '.embedding_matches[0].columns[:10]'

