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

### API Server

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

### CLI Tool

The project also includes a command-line interface that provides the same functionality without needing to run a web server:

1. Build knowledge from dbt models and exposures:
	```bash
	python gunicorn/parser_example_compiled.py
	```

2. Run the CLI tool:
	```bash
	python gunicorn/cli_combined.py
	```

3. Or run a demo to see functionality without interaction:
	```bash
	python gunicorn/demo_cli.py
	```

#### CLI Example Output

```
🔎 AI Agent with LLM + Embedding Search
Type 'exit' or 'quit' to quit.

❓ Your question: show me columns from sales models

============================================================
💡 LLM Suggestion:
------------------------------
  type: model
  name: fct_sales
  description: Fact table containing sales transactions with revenue metrics
  columns: order_id, product_id, customer_id, sales_amount, order_date
  reasoning: This model contains sales data with detailed transaction information

💡 Embedding-based Top Matches:
------------------------------
  1. fct_sales
     Description: Fact table containing sales transactions with revenue metrics
     Columns: order_id, product_id, customer_id, sales_amount, order_date
     Score: 0.847

  2. sales_dashboard
     Description: Executive dashboard showing sales performance metrics
     Columns: total_sales, sales_count, avg_order_value
     Score: 0.623

  3. dim_products
     Description: Product dimension table with category information
     Columns: product_id, product_name, category, price
     Score: 0.412

============================================================
```

The CLI provides the same intelligent field filtering as the API:
- **Columns**: Include `column` or `columns` in your query to see column details
- **Names**: Include `name`, `model`, or `report` to focus on model/report names
- **Descriptions**: Include `description` to see detailed descriptions

### Testing GPU/MPS Support

The project includes test files to verify GPU acceleration support:

#### MPS Test (Apple Silicon)
```bash
python test_mps.py
```
This script benchmarks matrix multiplication performance on CPU vs MPS (Metal Performance Shaders) for Apple Silicon Macs. It compares computation time between devices and helps verify MPS backend availability.

#### GPU Test
```bash
python torch_gpu_test.py
```
A simple test to check if MPS is available and verify basic tensor operations work on the selected device. Useful for troubleshooting GPU acceleration issues.

**Note**: These tests are particularly useful for Apple Silicon Mac users to ensure optimal performance when running the AI models in the agent.

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

```
