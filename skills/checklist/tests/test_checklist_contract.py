#!/usr/bin/env python3
import json
import re
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).parents[1]


class ChecklistContractTests(unittest.TestCase):
    def test_catalog_has_242_unique_evidence_gates(self):
        checklist = (ROOT / "CHECKLIST.md").read_text()
        gate_ids = re.findall(r"\*\*([A-Z]+-\d+)", checklist)

        self.assertEqual(len(gate_ids), 242)
        self.assertEqual(len(gate_ids), len(set(gate_ids)))

    def test_juce_baseline_is_current_pinned_and_identical_across_platforms(self):
        checklist = (ROOT / "CHECKLIST.md").read_text()
        audit = (ROOT / "CORPUS-AUDIT.md").read_text()
        collector = (ROOT / "scripts" / "audit-native-plugin.sh").read_text()

        self.assertIn("BUILD-13", checklist)
        self.assertIn("one repository-owned exact JUCE stable tag or commit", checklist)
        self.assertIn("official latest stable release", checklist)
        self.assertIn("same JUCE version on macOS and Windows", checklist)
        self.assertIn("`BUILD-13`", audit)
        self.assertIn('observe_files "BUILD-13"', collector)

    def test_static_collector_observes_hidden_juce_pin(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            repo = Path(temp_dir)
            (repo / ".juce-version").write_text("8.0.14\n", encoding="utf-8")

            completed = subprocess.run(
                [str(ROOT / "scripts" / "audit-native-plugin.sh"), str(repo)],
                check=True,
                capture_output=True,
                text=True,
            )
            report = json.loads(completed.stdout)
            build_13 = next(item for item in report["observations"] if item["id"] == "BUILD-13")

            self.assertEqual(build_13["static_result"], "observed")
            self.assertIn(".juce-version", build_13["evidence"])

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

    def test_install_requires_a_closed_host_and_fresh_post_install_process(self):
        skill = (ROOT / "SKILL.md").read_text()
        checklist = (ROOT / "CHECKLIST.md").read_text()

        self.assertIn("Pre-install host barrier", skill)
        self.assertIn("newly launched host process", skill)
        self.assertIn("INSTALL-14", checklist)
        self.assertIn("start time is later than the installed bundle replacement", checklist)

    def test_host_visible_refresh_does_not_trust_juce_visibility(self):
        checklist = (ROOT / "CHECKLIST.md").read_text()

        self.assertIn("LIFE-14", checklist)
        self.assertIn("isShowing() == false", checklist)
        self.assertIn("editor construction until destruction", checklist)


if __name__ == "__main__":
    unittest.main()
