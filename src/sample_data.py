from __future__ import annotations

import json
from pathlib import Path
from tempfile import NamedTemporaryFile

import pandas as pd


PUBLIC_DATASET_REFERENCE = {
    "dataset_name": "Student support knowledge base style corpus",
    "dataset_reference": "Local academic support corpus with FAQ, policy, calendar, and support process content.",
    "dataset_note": (
        "This repository uses a deterministic local knowledge base so the support copilot remains fully testable, "
        "grounded, and independent from external APIs."
    ),
}


def _atomic_write_csv(df: pd.DataFrame, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with NamedTemporaryFile("w", suffix=".csv", delete=False, dir=path.parent, encoding="utf-8") as tmp_file:
        temp_path = Path(tmp_file.name)
    try:
        df.to_csv(temp_path, index=False)
        temp_path.replace(path)
    finally:
        if temp_path.exists():
            temp_path.unlink()


def _atomic_write_json(payload: dict, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with NamedTemporaryFile("w", suffix=".json", delete=False, dir=path.parent, encoding="utf-8") as tmp_file:
        temp_path = Path(tmp_file.name)
    try:
        temp_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        temp_path.replace(path)
    finally:
        if temp_path.exists():
            temp_path.unlink()


def _build_corpus() -> pd.DataFrame:
    rows = [
        {
            "doc_id": "SUP-1001",
            "document_type": "faq",
            "title": "Student FAQ",
            "section_title": "Late Work",
            "content": (
                "Assignments submitted within 48 hours after the deadline may still receive partial credit. "
                "After that period, students need prior instructor approval for any additional consideration."
            ),
        },
        {
            "doc_id": "SUP-1002",
            "document_type": "calendar",
            "title": "Course Calendar",
            "section_title": "Exam Schedule",
            "content": (
                "The midterm is scheduled for October 3 and the final project presentation for November 21. "
                "Any schedule change is announced in the learning platform and in the weekly digest."
            ),
        },
        {
            "doc_id": "SUP-1003",
            "document_type": "policy",
            "title": "Accommodation Policy",
            "section_title": "How to Request Support",
            "content": (
                "Students requesting accommodations should contact student services and provide documentation as early as possible. "
                "Instructors implement accommodations after receiving the official support notice."
            ),
        },
        {
            "doc_id": "SUP-1004",
            "document_type": "support_process",
            "title": "Technical Support Process",
            "section_title": "Platform Issues",
            "content": (
                "If the learning platform is unavailable, students should open a support ticket, attach screenshots when possible, "
                "and notify the instructor if an assignment deadline is affected."
            ),
        },
        {
            "doc_id": "SUP-1005",
            "document_type": "faq",
            "title": "Student FAQ",
            "section_title": "Office Hours",
            "content": (
                "Office hours take place every Tuesday from 6 PM to 7 PM Eastern Time. "
                "Students should use them for conceptual blockers, project feedback, and rubric clarification."
            ),
        },
        {
            "doc_id": "SUP-1006",
            "document_type": "policy",
            "title": "Academic Integrity Policy",
            "section_title": "Allowed and Disallowed AI Usage",
            "content": (
                "Students may use AI tools for brainstorming when the assignment explicitly allows it. "
                "They must disclose that assistance. Submitting AI-generated work as original content without disclosure violates policy."
            ),
        },
        {
            "doc_id": "SUP-1007",
            "document_type": "assignment_guide",
            "title": "Project Submission Guide",
            "section_title": "Required Deliverables",
            "content": (
                "The final submission must include a GitHub repository, a short architecture note, and a demo video. "
                "The repository should contain reproducible instructions and automated tests."
            ),
        },
        {
            "doc_id": "SUP-1008",
            "document_type": "support_process",
            "title": "Discussion Board Guidelines",
            "section_title": "When to Post Publicly",
            "content": (
                "Students should post conceptual and course-wide questions in the discussion board before requesting private support. "
                "Private channels should be reserved for grades, accommodations, and personal matters."
            ),
        },
    ]
    return pd.DataFrame(rows)


def ensure_corpus(base_dir: str | Path) -> dict[str, str]:
    base_path = Path(base_dir)
    corpus_path = base_path / "data" / "raw" / "student_support_corpus.csv"
    reference_path = base_path / "data" / "raw" / "public_dataset_reference.json"

    corpus_df = _build_corpus()
    _atomic_write_csv(corpus_df, corpus_path)
    _atomic_write_json(PUBLIC_DATASET_REFERENCE, reference_path)

    return {
        "corpus_path": str(corpus_path),
        "reference_path": str(reference_path),
    }
