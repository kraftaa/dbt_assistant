# app.py
from flask import Flask, request, jsonify
import sys
import os
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from embed_search import EmbeddingSearch
from agent import ModelRouterAgent
from parser_example_compiled import build_knowledge, export_knowledge
import json

app = Flask(__name__)

from pathlib import Path

# Paths
# models_dir = "../dbt_project/models"  # adjust path as needed
models_dir = "../dbt_project/target/compiled/dbt_project/models/gold"
knowledge = build_knowledge(models_dir)
export_knowledge(knowledge, "models_and_reports.yaml")

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
    llm_response = agent.route_query(query, matches)
    print("llm response")
    print(llm_response)

    # Remove columns from response if not requested
    def wants_field(q, field):
        return field in q.lower()

    # Determine which fields to include
    include_columns = wants_field(query, "column") or wants_field(query, "columns")
    include_name = wants_field(query, "name") or wants_field(query, "model") or wants_field(query, "report")
    include_description = wants_field(query, "description")
    include_url = wants_field(query, "url") or wants_field(query, "link")
    include_score = wants_field(query, "score") or wants_field(query, "similarity")
    
    def filter_fields(obj):
        if not isinstance(obj, dict):
            return obj
        filtered = {}
        if include_name and "name" in obj:
            filtered["name"] = obj["name"]
        if include_description and "description" in obj:
            filtered["description"] = obj["description"]
        if include_columns and "columns" in obj:
            filtered["columns"] = obj["columns"]
        if include_url and "url" in obj:
            filtered["url"] = obj["url"]    
        # Always include type and reasoning if present
        if "type" in obj:
            filtered["type"] = obj["type"]
        if "reasoning" in obj:
            filtered["reasoning"] = obj["reasoning"]
        return filtered if filtered else obj

    llm_response_filtered = filter_fields(llm_response)
    matches_filtered = [filter_fields(m) for m in matches]

    return jsonify({
        "llm_suggestion": llm_response_filtered,
        "embedding_matches": matches_filtered
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

