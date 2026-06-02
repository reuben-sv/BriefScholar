from modules.groq_client import GroqClient
from modules.pdf_extractor import split_text_into_chunks


class PaperChatbot:
    def __init__(self):
        self.groq = GroqClient()

    def find_relevant_chunks(self, question: str, paper_text: str, top_k: int = 3) -> str:
        """
        Simple keyword-based retrieval.
        Beginner-friendly version without vector database.
        """
        chunks = split_text_into_chunks(paper_text, chunk_size=700)
        question_words = set(question.lower().split())

        scored_chunks = []

        for chunk in chunks:
            chunk_words = set(chunk.lower().split())
            score = len(question_words.intersection(chunk_words))
            scored_chunks.append((score, chunk))

        scored_chunks.sort(reverse=True, key=lambda x: x[0])

        relevant_chunks = [chunk for score, chunk in scored_chunks[:top_k] if score > 0]

        if not relevant_chunks:
            return paper_text[:4000]

        return "\n\n".join(relevant_chunks)

    def answer_question(self, question: str, paper_text: str) -> str:
        context = self.find_relevant_chunks(question, paper_text)

        system_prompt = """
You are a research paper chatbot.
Answer only using the provided paper context.
If the answer is not clearly available in the context, say:
"This information is not clearly available in the uploaded paper."
Do not make up answers.
"""

        user_prompt = f"""
Paper context:
{context}

Question:
{question}

Answer clearly and simply.
"""

        return self.groq.generate_response(system_prompt, user_prompt, temperature=0.2)
