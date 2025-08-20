# cli_combined.py

from agent import ModelRouterAgent
from embed_search import EmbeddingSearch

def main():
    agent = ModelRouterAgent("models_and_reports.yaml", use_hf_model=True)
    searcher = EmbeddingSearch("models_and_reports.yaml")

    print("🔎 AI Agent with LLM + Embedding Search\nType 'exit' to quit.\n")

    while True:
        user_input = input("❓ Your question: ")
        if user_input.lower() in ["exit", "quit"]:
            print("👋 Goodbye!")
            break

        llm_response = agent.route_query(user_input)
        embed_results = searcher.search(user_input, top_k=2)

        print("\n💡 LLM Suggestion:")
        print(f"{llm_response}\n")

        print("💡 Embedding-based Top Matches:")
        for res in embed_results:
            print(f"- {res}")
        print()

if __name__ == "__main__":
    main()
