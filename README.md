# dbt Assistant API

## Overview

This project is a dbt-powered assistant API that makes your data models and business reports searchable and explainable. It combines embedding search, LLM reasoning, and flexible API responses to answer questions about dbt models, columns, and published reports (exposures).

## Features

- Natural language search for dbt models, columns, and exposures (reports/dashboards)
- Returns model details, columns, lineage, and report URLs
- Integrates with Superset by extracting YAML metadata from Superset datasets and exposures
- Unified knowledge graph for analytics assets
- Automated documentation and search for all analytics resources

## Superset Integration

You can link this API with your Superset instance by extracting YAML metadata from Superset datasets and exposures. This enables:

- One-click access to dashboards and reports from your data catalog
- Clear lineage between dbt models and business-facing reports
- Connecting technical data models to business outcomes

### Example: Extracting Superset YAML

1. In Superset, go to a dataset or dashboard and click "Export to YAML".
2. Save the YAML file and add it to your project (e.g., as an exposure).
3. The assistant will parse exposures and make them searchable via the API.

## Why is this useful?

- No more hunting for the right dashboard or model—just ask!
- Empower everyone in your organization to find, understand, and use data
- Automated, up-to-date documentation for all analytics assets

## Usage

1. Build knowledge from dbt models and exposures:
	```bash
	python gunicorn/parser_example_compiled.py
	```
2. Start the API server:
	```bash
	python gunicorn/app.py
	# or
	gunicorn --bind 0.0.0.0:5000 --workers 1 --threads 2 gunicorn/app:app
	```
3. Query the API:
	```bash
	curl -X POST http://localhost:5000/search \
		  -H "Content-Type: application/json" \
		  -d '{"query": "what is url for sales dashboard"}'
	```

## Example API Response

```json
{
  "llm_suggestion": {
	 "type": "exposure",
	 "name": "sales_dashboard",
	 "description": "Sales dashboard for business users.",
	 "columns": ["order_id", "product_id", "sales_amount"],
	 "url": "https://dashboard.example.com/sales",
	 "reasoning": "This exposure is a published dashboard for sales."
  },
  "embedding_matches": [ ... ]
}
```

## Contributing

Pull requests and suggestions are welcome!

## License

MIT
# 🧠 AI Agent for DBT Models & Reports

This is a lightweight Python agent that maps user questions to relevant **dbt models** or **reports** using Hugging Face Transformers (Flan-T5) or OpenAI (commented out).

---

## 🚀 Features
- ✅ Load model/report metadata from YAML
- ✅ Use Hugging Face `flan-t5-base` for prompt-based matching
- ✅ Optional OpenAI support (commented out)
- ✅ CLI tool
- ✅ Flask Web API

---

## 🛠️ Setup

```bash
pip install -r requirements.txt
