try:
    import faiss
    import numpy as np
    from sentence_transformers import SentenceTransformer
except ImportError:
    faiss = None
    np = None
    SentenceTransformer = None

from backend.modules.pdf_extractor import split_text_into_chunks


class RAGEngine:
    def __init__(self):
        self.embedding_model = None
        self.index = None
        self.chunks = []
        self.use_vector_search = False

        if SentenceTransformer is not None:
            try:
                self.embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
                self.use_vector_search = True
            except Exception:
                self.embedding_model = None

    def build_vector_store(self, paper_text: str):
        """
        Converts paper chunks into embeddings and stores them in FAISS.
        """
        self.chunks = split_text_into_chunks(paper_text, chunk_size=250)

        if not self.chunks:
            raise ValueError("No text chunks found from the paper.")

        if not self.use_vector_search:
            return {
                "message": "Keyword retrieval prepared successfully",
                "total_chunks": len(self.chunks),
            }

        embeddings = self.embedding_model.encode(self.chunks)

        embeddings = np.array(embeddings).astype("float32")

        dimension = embeddings.shape[1]

        self.index = faiss.IndexFlatL2(dimension)

        self.index.add(embeddings)

        return {
            "message": "Vector store created successfully",
            "total_chunks": len(self.chunks)
        }

    def retrieve_relevant_chunks(self, question: str, top_k: int = 3) -> str:
        """
        Retrieves most relevant chunks using semantic similarity search.
        """
        if self.index is None:
            return self._keyword_retrieve(question, top_k=top_k)

        question_embedding = self.embedding_model.encode([question])
        question_embedding = np.array(question_embedding).astype("float32")

        distances, indices = self.index.search(question_embedding, top_k)

        relevant_chunks = []

        for idx in indices[0]:
            if idx < len(self.chunks):
                relevant_chunks.append(self.chunks[idx])

        return self._limit_context("\n\n".join(relevant_chunks), max_chars=3000)

    def _keyword_retrieve(self, question: str, top_k: int) -> str:
        question_words = self._important_words(question)
        scored_chunks = []

        for chunk in self.chunks:
            chunk_words = self._important_words(chunk)
            score = len(question_words.intersection(chunk_words))
            scored_chunks.append((score, chunk))

        scored_chunks.sort(reverse=True, key=lambda item: item[0])
        relevant_chunks = [chunk for score, chunk in scored_chunks[:top_k] if score > 0]

        if not relevant_chunks:
            relevant_chunks = self.chunks[:1]

        return self._limit_context("\n\n".join(relevant_chunks), max_chars=3000)

    def _important_words(self, text: str) -> set[str]:
        stop_words = {
            "a",
            "an",
            "and",
            "are",
            "as",
            "at",
            "be",
            "by",
            "for",
            "from",
            "in",
            "is",
            "it",
            "of",
            "on",
            "or",
            "that",
            "the",
            "this",
            "to",
            "was",
            "what",
            "which",
            "with",
        }
        words = {
            word.strip(".,;:!?()[]{}\"'").lower()
            for word in text.split()
        }
        return {word for word in words if len(word) > 2 and word not in stop_words}

    def _limit_context(self, text: str, max_chars: int) -> str:
        if len(text) <= max_chars:
            return text

        selected_text = text[:max_chars]
        last_sentence_end = max(
            selected_text.rfind("."),
            selected_text.rfind("?"),
            selected_text.rfind("!"),
        )

        if last_sentence_end > max_chars * 0.65:
            return selected_text[: last_sentence_end + 1]

        return selected_text
