# cli.py

from agent import ModelRouterAgent

def main():
    agent = ModelRouterAgent("models_and_reports.yaml", use_hf_model=True)

    print("🔎 AI Agent for DBT Models & Reports\nType 'exit' to quit.\n")
    
    while True:
        user_input = input("❓ Your question: ")
        if user_input.lower() in ["exit", "quit"]:
            print("👋 Goodbye!")
            break
        
        response = agent.route_query(user_input)
        print(f"💡 Suggestion: {response}\n")

if __name__ == "__main__":
    main()
