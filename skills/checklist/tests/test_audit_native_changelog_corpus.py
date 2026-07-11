#!/usr/bin/env python3
import json
import subprocess
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).parents[1] / "scripts" / "audit-native-changelog-corpus.py"
PRODUCTS = {
    "Janggo": "janggonative",
    "Manta": "mantanative",
    "Scepter": "scepternative",
    "Shard": "splitter",
    "Vanguard": "vanguardnative",
    "Yasha": "yashanative",
    "Dagon": "dagon",
}


class NativeChangelogCorpusAuditTests(unittest.TestCase):
    def test_accounts_for_every_line_and_every_version_block(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            workspace = Path(temp_dir)
            for index, repo in enumerate(PRODUCTS.values()):
                changelog = workspace / repo / "CHANGELOG.md"
                changelog.parent.mkdir()
                content = (
                    f"# Product {index}\n"
                    "Preamble text.\n"
                    "## v1.1.0 - focus and zoom fix\n"
                    "Returned keyboard focus to the host and persisted zoom.\vStill one physical line.\n"
                    "## [1.0.0] - initial release\n"
                    "Built VST3, AU, and Standalone.\n"
                )
                if repo == "mantanative":
                    changelog.write_bytes(content.replace("Preamble", "Pre\x00amble").encode())
                else:
                    changelog.write_text(content)

            completed = subprocess.run(
                ["python3", str(SCRIPT), str(workspace)],
                check=True,
                capture_output=True,
                text=True,
            )
            report = json.loads(completed.stdout)

            self.assertEqual(report["schema"], "mt-native-changelog-corpus-v1")
            self.assertEqual(report["product_count"], 7)
            self.assertEqual(report["version_entry_count"], 14)
            self.assertTrue(report["all_lines_accounted_for"])
            self.assertEqual({product["product"] for product in report["products"]}, set(PRODUCTS))

            manta = next(product for product in report["products"] if product["product"] == "Manta")
            self.assertTrue(manta["contained_nul_bytes"])
            self.assertEqual(manta["version_entry_count"], 2)
            self.assertEqual(manta["line_count"], 6)
            self.assertEqual(manta["accounted_line_count"], manta["line_count"])
            self.assertEqual(manta["entries"][0]["start_line"], 3)
            self.assertEqual(manta["entries"][0]["end_line"], 4)
            self.assertIn("focus", manta["entries"][0]["categories"])
            self.assertIn("zoom", manta["entries"][0]["categories"])
            self.assertEqual(manta["entries"][0]["semantic_status"], "requires_human_review")

    def test_fails_when_one_of_the_seven_changelogs_is_missing(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            completed = subprocess.run(
                ["python3", str(SCRIPT), temp_dir],
                capture_output=True,
                text=True,
            )

            self.assertNotEqual(completed.returncode, 0)
            self.assertIn("Missing canonical changelog", completed.stderr)


if __name__ == "__main__":
    unittest.main()
