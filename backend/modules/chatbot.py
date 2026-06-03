from backend.modules.groq_client import GroqClient
from backend.modules.rag_engine import RAGEngine


class PaperChatbot:
    def __init__(self):
        self.groq = GroqClient()
        self.rag = RAGEngine()

    def prepare_paper(self, paper_text: str):
        """
        Builds FAISS vector store after PDF text is extracted.
        """
        return self.rag.build_vector_store(paper_text)

    def answer_question(self, question: str) -> str:
        """
        Answers question using RAG retrieved context.
        """
        context = self.rag.retrieve_relevant_chunks(question, top_k=2)

        system_prompt = """
You are a research paper chatbot.
Answer only using the provided paper context.
If the answer is not clearly available in the context, say:
"This information is not clearly available in the uploaded paper."
Do not make up answers.
Explain in simple student-friendly language.
"""

        user_prompt = f"""
Relevant paper context:
{context}

User question:
{question}

Answer:
"""

        return self.groq.generate_response(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            temperature=0.2,
            max_tokens=500,
        )
