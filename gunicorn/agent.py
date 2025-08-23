# # agent.py
#
# import yaml
# from transformers import pipeline
#
# # Uncomment to use OpenAI API instead
# # import openai
#
# class ModelRouterAgent:
#     def __init__(self, yaml_file, use_hf_model=True):
#         with open(yaml_file, "r") as f:
#             self.knowledge = yaml.safe_load(f)
#
#         self.use_hf_model = use_hf_model
#
#         if use_hf_model:
#             # self.llm = pipeline("text2text-generation", model="google/flan-t5-base")
#             self.llm = pipeline("text2text-generation", model="google/flan-t5-small")
#         # else:
#         #     openai.api_key = "YOUR_OPENAI_API_KEY"
#
#     def build_prompt(self, user_query):
#         context = "You are an assistant that helps map user questions to the correct dbt model or report.\n\n"
#
#         context += "DBT Models:\n"
#         for model, details in self.knowledge.get("dbt_models", {}).items():
#             context += f"- {model}: {details['description']}\n"
#
#         context += "\nReports:\n"
#         for report, details in self.knowledge.get("reports", {}).items():
#             context += f"- {report}: {details['description']}\n"
#
#         context += f"\nUser query: \"{user_query}\"\n"
#         context += "Return the best matching dbt model or report with a short explanation."
#
#         return context
#
#     def route_query(self, user_query):
#         prompt = self.build_prompt(user_query)
#
#         if self.use_hf_model:
#             output = self.llm(prompt, max_length=150)[0]["generated_text"]
#             return output
#         else:
#             # Uncomment this block to use OpenAI API
#             # response = openai.ChatCompletion.create(
#             #     model="gpt-4",
#             #     messages=[
#             #         {"role": "system", "content": "You are a helpful assistant."},
#             #         {"role": "user", "content": prompt}
#             #     ]
#             # )
#             # return response['choices'][0]['message']['content']
#             return "OpenAI option is disabled. Enable it in the code if needed."
# agent.py

import yaml
from transformers import pipeline
from embed_search import EmbeddingSearch  # import your embedding search

class ModelRouterAgent:
    def __init__(self, yaml_file, use_hf_model=True):
        with open(yaml_file, "r") as f:
            self.knowledge = yaml.safe_load(f)

        self.use_hf_model = use_hf_model
        self.search_engine = EmbeddingSearch(yaml_file)  # init embeddings

        if use_hf_model:
            self.llm = pipeline("text2text-generation", model="google/flan-t5-small")

    def build_prompt(self, user_query, embed_results=None):
        context = "You are an assistant that helps map user questions to the correct dbt model or report.\n\n"

        if embed_results:
            context += "Here are the most relevant candidates based on embeddings:\n"
            for match in embed_results:
                # Use 'name' from your embedding search results
                context += f"- {match.get('name', 'UNKNOWN')}: {match.get('description', '')} (score: {match.get('score', 0):.3f})\n"

        context += f"\nUser query: \"{user_query}\"\n"
        # context += "Based on the candidates above, return the best matching dbt model or report and briefly explain why you chose it."
        context += """
            Instructions:
    - Return the best matching model(s) or exposure(s).
    - Include the columns that are relevant to the query.
    - Provide a short reasoning for why you chose them.
    - Output in this JSON format(example answer):
    
        [
          {
            "type": "model" or "exposure",
            "name": "model_or_exposure_name",
            "description": "description text",
            "columns": ["column1", "column2"],
            "reasoning": "short explanation"
          }
        ]
    """
        return context

    def route_query(self, user_query, embed_results=None):
        prompt = self.build_prompt(user_query, embed_results)

        if self.use_hf_model:
            output = self.llm(prompt, max_length=150)[0]["generated_text"]
            return output
        else:
            return "OpenAI option is disabled. Enable it in the code if needed."
    # def route_query(self, user_query, top_k=3):
    #     # Step 1: use embeddings
    #     embed_results = self.search_engine.search(user_query, top_k=top_k)
    #
    #     # Step 2: build LLM prompt with only top matches
    #     prompt = self.build_prompt(user_query, embed_results)
    #
    #     if self.use_hf_model:
    #         llm_output = self.llm(prompt, max_length=150)[0]["generated_text"]
    #         return {
    #             "llm_suggestion": llm_output,
    #             "embedding_matches": embed_results
    #         }
    #     else:
    #         return {
    #             "llm_suggestion": "OpenAI option disabled",
    #             "embedding_matches": embed_results
    #         }
