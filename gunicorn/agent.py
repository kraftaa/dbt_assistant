# agent.py

import yaml
from transformers import pipeline

# Uncomment to use OpenAI API instead
# import openai

class ModelRouterAgent:
    def __init__(self, yaml_file, use_hf_model=True):
        with open(yaml_file, "r") as f:
            self.knowledge = yaml.safe_load(f)
        
        self.use_hf_model = use_hf_model

        if use_hf_model:
            # self.llm = pipeline("text2text-generation", model="google/flan-t5-base")
            self.llm = pipeline("text2text-generation", model="google/flan-t5-small")
        # else:
        #     openai.api_key = "YOUR_OPENAI_API_KEY"
    
    def build_prompt(self, user_query):
        context = "You are an assistant that helps map user questions to the correct dbt model or report.\n\n"

        context += "DBT Models:\n"
        for model, details in self.knowledge.get("dbt_models", {}).items():
            context += f"- {model}: {details['description']}\n"
        
        context += "\nReports:\n"
        for report, details in self.knowledge.get("reports", {}).items():
            context += f"- {report}: {details['description']}\n"

        context += f"\nUser query: \"{user_query}\"\n"
        context += "Return the best matching dbt model or report with a short explanation."

        return context

    def route_query(self, user_query):
        prompt = self.build_prompt(user_query)

        if self.use_hf_model:
            output = self.llm(prompt, max_length=150)[0]["generated_text"]
            return output
        else:
            # Uncomment this block to use OpenAI API
            # response = openai.ChatCompletion.create(
            #     model="gpt-4",
            #     messages=[
            #         {"role": "system", "content": "You are a helpful assistant."},
            #         {"role": "user", "content": prompt}
            #     ]
            # )
            # return response['choices'][0]['message']['content']
            return "OpenAI option is disabled. Enable it in the code if needed."
