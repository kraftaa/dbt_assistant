g# app.py - Main Flask application for the dbt assistant
from flask import Flask, request, jsonify
import sys
import os
from pathlib import Path

# Import our modules
from agent import ModelRouterAgent
from embed_search import EmbeddingSearch
from build_knowledge_parse import build_knowledge, export_knowledge

app = Flask(__name__)

# Paths
models_dir = "../dbt_project/target/compiled/dbt_project/models/gold"
knowledge = build_knowledge(models_dir)
export_knowledge(knowledge, "../config/models_and_reports.yaml")

search_engine = EmbeddingSearch("../config/models_and_reports.yaml")
agent = ModelRouterAgent("../config/models_and_reports.yaml", use_hf_model=True)

@app.route("/")
def index():
    return "DBT Assistant API is running!"

@app.route("/search", methods=["GET", "POST"])
def run_search():
    if request.method == "POST":
        query = request.json.get("query")
    else:
        query = request.args.get("query", "")
    
    matches = search_engine.search(query, top_k=3)
    llm_response = agent.route_query(query, matches)

    # Remove columns from response if not requested
    def wants_field(q, field):
        return field in q.lower()

    # Determine which fields to include
    include_columns = wants_field(query, "column") or wants_field(query, "columns")
    include_name = wants_field(query, "name") or wants_field(query, "model") or wants_field(query, "report")
    include_description = wants_field(query, "description")

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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
