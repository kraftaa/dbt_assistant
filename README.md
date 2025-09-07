# dbt Assistant API

## Overview

This project is a dbt-powered assistant API that makes your data models and business reports searchable and explainable. It combines embedding search, LLM reasoning, and flexible API responses to answer questions about dbt models, columns, and published reports (exposures).

## Project Structure

```
dbt_assistant/
├── dbt_project/           # Your dbt models and configuration
├── app/                   # Main application source code
│   ├── agent.py          # AI agent for query routing
│   ├── app.py            # Flask web API
│   ├── cli.py            # Command-line interface
│   ├── embed_search.py   # Embedding-based search engine
│   ├── parser_example_compiled.py  # Knowledge base builder
│   └── models_and_reports.yaml     # Knowledge base data
├── deploy/                # Deployment configurations
│   ├── Dockerfile        # Docker container setup
│   ├── docker-compose.yml # Docker Compose configuration
│   ├── nginx.conf        # Nginx configuration
│   └── gunicorn_conf.py  # Gunicorn server configuration
├── tests/                 # Test files
│   ├── test_mps.py       # MPS (Apple Silicon) performance test
│   └── torch_gpu_test.py # GPU availability test
├── main.py                # Main entry point script
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

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

## Quick Start

### 1. Build Knowledge Base

First, build the knowledge base from your dbt models:
In `dbt_project` directory:
```
dbt compile --target dev --profiles-dir config
```

```bash
python3 app/parser_example_compiled.py
```

### 2. Run the Assistant

The project provides multiple ways to run the assistant:

#### Option A: Main Script (Recommended)
```bash
# Run CLI (interactive mode)
python3 main.py

# Run API server
python3 main.py api

# Show help
python3 main.py help
```

#### Option B: Direct Module Execution
```bash
# Run CLI directly
python3 app/cli.py

# Run API server directly
python3 app/app.py
```

## Usage

### CLI Tool

The command-line interface provides interactive access to the assistant:

```bash
python3 main.py cli
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

The CLI provides intelligent field filtering based on your query:
- **Columns**: Include `column` or `columns` in your query to see column details
- **Names**: Include `name`, `model`, or `report` to focus on model/report names
- **Descriptions**: Include `description` to see detailed descriptions

### API Server

For production use or integration with other systems:

```bash
python3 main.py api
```

The API will be available at `http://localhost:5000` with the following endpoints:

- `GET /` - Health check
- `GET/POST /search` - Search endpoint

#### Example API Usage

```bash
curl -X POST http://localhost:5000/search \
     -H "Content-Type: application/json" \
     -d '{"query": "what is url for sales dashboard"}'
```

Example questions:
"Show me columns from sales models"
"What dashboards use customer data?"
"Which models feed into the executive dashboard?"
"Show me all bronze layer models"
"What's the URL for the sales dashboard?"

#### Example API Response

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

### Testing GPU/MPS Support

The project includes test files to verify GPU acceleration support:

#### MPS Test (Apple Silicon)
```bash
python3 tests/test_mps.py
```
This script benchmarks matrix multiplication performance on CPU vs MPS (Metal Performance Shaders) for Apple Silicon Macs. It compares computation time between devices and helps verify MPS backend availability.

#### GPU Test
```bash
python3 tests/torch_gpu_test.py
```
A simple test to check if MPS is available and verify basic tensor operations work on the selected device. Useful for troubleshooting GPU acceleration issues.

**Note**: These tests are particularly useful for Apple Silicon Mac users to ensure optimal performance when running the AI models in the agent.

## Deployment

### Docker Deployment

The project includes Docker configuration for easy deployment:

```bash
# Build and run with Docker Compose
cd deploy
docker-compose up --build
```

### Manual Deployment

For manual deployment:

```bash
# Install dependencies
pip3 install -r requirements.txt

# Build knowledge base
python3 app/parser_example_compiled.py

# Run with Gunicorn
gunicorn --bind 0.0.0.0:5000 --workers 1 --threads 2 app.app:app
```

## Contributing

Pull requests and suggestions are welcome!

## License

MIT
