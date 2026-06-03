import re
from typing import Any

from backend.modules.simplifier import PaperSimplifier


class CoreViva:
    def __init__(self):
        self.simplifier = PaperSimplifier()

    def generate(self, paper_text: str) -> list[dict[str, Any]]:
        viva_text = self.simplifier.viva_questions(paper_text)
        questions = self._parse_questions(viva_text)

        if questions:
            return questions

        return [
            {
                "id": 1,
                "type": "Comprehension",
                "question": "What is the central idea of this paper?",
                "answer": viva_text.strip(),
            }
        ]

    def _parse_questions(self, text: str) -> list[dict[str, Any]]:
        questions: list[dict[str, Any]] = []
        current_type = "Comprehension"
        current_question = ""
        current_answer = ""

        for raw_line in text.splitlines():
            line = self._clean_line(raw_line)
            if not line:
                continue

            detected_type = self._detect_type(line)
            if detected_type:
                current_type = detected_type
                continue

            question = self._extract_question(line)
            if question:
                if current_question:
                    self._append_question(
                        questions,
                        current_type,
                        current_question,
                        current_answer,
                    )
                current_question = question
                current_answer = ""
                continue

            answer = self._extract_answer(line)
            if answer:
                current_answer = f"{current_answer} {answer}".strip()
            elif current_question:
                current_answer = f"{current_answer} {line}".strip()

        if current_question:
            self._append_question(questions, current_type, current_question, current_answer)

        return questions

    def _append_question(
        self,
        questions: list[dict[str, Any]],
        question_type: str,
        question: str,
        answer: str,
    ) -> None:
        questions.append(
            {
                "id": len(questions) + 1,
                "type": question_type,
                "question": question,
                "answer": answer or "Answer not clearly generated.",
            }
        )

    def _detect_type(self, line: str) -> str:
        lowered = line.lower()

        if "technical" in lowered or "analytical" in lowered:
            return "Analytical"
        if "critical" in lowered:
            return "Critical Thinking"
        if "basic" in lowered or "comprehension" in lowered:
            return "Comprehension"

        return ""

    def _extract_question(self, line: str) -> str:
        match = re.match(r"(?:q(?:uestion)?\s*)?\d+[.)]\s*(.+)", line, flags=re.IGNORECASE)
        if match:
            return self._clean_question(match.group(1))

        match = re.match(r"q(?:uestion)?\s*[:\-]\s*(.+)", line, flags=re.IGNORECASE)
        if match:
            return self._clean_question(match.group(1))

        if line.endswith("?"):
            return self._clean_question(line)

        return ""

    def _extract_answer(self, line: str) -> str:
        match = re.match(r"(?:a|answer)\s*[:\-]\s*(.+)", line, flags=re.IGNORECASE)
        return self._clean_value(match.group(1)) if match else ""

    def _clean_question(self, text: str) -> str:
        text = self._clean_value(text)
        answer_match = re.search(r"\s+(?:answer|a)\s*[:\-]\s*(.+)", text, flags=re.IGNORECASE)
        if answer_match:
            return text[: answer_match.start()].strip()
        return text

    def _clean_line(self, line: str) -> str:
        line = line.strip()
        line = re.sub(r"^\s*[-*]\s*", "", line)
        return self._clean_value(line)

    def _clean_value(self, text: str) -> str:
        text = text.replace("**", "").replace("__", "")
        return text.strip(" -*\t")
