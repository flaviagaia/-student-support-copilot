from __future__ import annotations

from pathlib import Path

from src.retrieval import retrieve_support_context


def build_support_answer(base_dir: str | Path, question: str, top_k: int = 3) -> dict:
    _, hits = retrieve_support_context(base_dir, question=question, top_k=top_k)
    primary = hits[0]
    secondary = hits[1] if len(hits) > 1 else None

    answer_parts = [f"Based on {primary.title} / {primary.section_title}, {primary.content}"]
    if secondary and secondary.similarity >= 0.15:
        answer_parts.append(f"Additional context from {secondary.title} / {secondary.section_title}: {secondary.content}")

    recommended_channel = "discussion_board"
    if "accommodation" in question.lower():
        recommended_channel = "student_services"
    elif "platform" in question.lower() or "technical" in question.lower():
        recommended_channel = "support_ticket"
    elif "grade" in question.lower():
        recommended_channel = "private_instructor_contact"

    confidence = round(min(max(primary.similarity * 1.9, 0.0), 0.99), 4)

    return {
        "question": question,
        "answer": " ".join(answer_parts),
        "recommended_channel": recommended_channel,
        "confidence": confidence,
        "sources": [
            {
                "doc_id": hit.doc_id,
                "document_type": hit.document_type,
                "title": hit.title,
                "section_title": hit.section_title,
                "similarity": hit.similarity,
            }
            for hit in hits
        ],
        "limitation_note": (
            "This response is grounded only in the local student-support corpus bundled with the MVP. "
            "A production copilot should validate course version, institution policy, and support-process updates."
        ),
    }
