import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from modules.pdf_extractor import split_text_into_chunks


class RAGEngine:
    def __init__(self):
        self.embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
        self.index = None
        self.chunks = []

    def build_vector_store(self, paper_text: str):
        """
        Converts paper chunks into embeddings and stores them in FAISS.
        """
        self.chunks = split_text_into_chunks(paper_text, chunk_size=500)

        if not self.chunks:
            raise ValueError("No text chunks found from the paper.")

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
            raise ValueError("Vector store is not created. Upload a paper first.")

        question_embedding = self.embedding_model.encode([question])
        question_embedding = np.array(question_embedding).astype("float32")

        distances, indices = self.index.search(question_embedding, top_k)

        relevant_chunks = []

        for idx in indices[0]:
            if idx < len(self.chunks):
                relevant_chunks.append(self.chunks[idx])

        return "\n\n".join(relevant_chunks)
