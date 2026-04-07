from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from src.generation import build_support_answer
from src.pipeline import run_pipeline


class StudentSupportCopilotTestCase(unittest.TestCase):
    def test_pipeline_contract(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            summary = run_pipeline(temp_dir)
            self.assertEqual(summary["dataset_source"], "student_support_local_sample")
            self.assertEqual(summary["document_count"], 8)
            self.assertGreaterEqual(summary["top_similarity"], 0.15)
            self.assertGreaterEqual(summary["confidence"], 0.25)

            report = json.loads(Path(summary["report_artifact"]).read_text(encoding="utf-8"))
            self.assertIn("answer", report)
            self.assertGreaterEqual(len(report["sources"]), 2)

    def test_technical_issue_routes_to_support_ticket(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            response = build_support_answer(
                temp_dir,
                question="What should I do if the learning platform is down before a deadline?",
                top_k=3,
            )
            self.assertEqual(response["recommended_channel"], "support_ticket")
            self.assertEqual(response["sources"][0]["doc_id"], "SUP-1004")


if __name__ == "__main__":
    unittest.main()
