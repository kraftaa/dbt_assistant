# cli_combined.py

from agent import ModelRouterAgent
from embed_search import EmbeddingSearch
import json

def wants_field(query, field):
    """Check if the query wants a specific field"""
    return field in query.lower()

def filter_fields(obj, query):
    """Filter fields based on query content, similar to Flask app"""
    if not isinstance(obj, dict):
        return obj
    
    # Determine which fields to include
    include_columns = wants_field(query, "column") or wants_field(query, "columns")
    include_name = wants_field(query, "name") or wants_field(query, "model") or wants_field(query, "report")
    include_description = wants_field(query, "description")
    
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
    if "url" in obj:
        filtered["url"] = obj["url"]
    if "score" in obj:
        filtered["score"] = obj["score"]
    
    return filtered if filtered else obj

def main():
    agent = ModelRouterAgent("models_and_reports.yaml", use_hf_model=True)
    searcher = EmbeddingSearch("models_and_reports.yaml")

    print("🔎 AI Agent with LLM + Embedding Search")
    print("Type 'exit' or 'quit' to quit.\n")

    while True:
        user_input = input("❓ Your question: ")
        if user_input.lower() in ["exit", "quit"]:
            print("👋 Goodbye!")
            break

        # Get embedding matches first
        embed_results = searcher.search(user_input, top_k=3)
        
        # Get LLM response with embedding context
        llm_response = agent.route_query(user_input, embed_results)

        print("\n" + "="*60)
        print("💡 LLM Suggestion:")
        print("-" * 30)
        
        # Filter and display LLM response
        llm_filtered = filter_fields(llm_response, user_input)
        if isinstance(llm_filtered, dict):
            for key, value in llm_filtered.items():
                if key == "columns" and isinstance(value, list):
                    print(f"  {key}: {', '.join(value[:10])}{'...' if len(value) > 10 else ''}")
                else:
                    print(f"  {key}: {value}")
        else:
            print(f"  {llm_filtered}")

        print("\n💡 Embedding-based Top Matches:")
        print("-" * 30)
        
        # Filter and display embedding results
        for i, res in enumerate(embed_results, 1):
            filtered_res = filter_fields(res, user_input)
            print(f"  {i}. {filtered_res.get('name', 'Unknown')}")
            if 'description' in filtered_res:
                desc = filtered_res['description']
                if len(desc) > 80:
                    desc = desc[:80] + "..."
                print(f"     Description: {desc}")
            if 'columns' in filtered_res and filtered_res['columns']:
                cols = filtered_res['columns'][:5]  # Show first 5 columns
                print(f"     Columns: {', '.join(cols)}{'...' if len(filtered_res['columns']) > 5 else ''}")
            if 'score' in filtered_res:
                print(f"     Score: {filtered_res['score']:.3f}")
            print()

        print("="*60)
        print()

if __name__ == "__main__":
    main()
