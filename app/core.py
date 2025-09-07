# core.py - Shared core logic for both CLI and web app

from agent import ModelRouterAgent
from embed_search import EmbeddingSearch

class DbtAssistant:
    def __init__(self, yaml_file, use_hf_model=True):
        self.agent = ModelRouterAgent(yaml_file, use_hf_model=use_hf_model)
        self.searcher = EmbeddingSearch(yaml_file)
    
    def wants_field(self, query, field):
        """Check if the query wants a specific field"""
        return field in query.lower()
    
    def filter_fields(self, obj, query):
        """Filter fields based on query content"""
        if not isinstance(obj, dict):
            return obj
        
        # Determine which fields to include
        include_columns = self.wants_field(query, "column") or self.wants_field(query, "columns")
        include_name = (self.wants_field(query, "name") or 
                       self.wants_field(query, "model") or 
                       self.wants_field(query, "report") or 
                       self.wants_field(query, "dashboard"))
        include_description = (self.wants_field(query, "description") or 
                             self.wants_field(query, "dashboard") or 
                             self.wants_field(query, "model"))
        include_url = (self.wants_field(query, "url") or 
                      self.wants_field(query, "link") or 
                      self.wants_field(query, "dashboard"))
        include_score = self.wants_field(query, "score") or self.wants_field(query, "similarity")
        
        # For queries about models, always include name, description, and columns
        if self.wants_field(query, "model") or self.wants_field(query, "models"):
            include_name = True
            include_description = True
            include_columns = True
        
        filtered = {}
        if include_name and "name" in obj:
            filtered["name"] = obj["name"]
        if include_description and "description" in obj:
            filtered["description"] = obj["description"]
        if include_columns and "columns" in obj:
            filtered["columns"] = obj["columns"]
        if include_url and "url" in obj:
            filtered["url"] = obj["url"]
        # Always include type and reasoning if present
        if "type" in obj:
            filtered["type"] = obj["type"]
        if "reasoning" in obj:
            filtered["reasoning"] = obj["reasoning"]
        if "score" in obj:
            filtered["score"] = obj["score"]
        
        return filtered if filtered else obj
    
    def process_query(self, query, top_k=5):
        """Process a query and return both embedding matches and LLM suggestion"""
        # Get embedding matches
        embed_results = self.searcher.search(query, top_k=top_k)
        
        # Get LLM response with embedding context
        llm_response = self.agent.route_query(query, embed_results)
        
        # Filter both responses
        llm_filtered = self.filter_fields(llm_response, query)
        embed_filtered = [self.filter_fields(res, query) for res in embed_results]
        
        return {
            "llm_suggestion": llm_filtered,
            "embedding_matches": embed_filtered
        }
