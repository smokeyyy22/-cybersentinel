from typing import Tuple, List

from ..config import CHROMA_ENABLED


collection = None

try:
    if CHROMA_ENABLED:
        import chromadb
        from chromadb.utils import embedding_functions

        chroma_client = chromadb.PersistentClient(path="./chroma_db")
        try:
            embedding_fn = embedding_functions.DefaultEmbeddingFunction()
        except BaseException as embed_err:
            print(f"Embedding init failed (likely offline): {embed_err}")
            embedding_fn = None

        if embedding_fn:
            try:
                collection = chroma_client.get_collection(
                    name="cybersec_docs", embedding_function=embedding_fn
                )
            except Exception:
                collection = chroma_client.create_collection(
                    name="cybersec_docs", embedding_function=embedding_fn
                )
except BaseException as db_err:
    print(f"Chroma init failed: {db_err}")
    collection = None


def retrieve_context(query: str, n_results: int = 3) -> Tuple[str, List[str]]:
    if not collection:
        return "", []
    try:
        results = collection.query(query_texts=[query], n_results=n_results)
        if results["documents"] and results["documents"][0]:
            context = "\n\n".join(results["documents"][0])
            sources = results.get("metadatas", [[]])[0]
            source_names = [s.get("source", "Unknown") for s in sources]
            return context, source_names
        return "", []
    except Exception as e:
        print(f"Context retrieval error: {e}")
        return "", []


def vector_status() -> tuple[str, int]:
    status = "online" if collection else "offline"
    count = 0
    try:
        if collection:
            count = collection.count()
    except Exception:
        status = "degraded"
    return status, count
