# cli_embed.py

from embed_search import EmbeddingSearch

def main():
    searcher = EmbeddingSearch("models_and_reports.yaml")

    print("🔎 Embedding-based Search for DBT Models & Reports\nType 'exit' to quit.\n")

    while True:
        user_input = input("❓ Your question: ")
        if user_input.lower() in ["exit", "quit"]:
            print("👋 Goodbye!")
            break

        results = searcher.search(user_input, top_k=2)
        print("💡 Top Matches:")
        for res in results:
            print(f"- {res}")
        print()

if __name__ == "__main__":
    main()
