#!/usr/bin/env python3
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).parents[1]


class ChecklistContractTests(unittest.TestCase):
    def test_catalog_has_233_unique_evidence_gates(self):
        checklist = (ROOT / "CHECKLIST.md").read_text()
        gate_ids = re.findall(r"\*\*([A-Z]+-\d+)", checklist)

        self.assertEqual(len(gate_ids), 233)
        self.assertEqual(len(gate_ids), len(set(gate_ids)))

    def test_corpus_audit_names_the_exact_seven_and_1842_version_blocks(self):
        audit = (ROOT / "CORPUS-AUDIT.md").read_text()

        table_rows = re.findall(
            r"^\| (Janggo|Manta|Scepter|Shard|Vanguard|Yasha|Dagon) \| ([\d,]+) \| ([\d,]+) \|",
            audit,
            re.MULTILINE,
        )
        self.assertEqual(
            table_rows,
            [
                ("Janggo", "775", "28"),
                ("Manta", "14,456", "430"),
                ("Scepter", "16,862", "866"),
                ("Shard", "1,489", "59"),
                ("Vanguard", "7,163", "214"),
                ("Yasha", "5,600", "116"),
                ("Dagon", "3,927", "129"),
            ],
        )
        self.assertIn("**1,842**", audit)
        self.assertIn("**50,272**", audit)

    def test_skill_requires_full_catalog_and_provenance_review(self):
        skill = (ROOT / "SKILL.md").read_text()

        self.assertIn("Read that file completely", skill)
        self.assertIn("CORPUS-AUDIT.md", skill)
        self.assertIn("requires_human_review", skill)


if __name__ == "__main__":
    unittest.main()
