#!/usr/bin/env python3
"""Inventory every line and version block in the seven native product changelogs.

This tool establishes corpus coverage only. Keyword categories route human review;
they never assert that a changelog lesson is represented by a checklist gate.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path


PRODUCTS = {
    "Janggo": "janggonative",
    "Manta": "mantanative",
    "Scepter": "scepternative",
    "Shard": "splitter",
    "Vanguard": "vanguardnative",
    "Yasha": "yashanative",
    "Dagon": "dagon",
}

VERSION_HEADER = re.compile(r"^## (?:\[)?v?\d", re.IGNORECASE)
CATEGORY_PATTERNS = {
    "focus": re.compile(
        r"focus|keyboard|key press|keypress|texteditor|text field|modal|popup|menu|dropdown|combobox|ime|hwnd",
        re.IGNORECASE,
    ),
    "zoom": re.compile(
        r"zoom|scale|resiz|bounds|dpi|retina|hidpi|aspect|window size|display",
        re.IGNORECASE,
    ),
    "ui-performance-lifecycle": re.compile(
        r"freeze|deadlock|hang|chok|stutter|repaint|timer|thread|worker|async|shutdown|teardown|close crash|"
        r"use.after.free|safe.?pointer|weak.?reference|lock|cpu|allocat|cache|backpressure|message thread|"
        r"multi.instance|multi.editor",
        re.IGNORECASE,
    ),
    "audio-realtime": re.compile(
        r"real.?time|audio thread|processblock|block size|sample rate|nan|inf|finite|denormal|allocation|"
        r"click|pop|fade|smoothing|transport|playhead|offline bounce",
        re.IGNORECASE,
    ),
    "bus-sidechain-midi": re.compile(
        r"side.?chain|bus|channel|mono|stereo|midi|aux|surround",
        re.IGNORECASE,
    ),
    "latency-bypass": re.compile(
        r"latency|bypass|pdc|lookahead|delay compensation|tail",
        re.IGNORECASE,
    ),
    "state-parameters-automation": re.compile(
        r"state|parameter|apvts|automation|gesture|undo|session|restore|serialize|migration|version hint|"
        r"paramid|parameter id",
        re.IGNORECASE,
    ),
    "presets-filesystem": re.compile(
        r"preset|file chooser|filesystem|path traversal|directory|json|save|load|reference file",
        re.IGNORECASE,
    ),
    "rendering-ui-truth": re.compile(
        r"render|paint|draw|image|gradient|glass|frost|waveform|meter|spectrum|visual|pixel|tooltip|"
        r"hit.?test|geometry|canvas|colour|color|alpha|font|label",
        re.IGNORECASE,
    ),
    "licensing-trial": re.compile(
        r"licen|trial|activat|serial|purchase|rsa|signature|entitlement|key field|expiry|expired",
        re.IGNORECASE,
    ),
    "build-install-validation": re.compile(
        r"build|cmake|install|sign|notari|package|installer|pluginval|validator|auval|vst3|standalone|"
        r"release|beta|windows|macos|logic|ableton|reaper|studio one|fl studio|cubase|bitwig|host",
        re.IGNORECASE,
    ),
    "identity-hygiene": re.compile(
        r"version bump|identity|bundle|plugin code|product name|cleanup|remove|legacy|changelog|"
        r"documentation|readme|todo|debug",
        re.IGNORECASE,
    ),
    "security-untrusted-input": re.compile(
        r"secur|sanitize|escape|canonical|tamper|atomic write|transaction|symlink|path traversal|"
        r"malformed|oversized|overflow",
        re.IGNORECASE,
    ),
}


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def classify(block: str) -> list[str]:
    return [name for name, pattern in CATEGORY_PATTERNS.items() if pattern.search(block)]


def physical_lines(text: str) -> list[str]:
    """Split only on LF, preserving every other control character as content."""
    parts = text.split("\n")
    if parts and parts[-1] == "":
        parts.pop()
        return [part + "\n" for part in parts]
    if not parts:
        return []
    return [part + "\n" for part in parts[:-1]] + [parts[-1]]


def audit_changelog(product: str, repo: str, changelog: Path) -> dict[str, object]:
    raw = changelog.read_bytes()
    contained_nul_bytes = b"\0" in raw
    normalized = raw.replace(b"\0", b"").decode("utf-8", errors="replace")
    lines = physical_lines(normalized)
    header_indexes = [index for index, line in enumerate(lines) if VERSION_HEADER.match(line)]
    if not header_indexes:
        raise ValueError(f"No version headings found in {changelog}")

    entries = []
    for entry_index, start_index in enumerate(header_indexes):
        end_index = header_indexes[entry_index + 1] if entry_index + 1 < len(header_indexes) else len(lines)
        block = "".join(lines[start_index:end_index])
        entries.append(
            {
                "title": lines[start_index].removeprefix("## ").strip(),
                "start_line": start_index + 1,
                "end_line": end_index,
                "line_count": end_index - start_index,
                "sha256": sha256(block.encode("utf-8")),
                "categories": classify(block),
                "semantic_status": "requires_human_review",
            }
        )

    preamble_end = header_indexes[0]
    accounted_line_count = preamble_end + sum(int(entry["line_count"]) for entry in entries)
    return {
        "product": product,
        "repository": repo,
        "changelog": str(changelog),
        "raw_sha256": sha256(raw),
        "contained_nul_bytes": contained_nul_bytes,
        "line_count": len(lines),
        "preamble": {
            "start_line": 1 if preamble_end else 0,
            "end_line": preamble_end,
            "line_count": preamble_end,
            "sha256": sha256("".join(lines[:preamble_end]).encode("utf-8")),
            "semantic_status": "requires_human_review",
        },
        "version_entry_count": len(entries),
        "accounted_line_count": accounted_line_count,
        "all_lines_accounted_for": accounted_line_count == len(lines),
        "entries": entries,
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Account for every line and version block in the seven canonical native plug-in changelogs."
    )
    parser.add_argument("workspace", type=Path, help="Workspace containing the seven canonical repositories")
    args = parser.parse_args()

    products = []
    try:
        for product, repo in PRODUCTS.items():
            changelog = args.workspace.expanduser().resolve() / repo / "CHANGELOG.md"
            if not changelog.is_file():
                raise FileNotFoundError(f"Missing canonical changelog: {changelog}")
            print(f"Auditing {product}: {changelog}", file=sys.stderr)
            products.append(audit_changelog(product, repo, changelog))
    except (FileNotFoundError, OSError, ValueError) as error:
        print(error, file=sys.stderr)
        return 2

    report = {
        "schema": "mt-native-changelog-corpus-v1",
        "warning": "Keyword categories route review only; every block still requires human semantic review.",
        "workspace": str(args.workspace.expanduser().resolve()),
        "product_count": len(products),
        "version_entry_count": sum(int(product["version_entry_count"]) for product in products),
        "all_lines_accounted_for": all(bool(product["all_lines_accounted_for"]) for product in products),
        "products": products,
    }
    json.dump(report, sys.stdout, indent=2, sort_keys=True)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
