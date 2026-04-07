from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from src.sample_data import ensure_corpus


@dataclass
class SupportHit:
    doc_id: str
    document_type: str
    title: str
    section_title: str
    content: str
    similarity: float


def retrieve_support_context(base_dir: str | Path, question: str, top_k: int = 3) -> tuple[pd.DataFrame, list[SupportHit]]:
    dataset = ensure_corpus(base_dir)
    corpus = pd.read_csv(dataset["corpus_path"])

    search_text = corpus["title"].fillna("") + " " + corpus["section_title"].fillna("") + " " + corpus["content"].fillna("")
    vectorizer = TfidfVectorizer(ngram_range=(1, 2), stop_words="english")
    matrix = vectorizer.fit_transform(search_text)
    question_vector = vectorizer.transform([question])
    similarities = cosine_similarity(question_vector, matrix).ravel()

    corpus = corpus.copy()
    corpus["similarity"] = similarities
    ranked = corpus.sort_values("similarity", ascending=False).head(top_k)

    hits = [
        SupportHit(
            doc_id=row.doc_id,
            document_type=row.document_type,
            title=row.title,
            section_title=row.section_title,
            content=row.content,
            similarity=round(float(row.similarity), 4),
        )
        for row in ranked.itertuples(index=False)
    ]
    return corpus, hits
