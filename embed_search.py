# embed_search.py

import yaml
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

class EmbeddingSearch:
    def __init__(self, yaml_file, embedding_model="all-MiniLM-L6-v2"):
        with open(yaml_file, "r") as f:
            self.knowledge = yaml.safe_load(f)
        
        self.entries = []
        self.labels = []
        self.model = SentenceTransformer(embedding_model)

        self.build_index()

    def build_index(self):
        for model, details in self.knowledge.get("dbt_models", {}).items():
            self.entries.append(details["description"])
            self.labels.append(f"DBT Model: {model}")

        for report, details in self.knowledge.get("reports", {}).items():
            self.entries.append(details["description"])
            self.labels.append(f"Report: {report}")

        embeddings = self.model.encode(self.entries, convert_to_numpy=True)
        self.index = faiss.IndexFlatL2(embeddings.shape[1])
        self.index.add(embeddings)

    def search(self, query, top_k=1):
        query_embedding = self.model.encode([query], convert_to_numpy=True)
        distances, indices = self.index.search(query_embedding, top_k)
        results = []
        for idx in indices[0]:
            results.append(self.labels[idx])
        return results
