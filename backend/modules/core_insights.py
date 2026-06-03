import re
from typing import Any

from backend.modules.simplifier import PaperSimplifier


class CoreInsightsBrief:
    def __init__(self):
        self.simplifier = PaperSimplifier()

    def generate(self, paper_text: str) -> dict[str, Any]:
        summary_text = self.simplifier.summarize_paper(paper_text)
        contributions_text = self.simplifier.key_contributions(paper_text)
        metadata = self._extract_metadata_from_paper(paper_text)
        parsed_summary = self._parse_summary_sections(summary_text)

        return {
            "title": (
                parsed_summary.get("title")
                or metadata["title"]
                or "Uploaded Research Paper"
            ),
            "authors": (
                parsed_summary.get("authors")
                or metadata["authors"]
                or "Authors not identified"
            ),
            "abstract": self._extract_abstract(summary_text, parsed_summary),
            "contributions": self._split_bullets(contributions_text),
        }

    def _parse_summary_sections(self, summary_text: str) -> dict[str, str]:
        section_labels = {
            "title": ["title/topic of the paper", "title/topic", "title", "topic"],
            "authors": ["authors", "author"],
            "problem": ["main problem addressed", "problem addressed", "main problem"],
            "summary": ["simple summary", "summary"],
            "conclusion": ["main conclusion", "conclusion"],
        }
        label_lookup = {
            self._normalize_label(label): key
            for key, labels in section_labels.items()
            for label in labels
        }
        sections: dict[str, str] = {}
        current_key = ""

        for raw_line in summary_text.splitlines():
            line = raw_line.strip()
            if not line:
                continue

            cleaned_line = self._strip_markdown(line)
            label, value = self._split_labeled_line(cleaned_line)

            if label:
                key = label_lookup.get(self._normalize_label(label))
                if key:
                    current_key = key
                    if value:
                        sections[key] = self._clean_value(value)
                    continue

            if current_key:
                existing = sections.get(current_key, "")
                sections[current_key] = self._clean_value(f"{existing} {cleaned_line}".strip())

        return {
            key: value
            for key, value in sections.items()
            if value.lower() not in {"not mentioned", "not identified", "unknown", "not available"}
        }

    def _extract_abstract(self, summary_text: str, sections: dict[str, str]) -> str:
        parts = [
            sections.get("problem", ""),
            sections.get("summary", ""),
            sections.get("conclusion", ""),
        ]
        parts = [part for part in parts if part]
        if parts:
            return " ".join(parts)

        lines = []
        for raw_line in summary_text.splitlines():
            line = self._strip_markdown(raw_line.strip())
            label, _ = self._split_labeled_line(line)
            if label and self._normalize_label(label) in {
                "title topic of the paper",
                "title topic",
                "title",
                "topic",
                "authors",
                "author",
            }:
                continue
            if line:
                lines.append(line)

        return " ".join(lines).strip()

    def _split_labeled_line(self, line: str) -> tuple[str, str]:
        line = line.strip(" -*\t")
        match = re.match(r"([^:]+):\s*(.*)$", line)
        if not match:
            return "", ""

        return match.group(1).strip(), match.group(2).strip()

    def _normalize_label(self, label: str) -> str:
        label = label.lower().replace("/", " ")
        label = re.sub(r"[^a-z0-9\s]", "", label)
        return re.sub(r"\s+", " ", label).strip()

    def _strip_markdown(self, text: str) -> str:
        text = re.sub(r"^\s*[-*]\s*", "", text)
        text = text.replace("**", "").replace("__", "")
        return text.strip()

    def _clean_value(self, value: str) -> str:
        return self._strip_markdown(value).strip(" -*\t")

    def _extract_metadata_from_paper(self, paper_text: str) -> dict[str, str]:
        lines = [
            line.strip()
            for line in paper_text[:2500].splitlines()
            if line.strip()
        ]

        title = ""
        authors = ""

        for index, line in enumerate(lines[:12]):
            if self._looks_like_title(line):
                title = line
                author_lines = []

                for next_line in lines[index + 1:index + 5]:
                    if re.search(r"\babstract\b", next_line, flags=re.IGNORECASE):
                        break
                    if self._looks_like_author_line(next_line):
                        author_lines.append(next_line)

                authors = " ".join(author_lines).strip()
                break

        return {"title": title, "authors": authors}

    def _looks_like_title(self, line: str) -> bool:
        lowered = line.lower()
        ignored_terms = ["abstract", "doi", "arxiv", "conference", "journal", "proceedings"]

        return (
            8 <= len(line) <= 180
            and any(char.isalpha() for char in line)
            and not any(term in lowered for term in ignored_terms)
            and not re.match(r"^\d+$", line)
        )

    def _looks_like_author_line(self, line: str) -> bool:
        lowered = line.lower()
        ignored_terms = ["abstract", "introduction", "keywords", "doi", "http", "www."]

        return (
            3 <= len(line) <= 220
            and not any(term in lowered for term in ignored_terms)
            and (
                "," in line
                or " and " in lowered
                or bool(re.search(r"\b[A-Z][a-z]+(?:\s+[A-Z]\.)?(?:\s+[A-Z][a-z]+)+\b", line))
            )
        )

    def _split_bullets(self, text: str) -> list[str]:
        lines = re.split(r"\n+|(?:^|\s)[-*]\s+", text)
        contributions = [
            self._clean_value(line)
            for line in lines
            if self._clean_value(line)
        ]
        return contributions[:6]
