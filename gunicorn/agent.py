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
from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM

from embed_search import EmbeddingSearch  # import your embedding search

class ModelRouterAgent:
    # def __init__(self, yaml_file, use_hf_model=True):
    #     with open(yaml_file, "r") as f:
    #         self.knowledge = yaml.safe_load(f)
    #
    #     self.use_hf_model = use_hf_model
    #     self.search_engine = EmbeddingSearch(yaml_file)  # init embeddings
    #
    #     if use_hf_model:
    #         self.llm = pipeline("text2text-generation", model="google/flan-t5-base")
# google/flan-t5-small
# google/flan-t5-base
# google/flan-t5-large
# google/flan-ul2
    def __init__(self, yaml_file, use_hf_model=True):
        # Load knowledge base
        with open(yaml_file, "r") as f:
            self.knowledge = yaml.safe_load(f)

        self.use_hf_model = use_hf_model
        self.search_engine = EmbeddingSearch(yaml_file)  # initialize embeddings

        if use_hf_model:
            # Initialize a strong instruction-following model
            model_name = "google/flan-t5-base"
            tokenizer = AutoTokenizer.from_pretrained(model_name)
            model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
            self.llm = pipeline(
                "text2text-generation",
                model=model,
                tokenizer=tokenizer,
                max_length=512,    # increase if you have long prompts
                do_sample=False    # deterministic output
            )
    def build_prompt(self, user_query, embed_results=None):
        context = "You are an assistant that helps map user questions to the correct dbt model or report.\n\n"

        if embed_results:
            context += "Here are the most relevant candidates based on embeddings:\n"
            for match in embed_results:
                info = match.get("info", {})
                columns = info.get("columns", [])
                context += f"- {match.get('name', 'unknown')}: {match.get('description', '')}\n"
                context += f"  Columns: {', '.join(columns) if columns else 'unknown'}\n"

        context += f"\nUser query: \"{user_query}\"\n"
        context += (
            "Return ONLY a single valid JSON object with these fields:\n"
            "- type: 'model' or 'exposure'\n"
            "- name: the model or exposure name\n"
            "- description: description text\n"
            "- columns: list of relevant columns\n"
            "- reasoning: short explanation of why this model/exposure matches the query\n"
            "Do NOT return anything else."
        )

        return context





    # def build_prompt(self, user_query, embed_results=None):
    #     context = (
    #         "You are an assistant that helps map user questions to the correct dbt model, exposure, or report.\n\n"
    #         "For each candidate, the columns are listed. Use them to determine which model or exposure contains relevant information.\n\n"
    #     )
    #
    #     if embed_results:
    #         context += "Candidate models/exposures:\n"
    #         for match in embed_results:
    #             key = match.get("key") or match.get("name")
    #             info = self.knowledge.get(key, {})
    #             desc = info.get("description", "No description")
    #             columns = info.get("columns", [])
    #             columns_str = ", ".join(columns) if columns else "No columns listed"
    #             score = match.get("score", 0.0)
    #             context += f"- Name: {key}\n  Description: {desc}\n  Columns: {columns_str}\n  Score: {score:.3f}\n\n"
    #
    #     context += (
    #         f"User query: \"{user_query}\"\n\n"
    #         "Task: Select the **most relevant model or exposure** for this query. "
    #         "Return **only** a single JSON object with the fields: type ('model' or 'exposure'), "
    #         "name, description, columns (list of relevant columns), and reasoning (short explanation of why this is relevant).\n"
    #         "Do not include any text outside this JSON."
    #     )
    #
    #     return context


    def route_query(self, user_query, embed_results=None):
        prompt = self.build_prompt(user_query, embed_results)

        if self.use_hf_model:
            # max_length increased to allow full JSON output
            output = self.llm(prompt, max_length=600, do_sample=False)[0]["generated_text"]
            # Optional: try to parse it as JSON and return, fallback to raw text
            try:
                import json
                return json.loads(output)
            except:
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
