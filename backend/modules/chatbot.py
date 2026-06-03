from backend.modules.groq_client import GroqClient
from backend.modules.pdf_extractor import split_text_into_chunks


class PaperChatbot:
    def __init__(self):
        self.groq = GroqClient()

    def find_relevant_chunks(self, question: str, paper_text: str, top_k: int = 2) -> str:
        """
        Simple keyword-based retrieval.
        Beginner-friendly version without vector database.
        """
        chunks = split_text_into_chunks(paper_text, chunk_size=300)
        question_words = self._important_words(question)

        scored_chunks = []

        for chunk in chunks:
            chunk_words = self._important_words(chunk)
            score = len(question_words.intersection(chunk_words))
            scored_chunks.append((score, chunk))

        scored_chunks.sort(reverse=True, key=lambda x: x[0])

        relevant_chunks = [chunk for score, chunk in scored_chunks[:top_k] if score > 0]

        if not relevant_chunks:
            return self._limit_context(paper_text, max_chars=2500)

        return self._limit_context("\n\n".join(relevant_chunks), max_chars=3000)

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

        return self.groq.generate_response(
            system_prompt,
            user_prompt,
            temperature=0.2,
            max_tokens=500,
        )

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
