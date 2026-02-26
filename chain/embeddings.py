from sentence_transformers import SentenceTransformer
from langchain.embeddings.base import Embeddings
from config import EMBED_MODEL
import torch

_model = None

def get_model():
    global _model
    if _model is None:
        device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"Loading embedding model on: {device}")
        _model = SentenceTransformer(EMBED_MODEL, device=device)
        print("Embedding model loaded!")
    return _model

class RepoEmbeddings(Embeddings):
    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        return get_model().encode(
            texts,
            normalize_embeddings=True
        ).tolist()

    def embed_query(self, text: str) -> list[float]:
        return get_model().encode(
            text,
            normalize_embeddings=True
        ).tolist()

def get_embeddings() -> RepoEmbeddings:
    return RepoEmbeddings()