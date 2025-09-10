# app.py - Web API for dbt assistant

from flask import Flask, request, jsonify
from core import DbtAssistant
from parser_dbt_compiled import build_knowledge, export_knowledge

app = Flask(__name__)

# Build knowledge base (optional - can be done separately)
models_dir = "../dbt_project/target/compiled/dbt_project/models/gold"
knowledge = build_knowledge(models_dir)
export_knowledge(knowledge, "models_and_reports.yaml")

# Initialize assistant
assistant = DbtAssistant("app/models_and_reports.yaml", use_hf_model=True)
@app.route("/")
def index():
    return "API is running!"

@app.route("/search", methods=["GET", "POST"])
def run_search():
    if request.method == "POST":
        query = request.json.get("query")
    else:
        query = request.args.get("query", "")
    
    # Process query using shared core logic
    result = assistant.process_query(query, top_k=3)
    
    return jsonify(result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

