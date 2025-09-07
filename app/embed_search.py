# embed_search.py

import yaml
import faiss
import numpy as np
from pathlib import Path
from sentence_transformers import SentenceTransformer

class EmbeddingSearch:
    def __init__(self, yaml_file, embedding_model="all-MiniLM-L6-v2", index_file="faiss_index.pkl"):
        self.yaml_file = yaml_file
        self.embedding_model = SentenceTransformer(embedding_model)
        self.index_file = Path(index_file)

        # load models/reports from YAML
        self.knowledge = self._load_yaml()

        # FAISS index + id mapping
        self.index = None
        self.id_to_key = []

        # build FAISS index
        self._build_index()
        print(f"✅ Loaded {len(self.knowledge)} knowledge items into FAISS index")

    def _load_yaml(self):
        """Load YAML with dbt models/reports definitions"""
        with open(self.yaml_file, "r") as f:
            return yaml.safe_load(f)

    def _build_index(self):
        """Build FAISS index for all names and descriptions"""
        texts = []
        self.id_to_key = []

        for key, item in self.knowledge.items():
            text = f"{item.get('name','')} - {item.get('description','')}"
            texts.append(text)
            self.id_to_key.append(key)

        embeddings = self.embedding_model.encode(texts, convert_to_numpy=True)

        # normalize (helps cosine similarity)
        embeddings = embeddings / np.linalg.norm(embeddings, axis=1, keepdims=True)

        # create FAISS index
        dim = embeddings.shape[1]
        self.index = faiss.IndexFlatIP(dim)  # inner product == cosine since normalized
        self.index.add(embeddings)

    def search(self, query, top_k=5):
        query_vec = self.embedding_model.encode(query).astype("float32").reshape(1, -1)
        D, I = self.index.search(query_vec, top_k)
        results = []
        for i, dist in zip(I[0], D[0]):
            if i >= 0:
                key = self.id_to_key[i]
                info = self.knowledge[key]
                # print("info")
                # print(info)
                results.append({
                    "name": key,                   # name of the dbt model or report
                    "type": info.get("type", "unknown"),
                    "description": info.get("description", ""),
                    "columns": info.get("columns", []),
                    "tables": info.get("tables", []),
                    "conditions": info.get("conditions", []),
                    "score": float(dist)
                })
        return results
