#!/usr/bin/env python3
"""Inventory preset-hygiene evidence candidates in one or more repositories.

This is deliberately a lead generator. It never emits pass/fail conclusions.
Inspect active build wiring and the cited source before making a claim.
"""

from __future__ import annotations

import argparse
import json
import re
from collections import defaultdict
from pathlib import Path
from typing import Iterable


TEXT_SUFFIXES = {
    ".c",
    ".cc",
    ".cpp",
    ".cxx",
    ".h",
    ".hh",
    ".hpp",
    ".inl",
    ".ipp",
    ".mm",
    ".md",
    ".py",
    ".rs",
    ".swift",
    ".txt",
    ".xml",
}

EXCLUDED_DIRS = {
    ".git",
    ".claude",
    ".codex-artifacts",
    ".idea",
    ".superpowers",
    ".venv",
    ".vscode",
    "_deps",
    "artifacts",
    "build",
    "builds",
    "cmake-build-debug",
    "cmake-build-release",
    "conductor",
    "dist",
    "external",
    "externals",
    "node_modules",
    "out",
    "parity",
    "plugins",
    "third_party",
    "vendor",
    "venv",
}

IGNORED_EXTENSIONS = {
    ".aif",
    ".aiff",
    ".als",
    ".app",
    ".au",
    ".bin",
    ".cpp",
    ".css",
    ".dll",
    ".dylib",
    ".flac",
    ".h",
    ".hpp",
    ".html",
    ".jpg",
    ".jpeg",
    ".js",
    ".log",
    ".md",
    ".mm",
    ".pdf",
    ".png",
    ".py",
    ".sh",
    ".so",
    ".svg",
    ".txt",
    ".vst3",
    ".wav",
    ".xml",
}

STRING_LITERAL_RE = re.compile(r"""["']([^"']+)["']""")
TRAILING_EXTENSION_RE = re.compile(r"""(\.[A-Za-z][A-Za-z0-9_-]{1,20})$""")

SIGNALS: dict[str, tuple[str, ...]] = {
    "format_or_product_marker": (
        r"""setProperty\s*\(\s*["'](?:format|kind|product|productId|presetKind)["']""",
        r"""["']MercurialTones\.[^"']*Preset["']""",
        r"""["']com\.mercurialtones\.[^"']+\.preset["']""",
    ),
    "schema_or_version_field": (
        r"""schemaVersion""",
        r"""schema_version""",
        r"""project_schema""",
        r"""kCurrent\w*Schema""",
    ),
    "schema_enforcement_candidate": (
        r"""unsupported[^;\n]*schema""",
        r"""schema\w*\s*(?:!=|<|>)""",
        r"""schemaVersion\s*(?:!=|<|>)""",
        r"""minimumReadableSchema""",
        r"""min(?:imum)?\w*Schema""",
    ),
    "legacy_reader_candidate": (
        r"""legacy""",
        r"""migrat\w*""",
    ),
    "real_unit_candidate": (
        r"""convertFrom0to1""",
        r"""denormali[sz]""",
        r"""plain (?:value|unit)""",
        r"""real unit""",
    ),
    "complete_or_sparse_semantics": (
        r"""restoreMissing""",
        r"""missing[^;\n]*(?:default|preset|parameter)""",
        r"""complete[^;\n]*(?:schema|preset|snapshot)""",
        r"""declared-subset""",
        r"""presetKind""",
    ),
    "validate_before_apply_candidate": (
        r"""validate[^;\n]*(?:preset|payload|document|root)""",
        r"""before (?:apply|touch|mutat)""",
        r"""temporary model""",
        r"""applyParsed""",
        r"""decode\w*Preset""",
    ),
    "finite_or_range_validation": (
        r"""(?:std::)?isfinite\s*\(\s*(?:real|normalised|value|number|parameter)""",
        r"""out.of.range""",
    ),
    "size_depth_or_count_bound": (
        r"""max\w*(?:Preset|Payload|Json|Depth|Catalog|File|Document)(?:\w*Size|\w*Count|\w*Bytes|\w*Characters|\w*)""",
        r"""(?:preset|payload|file)\s+(?:bytes|size limit)""",
        r"""nesting[^;\n]*(?:limit|max|depth)""",
    ),
    "path_hygiene_candidate": (
        r"""UnsafePresetPath""",
        r"""saniti[sz]e\w*Preset""",
        r"""normalise\w*PresetPath""",
        r"""isAChildOf""",
        r"""canonical\w*Path""",
        r"""path traversal""",
    ),
    "symlink_or_regular_file_guard": (
        r"""symlink""",
        r"""reparse""",
        r"""O_NOFOLLOW""",
        r"""regular file""",
    ),
    "atomic_write_candidate": (
        r"""TemporaryFile""",
        r"""MoveFileEx""",
        r"""WRITE_THROUGH""",
        r"""\batomic(?:ally)?[- ](?:write|replace|rename)""",
        r"""(?:written|replaced|renamed)[- ]atomically""",
        r"""same-directory[^;\n]*temp""",
        r"""overwriteTargetFileWithTemporary""",
        r"""replaceFileIn""",
        r"""(?:std::filesystem::|::)rename\s*\(""",
    ),
    "direct_replace_candidate": (
        r"""replaceWithText""",
        r"""replaceWithData""",
    ),
    "async_catalog_candidate": (
        r"""generation token""",
        r"""stale publish""",
        r"""AsyncUpdater""",
        r"""ThreadPool""",
        r"""background thread""",
    ),
    "dirty_host_or_transition_candidate": (
        r"""suppress\w*Dirty""",
        r"""updateHostDisplay""",
        r"""presetTransition""",
        r"""beginPresetLoad""",
        r"""endPresetLoad""",
    ),
    "preset_test_candidate": (
        r"""preset[^;\n]*(?:round.?trip|corrupt|traversal|migration|schema|atomic)""",
        r"""(?:round.?trip|corrupt|traversal|migration|schema|atomic)[^;\n]*preset""",
    ),
}

