# cli.py - Command Line Interface for dbt assistant

from core import DbtAssistant

def main():
    assistant = DbtAssistant("app/models_and_reports.yaml", use_hf_model=True)

    print("🔎 AI Agent with LLM + Embedding Search")
    print("Type 'exit' or 'quit' to quit.\n")

    while True:
        user_input = input("❓ Your question: ")
        if user_input.lower() in ["exit", "quit"]:
            print("👋 Goodbye!")
            break

        # Process query using shared core logic
        result = assistant.process_query(user_input, top_k=5)

        print("\n" + "="*60)
        print("💡 LLM Suggestion:")
        print("-" * 30)
        
        # Display LLM response
        llm_suggestion = result["llm_suggestion"]
        if isinstance(llm_suggestion, dict):
            for key, value in llm_suggestion.items():
                if key == "columns" and isinstance(value, list):
                    print(f"  {key}: {', '.join(value[:10])}{'...' if len(value) > 10 else ''}")
                else:
                    print(f"  {key}: {value}")
        else:
            print(f"  {llm_suggestion}")

        print("\n💡 Embedding-based Top Matches:")
        print("-" * 30)
        
        # Display embedding results
        for i, res in enumerate(result["embedding_matches"], 1):
            print(f"  {i}. {res.get('name', 'Unknown')}")
            if 'description' in res:
                desc = res['description']
                if len(desc) > 80:
                    desc = desc[:80] + "..."
                print(f"     Description: {desc}")
            if 'columns' in res and res['columns']:
                cols = res['columns'][:5]  # Show first 5 columns
                print(f"     Columns: {', '.join(cols)}{'...' if len(res['columns']) > 5 else ''}")
            if 'score' in res:
                print(f"     Score: {res['score']:.3f}")
            print()

        print("="*60)
        print()

if __name__ == "__main__":
    main()