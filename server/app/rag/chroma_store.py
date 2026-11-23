"""
ChromaDB persistent vector store wrapping sentence-transformers/all-MiniLM-L6-v2.
100% offline with local_files_only=True and local directory persistence.
"""

import os
from pathlib import Path
from typing import List, Dict, Any, Optional
import chromadb
from chromadb import Documents, EmbeddingFunction, Embeddings
from sentence_transformers import SentenceTransformer

# Enforce strict offline execution
os.environ["HF_HUB_OFFLINE"] = "1"
os.environ["TRANSFORMERS_OFFLINE"] = "1"


class LocalMiniLMEmbeddingFunction(EmbeddingFunction):
    """Offline embedding function wrapping sentence-transformers/all-MiniLM-L6-v2."""

    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name, local_files_only=True)

    def name(self) -> str:
        return "LocalMiniLMEmbeddingFunction"

    def get_config(self) -> Dict[str, Any]:
        return {"model_name": "sentence-transformers/all-MiniLM-L6-v2"}

    def __call__(self, input: Documents) -> Embeddings:
        embeddings = self.model.encode(input, convert_to_numpy=True)
        return embeddings.tolist()


class ChromaStore:
    """Persistent ChromaDB client for indexing and querying agricultural advisory documents."""

    DEFAULT_COLLECTION = "farmer_advisory"

    def __init__(self, persist_dir: Optional[str] = None):
        if persist_dir is None:
            # Default to d:\ARM\server\chroma_db
            persist_dir = str(Path(__file__).resolve().parent.parent.parent / "chroma_db")

        self.persist_dir = Path(persist_dir)
        self.persist_dir.mkdir(parents=True, exist_ok=True)

        self.client = chromadb.PersistentClient(path=str(self.persist_dir))
        self.embedding_function = LocalMiniLMEmbeddingFunction()
        self.collection = self.get_or_create_collection(self.DEFAULT_COLLECTION)

    def get_or_create_collection(self, name: str = DEFAULT_COLLECTION):
        return self.client.get_or_create_collection(
            name=name,
            embedding_function=self.embedding_function,
            metadata={"hnsw:space": "cosine"}
        )

    def count(self) -> int:
        return self.collection.count()

    def is_indexed(self) -> bool:
        return self.count() > 0

    def add_documents(
        self,
        documents: List[str],
        metadatas: List[Dict[str, Any]],
        ids: List[str]
    ) -> None:
        """Add batch of documents into the collection."""
        if not documents:
            return
        self.collection.add(documents=documents, metadatas=metadatas, ids=ids)

    def add_chunks(self, chunks: list) -> None:
        """Add KnowledgeChunk instances directly."""
        if not chunks:
            return
        docs = [c.text for c in chunks]
        metas = [c.metadata for c in chunks]
        ids = [c.chunk_id for c in chunks]
        self.add_documents(documents=docs, metadatas=metas, ids=ids)

    def query(
        self,
        query_text: str,
        n_results: int = 4,
        where: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """Retrieve most relevant chunks for a given query."""
        if self.count() == 0:
            return []

        results = self.collection.query(
            query_texts=[query_text],
            n_results=min(n_results, self.count()),
            where=where
        )

        output = []
        if results and results.get("documents") and len(results["documents"]) > 0:
            docs = results["documents"][0]
            metas = results["metadatas"][0] if results.get("metadatas") else [{}] * len(docs)
            dists = results["distances"][0] if results.get("distances") else [0.0] * len(docs)
            ids = results["ids"][0] if results.get("ids") else [""] * len(docs)

            for doc_id, doc, meta, dist in zip(ids, docs, metas, dists):
                output.append({
                    "id": doc_id,
                    "text": doc,
                    "metadata": meta,
                    "distance": float(dist)
                })
        return output

    def reset(self) -> None:
        """Clear and recreate the collection."""
        try:
            self.client.delete_collection(name=self.DEFAULT_COLLECTION)
        except Exception:
            pass
        self.collection = self.get_or_create_collection(self.DEFAULT_COLLECTION)


_chroma_store_instance: Optional[ChromaStore] = None


def get_chroma_store(persist_dir: Optional[str] = None) -> ChromaStore:
    global _chroma_store_instance
    if _chroma_store_instance is None or persist_dir is not None:
        _chroma_store_instance = ChromaStore(persist_dir=persist_dir)
    return _chroma_store_instance
