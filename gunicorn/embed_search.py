# embed_search.py
# embed_search.py
import yaml
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

class EmbeddingSearch:
    def __init__(self, yaml_file, embedding_model="all-MiniLM-L6-v2"):
        with open(yaml_file, "r") as f:
            self.data = yaml.safe_load(f)

        self.model = SentenceTransformer(embedding_model)
        self.items = []
        self.embeddings = {}   # 👈 important
        self._load_embeddings(yaml_file)
        print(f"Loaded {len(self.embeddings)} embeddings")

        # Build embeddings for all items
        for item in self.data.get("items", []):
            name = item.get("name")
            desc = item.get("description", "")
            text = f"{name} {desc}"
            emb = self.model.encode([text], normalize_embeddings=True)[0]
            self.embeddings[name] = emb
            self.items.append({"name": name, "description": desc})

        # Build FAISS index
        if self.embeddings:
            dim = len(next(iter(self.embeddings.values())))
            self.index = faiss.IndexFlatIP(dim)
            self.index.add(np.array(list(self.embeddings.values()), dtype="float32"))
            self.names = list(self.embeddings.keys())
        else:
            self.index = None
            self.names = []

    def search(self, query, top_k=3):
        if not self.index:
            return []

        query_emb = self.model.encode([query], normalize_embeddings=True)
        D, I = self.index.search(np.array(query_emb, dtype="float32"), top_k)

        results = []
        for score, idx in zip(D[0], I[0]):
            name = self.names[idx]
            desc = next((it["description"] for it in self.items if it["name"] == name), "")
            results.append({
                "item": name,
                "description": desc,
                "score": float(score)
            })
        return results

# import yaml
# import numpy as np
# import faiss
# from sentence_transformers import SentenceTransformer
# from pathlib import Path
# import pickle
# from numpy.linalg import norm
#
# class EmbeddingSearch:
#     def __init__(self, yaml_file, embedding_model="all-MiniLM-L6-v2", index_file="faiss_index.pkl"):
#         self.yaml_file = yaml_file
#         self.embedding_model = SentenceTransformer(embedding_model)
#         self.index_file = Path(index_file)
#         self.knowledge = self._load_yaml()
#         self.index = None
#         self.id_to_key = []  # map vector indices back to model/report keys
#         self._build_index()
#
#     def _load_yaml(self):
#         with open(self.yaml_file) as f:
#             return yaml.safe_load(f)
#
#     def _build_index(self):
#         # Try to load from disk first
#         if self.index_file.exists():
#             print("Loading FAISS index from disk...")
#             with open(self.index_file, "rb") as f:
#                 self.index, self.id_to_key = pickle.load(f)
#             return
#
#         # Incremental embeddings: avoids loading everything at once
#         embeddings_list = []
#         self.id_to_key = []
#
#         for key, info in self.knowledge.items():
#             text = info.get("description", "") + "\n" + "\n".join(info.get("columns", []))
#             emb = self.embedding_model.encode(text)
#             embeddings_list.append(emb)
#             self.id_to_key.append(key)
#
#         embeddings = np.vstack(embeddings_list).astype("float32")
#         self.index = faiss.IndexFlatL2(embeddings.shape[1])
#         self.index.add(embeddings)
#
#         # Save to disk for next time
#         with open(self.index_file, "wb") as f:
#             pickle.dump((self.index, self.id_to_key), f)
#         print(f"FAISS index built and saved ({len(self.id_to_key)} items).")
#
#     # def search(self, query, top_k=5):
#     #     query_vec = self.embedding_model.encode(query).astype("float32").reshape(1, -1)
#     #     D, I = self.index.search(query_vec, top_k)
#     #     results = []
#     #     for i, dist in zip(I[0], D[0]):
#     #         if i >= 0:
#     #             key = self.id_to_key[i]
#     #             info = self.knowledge[key]
#     #             results.append({
#     #                 "item": key,
#     #                 "description": info.get("description", ""),
#     #                 "score": float(1.0 - dist)  # convert distance to similarity score
#     #             })
#     #     return results
#
#
#     def search(self, query, top_k=5):
#         query_vec = self.embedding_model.encode(query).astype("float32")
#         scores = []
#         for key, emb in self.embeddings.items():
#             sim = float(np.dot(query_vec, emb) / (norm(query_vec) * norm(emb)))  # cosine similarity
#             scores.append((key, sim))
#         scores = sorted(scores, key=lambda x: x[1], reverse=True)[:top_k]
#
#         results = []
#         for key, score in scores:
#             info = self.knowledge[key]
#             results.append({
#                 "item": key,
#                 "description": info.get("description", ""),
#                 "score": score
#             })
#         return results

# import yaml
# import faiss
# import numpy as np
# import torch
# from sentence_transformers import SentenceTransformer
#
# class EmbeddingSearch:
#     def __init__(self, yaml_file, embedding_model="all-MiniLM-L6-v2"):
#         with open(yaml_file, "r") as f:
#             self.knowledge = yaml.safe_load(f)
#
#         self.entries = []
#         self.labels = []
#
#         # Pick the best device: MPS > CUDA > CPU
#         if torch.backends.mps.is_available():
#             self.device = "mps"
#         elif torch.cuda.is_available():
#             self.device = "cuda"
#         else:
#             self.device = "cpu"
#
#         print(f"[EmbeddingSearch] Using device: {self.device}")
#
#         self.model = SentenceTransformer(embedding_model, device=self.device)
#
#         self.build_index()
#
#     def build_index(self):
#         for model, details in self.knowledge.get("dbt_models", {}).items():
#             self.entries.append(details["description"])
#             self.labels.append(f"DBT Model: {model}")
#
#         for report, details in self.knowledge.get("reports", {}).items():
#             self.entries.append(details["description"])
#             self.labels.append(f"Report: {report}")
#
#         # Encode entries → embeddings
#         embeddings = self.model.encode(
#             self.entries,
#             convert_to_numpy=True,
#             device=self.device
#         )
#         self.index = faiss.IndexFlatL2(embeddings.shape[1])
#         self.index.add(embeddings)
#
#     def search(self, query, top_k=1):
#         query_embedding = self.model.encode(
#             [query],
#             convert_to_numpy=True,
#             device=self.device
#         )
#         distances, indices = self.index.search(query_embedding, top_k)
#         results = []
#         for idx in indices[0]:
#             results.append(self.labels[idx])
#         return results