COMPILED_SIGNALS = {
    name: tuple(re.compile(pattern, re.IGNORECASE) for pattern in patterns)
    for name, patterns in SIGNALS.items()
}

ARTIFACT_CONTEXT_TOKENS = ("preset", "kit", "project")


def iter_text_files(root: Path) -> Iterable[Path]:
    for path in sorted(root.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        try:
            relative_parts = path.relative_to(root).parts
        except ValueError:
            continue
        if any(part in EXCLUDED_DIRS or part.startswith("build-") for part in relative_parts):
            continue
        if "docs" in relative_parts and "plans" in relative_parts:
            continue
        yield path


def classify_source(relative: Path) -> str:
    lowered = {part.lower() for part in relative.parts}
    if (
        "tests" in lowered
        or "test" in lowered
        or "test" in relative.name.lower()
        or "check" in relative.name.lower()
    ):
        return "test"
    if "docs" in lowered or relative.suffix.lower() == ".md":
        return "documentation"
    if relative.name == "CMakeLists.txt" or relative.suffix.lower() in {".cmake"}:
        return "build"
    return "source"


def compact_line(line: str, limit: int = 220) -> str:
    compact = " ".join(line.strip().split())
    return compact if len(compact) <= limit else compact[: limit - 1] + "…"


def scan_root(root: Path, max_hits: int) -> dict:
    evidence: dict[str, list[dict]] = defaultdict(list)
    extensions: dict[str, list[dict]] = defaultdict(list)
    files_scanned = 0

    for path in iter_text_files(root):
        files_scanned += 1
        relative = path.relative_to(root)
        source_class = classify_source(relative)
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue

        text_lines = text.splitlines()
        path_has_artifact_context = any(
            token in relative.as_posix().lower() for token in ARTIFACT_CONTEXT_TOKENS
        )
        for line_index, line in enumerate(text_lines):
            line_number = line_index + 1
            lower_line = line.lower()
            nearby_start = max(0, line_index - 3)
            nearby_end = min(len(text_lines), line_index + 4)
            nearby = "\n".join(text_lines[nearby_start:nearby_end]).lower()
            artifact_context = path_has_artifact_context or any(
                token in nearby for token in ARTIFACT_CONTEXT_TOKENS
            )
            extension_line_context = any(
                token in lower_line
                for token in (*ARTIFACT_CONTEXT_TOKENS, "filechooser")
            ) or (
                path_has_artifact_context
                and any(
                    token in lower_line
                    for token in (
                        "extension",
                        "wildcard",
                        "findchildfiles",
                        "rangeddirectoryiterator",
                    )
                )
            )
            if extension_line_context:
                for literal_match in STRING_LITERAL_RE.finditer(line):
                    literal = literal_match.group(1)
                    extension_match = TRAILING_EXTENSION_RE.search(literal)
                    if extension_match is None:
                        continue
                    raw_extension = extension_match.group(1)
                    # Canonical extensions in this corpus are lowercase. This
                    # also prevents a format marker such as
                    # "MercurialTones.TetherPreset" from masquerading as a
                    # filename extension.
                    if raw_extension != raw_extension.lower():
                        continue
                    extension = raw_extension.lower()
                    if extension in IGNORED_EXTENSIONS:
                        continue
                    if len(extensions[extension]) >= max_hits:
                        continue
                    extensions[extension].append(
                        {
                            "path": relative.as_posix(),
                            "line": line_number,
                            "class": source_class,
                            "text": compact_line(line),
                        }
                    )

            for signal_name, patterns in COMPILED_SIGNALS.items():
                if not artifact_context:
                    continue
                if len(evidence[signal_name]) >= max_hits:
                    continue
                if any(pattern.search(line) for pattern in patterns):
                    evidence[signal_name].append(
                        {
                            "path": relative.as_posix(),
                            "line": line_number,
                            "class": source_class,
                            "text": compact_line(line),
                        }
                    )

    return {
        "root": str(root),
        "files_scanned": files_scanned,
        "extensions": {
            extension: {
                "candidate_count_shown": len(hits),
                "evidence": hits,
            }
            for extension, hits in sorted(extensions.items())
        },
        "signals": {
            name: {
                "candidate_count_shown": len(evidence.get(name, [])),
                "evidence": evidence.get(name, []),
            }
            for name in sorted(SIGNALS)
        },
        "warning": (
            "Heuristic candidates only. Confirm active build wiring and inspect "
            "the complete read/apply/write paths before assigning an evidence label."
        ),
    }


def render_text(report: dict) -> str:
    lines = [
        f"Preset evidence inventory: {report['root']}",
        f"Files scanned: {report['files_scanned']}",
        report["warning"],
        "",
        "Candidate extensions:",
    ]
    if not report["extensions"]:
        lines.append("  (none)")
    for extension, details in report["extensions"].items():
        lines.append(f"  {extension}: {details['candidate_count_shown']} shown")
        for hit in details["evidence"]:
            lines.append(
                f"    {hit['class']} {hit['path']}:{hit['line']}  {hit['text']}"
            )

    lines.append("")
    lines.append("Evidence signals:")
    for name, details in report["signals"].items():
        if not details["evidence"]:
            continue
        lines.append(f"  {name}: {details['candidate_count_shown']} shown")
        for hit in details["evidence"]:
            lines.append(
                f"    {hit['class']} {hit['path']}:{hit['line']}  {hit['text']}"
            )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Inventory preset-hygiene evidence candidates without assigning pass/fail."
    )
    parser.add_argument("roots", nargs="+", help="Repository root(s) to scan")
    parser.add_argument("--json", action="store_true", help="Emit JSON")
    parser.add_argument(
        "--max-hits",
        type=int,
        default=12,
        help="Maximum evidence rows shown per signal/extension (default: 12)",
    )
    args = parser.parse_args()

    if args.max_hits < 1:
        parser.error("--max-hits must be at least 1")

    reports = []
    for raw_root in args.roots:
        root = Path(raw_root).expanduser().resolve()
        if not root.is_dir():
            parser.error(f"not a directory: {raw_root}")
        reports.append(scan_root(root, args.max_hits))

    if args.json:
        print(json.dumps(reports, indent=2, sort_keys=True))
    else:
        print("\n\n".join(render_text(report) for report in reports))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
