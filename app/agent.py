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
from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM, AutoModelForCausalLM

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
            # Use a smaller model for faster loading and inference
            model_name = "google/flan-t5-large"
            # model_name = "meta-llama/Llama-2-7b-chat-hf"
            # model_name = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
            tokenizer = AutoTokenizer.from_pretrained(model_name)
            model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
            # model = AutoModelForCausalLM.from_pretrained(model_name)
            
            self.llm = pipeline(
                "text2text-generation",
                model=model,
                tokenizer=tokenizer,
                max_length=800,
                do_sample=False
            )
    def build_prompt(self, user_query, embed_results=None):
        context = "You are an assistant that helps map user questions to the correct dbt model or report.\n\n"

        if embed_results:
            context += "Here are the most relevant candidates based on embeddings:\n"
            for match in embed_results:
                columns = match.get("columns", [])
                match_type = match.get("type", "unknown")
                context += f"- {match.get('name', 'unknown')} (type: {match_type}): {match.get('description', '')}\n"
                context += f"  Columns: {', '.join(columns) if columns else 'unknown'}\n"

        context += "\nUser query: \"{}\"\n".format(user_query)
        context += "\nIMPORTANT SELECTION RULES:\n"
        context += "- If the query asks about 'models' or 'data models', prefer items with type 'model' over 'exposure'\n"
        context += "- If the query asks about 'dashboards' or 'reports', prefer items with type 'exposure'\n"
        context += "- For queries about columns, data, or analysis, choose the most relevant model that contains the data\n"
        context += "\nReturn ONLY a single valid JSON object with these fields:\n"
        context += "- type: 'model' or 'exposure'\n"
        context += "- name: the model or exposure name\n"
        context += "- description: description text\n"
        context += "- columns: list of relevant columns\n"
        context += "- reasoning: short explanation of why this model/exposure matches the query\n"
        context += "Do NOT return anything else.\n"
        context += "\nImportant: In your output, use the actual column names listed above for the selected model/exposure. Do not use placeholder names like 'column1'.\n"
        context += "\nExample output:\n"
        context += '{"type": "model", "name": "some_model_name", "description": "Short description", "columns": ["colA", "colB", "colC"], "reasoning": "Explanation of why this model matches."}'

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
            output = self.llm(prompt, max_length=800, do_sample=False)[0]["generated_text"]
            import json
            generic_columns = set(["colA", "colB", "colC", "column1", "column2", "column3"])
            try:
                result = json.loads(output)
                print("result")
                print(result)
                # If columns, name, or description are generic/missing, replace with actual from top embedding match
                if embed_results and len(embed_results) > 0:
                    top_match = embed_results[0]
                    print("result columns")
                    print(result["columns"])
                    # if "columns" in result and set(result["columns"]).intersection(generic_columns):
                    if "columns" in result:
                        result["columns"] = top_match.get("columns", [])
                    if "url" in top_match and top_match.get("url"):
                        result["url"] = top_match.get("url", "")
                    if ("name" not in result or result["name"] in ["some_model_name", "unknown", ""]):
                        result["name"] = top_match.get("name", "unknown")
                    if ("description" not in result or result["description"] in ["Short description", "", None]):
                        result["description"] = top_match.get("description", "")
                return result
            except Exception:
                # Fallback: try to extract model name from output and build valid JSON
                import re
                print("exception")
                print(output)
                name = None
                description = None
                reasoning = None
                # Try to extract model name
                match_name = re.search(r'"name"\s*:\s*"([^\"]+)"', output)
                if match_name and match_name.group(1) not in ["some_model_name", "unknown", ""]:
                    name = match_name.group(1)
                elif embed_results and len(embed_results) > 0:
                    name = embed_results[0].get("name", "unknown")
                else:
                    name = "unknown"
                # Try to extract description
                match_desc = re.search(r'"description"\s*:\s*"([^\"]+)"', output)
                if match_desc and match_desc.group(1) not in ["Short description", "", None]:
                    description = match_desc.group(1)
                elif embed_results and len(embed_results) > 0:
                    description = embed_results[0].get("description", "")
                else:
                    description = ""
                # Try to extract reasoning
                match_reasoning = re.search(r'"reasoning"\s*:\s*"([^\"]+)"', output)
                if match_reasoning:
                    reasoning = match_reasoning.group(1)
                else:
                    reasoning = "Selected based on embedding match."
                # Always use columns and URL from top embedding match
                columns = []
                url = ""
                if embed_results and len(embed_results) > 0:
                    columns = embed_results[0].get("columns", [])
                    url = embed_results[0].get("url", "")
                return {
                    "type": "model",
                    "name": name,
                    "description": description,
                    "columns": columns,
                    "url": url,
                    "reasoning": reasoning
                }
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
