from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re


@dataclass
class RetrievedChunk:
    source: str
    content: str
    score: float


class SimpleRetriever:
    def __init__(self, knowledge_dir: str = "knowledge_base") -> None:
        self.knowledge_path = Path(knowledge_dir)
        self.docs: list[tuple[str, str]] = []

        for file in sorted(self.knowledge_path.glob("*.md")):
            content = file.read_text(encoding="utf-8").strip()
            if content:
                self.docs.append((file.name, content))

    @staticmethod
    def _tokenize(text: str) -> set[str]:
        return {t for t in re.findall(r"[a-zA-Z]+", text.lower()) if len(t) > 2}

    def search(self, query: str, k: int = 2) -> list[RetrievedChunk]:
        query_tokens = self._tokenize(query)
        if not query_tokens:
            return []

        scored: list[RetrievedChunk] = []
        for source, content in self.docs:
            doc_tokens = self._tokenize(content)
            overlap = len(query_tokens & doc_tokens)
            if overlap == 0:
                continue
            score = overlap / max(len(query_tokens), 1)
            scored.append(RetrievedChunk(source=source, content=content, score=score))

        scored.sort(key=lambda c: c.score, reverse=True)
        return scored[:k]
