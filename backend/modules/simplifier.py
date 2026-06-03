from backend.modules.groq_client import GroqClient


class PaperSimplifier:
    def __init__(self):
        self.groq = GroqClient()

    def summarize_paper(self, paper_text: str) -> str:
        selected_text = self._limit_text(paper_text, max_chars=5000)

        system_prompt = """
        You are an academic assistant. Explain research papers in simple, clear language for college students.
        Avoid unnecessary jargon. Be accurate and do not add information not present in the paper.
        """

        user_prompt = f"""
        Read the following research paper text and generate a simple summary.

        Paper text:
        {selected_text}

        Output format:
        - Title/topic of the paper
        - Authors
        - Main problem addressed
        - Simple summary
        - Main conclusion
        """

        return self.groq.generate_response(system_prompt, user_prompt)

    def key_contributions(self, paper_text: str) -> str:
        selected_text = self._limit_text(paper_text, max_chars=5500)

        system_prompt = "You are a research analysis assistant."

        user_prompt = f"""
        Identify the key contributions of this research paper.

        Paper text:
        {selected_text}

        Give the answer as clear bullet points.
        """

        return self.groq.generate_response(system_prompt, user_prompt)

    def methodology_explanation(self, paper_text: str) -> str:
        selected_text = self._limit_text(paper_text, max_chars=5500)

        system_prompt = """
        You explain technical methodology sections in simple student-friendly language.
        """

        user_prompt = f"""
        Explain the methodology used in this research paper in simple language.

        Paper text:
        {selected_text}

        Include:
        - Dataset/input used if mentioned
        - Techniques or models used
        - Step-by-step working
        - Evaluation method if mentioned
        """

        return self.groq.generate_response(system_prompt, user_prompt)

    def future_scope(self, paper_text: str) -> str:
        selected_text = self._limit_text(paper_text, max_chars=5500)

        system_prompt = "You are a research assistant who suggests realistic future work based on a paper."

        user_prompt = f"""
        Based on the paper below, generate possible future scope points.

        Paper text:
        {selected_text}

        Give realistic future improvements only.
        """

        return self.groq.generate_response(system_prompt, user_prompt)

    def viva_questions(self, paper_text: str) -> str:
        selected_text = self._limit_text(paper_text, max_chars=5500)

        system_prompt = """
        You create viva questions for students based on research papers.
        """

        user_prompt = f"""
        Generate viva questions and short answers from this research paper.

        Paper text:
        {selected_text}

        Output:
        - 10 basic viva questions with answers
        - 5 technical viva questions with answers
        """

        return self.groq.generate_response(system_prompt, user_prompt)

    def generate_all_outputs(self, paper_text: str) -> dict:
        return {
            "summary": self.summarize_paper(paper_text),
            "key_contributions": self.key_contributions(paper_text),
            "methodology": self.methodology_explanation(paper_text),
            "future_scope": self.future_scope(paper_text),
            "viva_questions": self.viva_questions(paper_text),
        }

    def _limit_text(self, paper_text: str, max_chars: int) -> str:
        if len(paper_text) <= max_chars:
            return paper_text

        selected_text = paper_text[:max_chars]
        last_sentence_end = max(
            selected_text.rfind("."),
            selected_text.rfind("?"),
            selected_text.rfind("!"),
        )

        if last_sentence_end > max_chars * 0.7:
            return selected_text[: last_sentence_end + 1]

        return selected_text
