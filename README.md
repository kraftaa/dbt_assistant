# dbt Assistant

## Overview

This project is an AI-powered dbt assistant that makes your data models and business reports searchable and explainable. It combines **semantic search** with **LLM reasoning** to answer natural language questions about dbt models, columns, and published reports (exposures).

## Key Features

- 🔍 **Semantic Search**: Uses FAISS vector embeddings to find relevant models based on meaning, not just keywords
- 🤖 **LLM Reasoning**: Applies AI to select the best match and provide structured responses
- 🎯 **Smart Filtering**: Automatically includes relevant fields (name, description, columns) based on your query
- 🚀 **Dual Interface**: Both CLI and web API with identical functionality
- 📊 **Model vs Dashboard Distinction**: Intelligently distinguishes between dbt models and business dashboards

## Architecture

```
dbt_assistant/
├── dbt_project/           # Your dbt models and configuration
├── app/                   # Main application source code
│   ├── core.py           # 🆕 Shared business logic (DbtAssistant class)
│   ├── agent.py          # AI agent for query routing
│   ├── app.py            # Flask web API (uses core.py)
│   ├── cli.py            # Command-line interface (uses core.py)
│   ├── embed_search.py   # Embedding-based search engine
│   ├── parser_dbt_compiled.py  # Knowledge base builder
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

## How It Works

1. **Knowledge Base**: Extracts dbt models and exposures into a searchable YAML format
2. **Embedding Search**: Converts model names/descriptions to vectors for semantic similarity
3. **Smart Reordering**: Prioritizes dbt models over dashboards when query mentions "models"
4. **LLM Selection**: Uses AI to choose the best match and provide reasoning
5. **Response Filtering**: Intelligently includes relevant fields based on query context

## Architecture Benefits

The project uses a **shared core architecture** (`core.py`) that both CLI and web API interfaces use:

- **🔄 Consistent Behavior**: CLI and web API provide identical responses
- **🛠️ Easy Maintenance**: Business logic changes only need to be made in one place
- **🧪 Better Testing**: Core logic can be tested independently
- **📦 Clean Separation**: Each interface focuses only on its presentation layer

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
python3 app/parser_dbt_compiled.py
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
  name: fct_sales
  description: DBT model located at ../dbt_project/target/compiled/dbt_project/models/gold/fct_sales.sql
  columns: order_id AS order_id, product_id AS product_id, total_amount AS sales_amount
  type: model
  reasoning: Selected based on embedding match.

💡 Embedding-based Top Matches:
------------------------------
  1. fct_sales
     Description: DBT model located at ../dbt_project/target/compiled/dbt_project/models/gold/fct_sales.sql
     Columns: order_id AS order_id, product_id AS product_id, total_amount AS sales_amount
     Score: 0.320

  2. dim_products
     Description: DBT model located at ../dbt_project/target/compiled/dbt_project/models/gold/dim_products.sql
     Columns: product_id AS product_id, product_name AS product_name, category AS category, price AS price
     Score: 0.291

  3. dim_customers
     Description: DBT model located at ../dbt_project/target/compiled/dbt_project/models/gold/dim_customers.sql
     Columns: customer_id AS customer_id, customer_name AS customer_name, email AS email
     Score: 0.252

  4. sales_dashboard
     Description: Sales dashboard for business users.
     Score: 0.469

  5. executive_dashboard
     Description: Executive-level dashboard for revenue and customer KPIs
     Score: 0.296

============================================================
```

**Key Features:**
- **Smart Model Selection**: When you ask about "models", it prioritizes actual dbt models over dashboards
- **Automatic Field Inclusion**: Queries about "models" automatically include name, description, and columns
- **Semantic Understanding**: Finds `fct_sales` even though it doesn't contain the word "sales" in the name

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
    "description": "Sales dashboard for business users.",
    "name": "sales_dashboard",
    "reasoning": "Selected based on embedding match.",
    "type": "model"
  },
  "embedding_matches": [
    {
      "description": "Sales dashboard for business users.",
      "name": "sales_dashboard",
      "score": 0.6779011487960815,
      "type": "exposure"
    },
    {
      "description": "Executive-level dashboard for revenue and customer KPIs",
      "name": "executive_dashboard",
      "score": 0.45495134592056274,
      "type": "exposure"
    },
    {
      "description": "DBT model located at ../dbt_project/target/compiled/dbt_project/models/gold/fct_sales.sql",
      "name": "fct_sales",
      "score": 0.2082435041666031,
      "type": "dbt_model"
    }
  ]
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
python3 app/parser_dbt_compiled.py

# Run with Gunicorn
gunicorn --bind 0.0.0.0:5000 --workers 1 --threads 2 app.app:app
```

## Contributing

Pull requests and suggestions are welcome!

## License

MIT
