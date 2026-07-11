---
name: checklist
description: Audits native audio plug-ins against Mercurial Tones' accumulated compatibility, real-time safety, host-focus, UI-lifecycle, zoom, state, licensing, installation, and release-hygiene regressions. Use when creating a plug-in, preparing a Beta or Release build, diagnosing recurring cross-product bugs, reviewing a native JUCE plug-in, or when the user says "$checklist", "plugin checklist", "compatibility check", "resilience check", or "release proof".
---

# Native Plugin Proof Checklist

## Purpose

Turn the failure history of every Mercurial Tones native plug-in into a release gate. This is not a list of suggestions: every applicable requirement needs reproducible evidence before the plug-in may be called compatible, resilient, or release-ready.

The complete requirement catalog is in [CHECKLIST.md](CHECKLIST.md). Read that file completely before beginning an audit. Do not audit from memory or from this summary.

## Scope

Use this skill for native audio plug-ins and native plug-in hosts, including JUCE VST3, AU, and Standalone products. It covers:

- new-product architecture and implementation reviews;
- pre-release and post-fix regression audits;
- host focus, modal, dropdown, and keyboard behavior;
- real-time audio, bus, block-size, latency, bypass, and state safety;
- editor lifetime, multi-instance UI load, rendering, zoom, and DPI behavior;
- trial, licensing, preset, installer, signing, validation, and repository hygiene.

Do not use it as proof that a DSP design sounds good. Listening approval and product-specific DSP acceptance remain separate gates.

## Evidence Contract

For every checklist item, record exactly one status:

- `PASS` — the named behavior was exercised and the artifact proves the expected result.
- `FAIL` — the behavior was exercised and violated the requirement.
- `BLOCKED` — the required environment or authority is unavailable; this blocks release.
- `N/A` — the product structurally cannot exercise the requirement, with source or build evidence explaining why.

`UNKNOWN`, “looks fine,” source inspection alone, and an unannotated skip are not passing states. A static pattern proves only that code exists. It does not prove host focus, thread safety, GPU rendering, session restoration, or installed-binary behavior.

Each evidence record must include:

1. checklist ID;
2. product, exact commit, version, and build flavor;
3. OS, architecture, format, host and host version when applicable;
4. exact command or manual procedure;
5. output, log, screenshot, recording, hash, or installed-artifact path;
6. timestamp and result;
7. issue/commit link for failures and fixes.

## Workflow

### 1. Freeze the audit identity

Record the repository path, commit, dirty state, declared version, plug-in formats, product profile, supported OS/architecture/hosts, and Release/Beta distinction. Do not mix evidence from different commits or binaries.

Classify the product features that affect applicability:

- effect, instrument, analyzer, or host;
- native component UI or WebView;
- sidechain, MIDI, latency, oversampling, lookahead, bypass, dry/wet;
- preset files, factory presets, license/trial, networking;
- hosted third-party plug-ins or detached child windows.

### 2. Run the static evidence collector

From the target repository:

```bash
bash /mnt/skills/user/checklist/scripts/audit-native-plugin.sh . > checklist-static.json
```

When running from a source checkout of this skill, substitute the actual script path. The script inventories evidence and flags missing mechanisms. Its `observed` result is not a runtime `PASS`.

### 3. Build the applicability matrix

Read [CHECKLIST.md](CHECKLIST.md) completely. Copy every requirement into the audit record. Mark applicability before testing. For `N/A`, cite the structural fact that makes the behavior impossible; for example, “no sidechain bus is declared in CMake or processor layout.”

Never mark a whole section `N/A` merely because the current implementation does not contain the feature expected by that section. Missing required behavior is a failure.

### 4. Prove the fast gates

Run repository tests, static hygiene, format validators, UI snapshot/rendering checks, state tests, block-size/sample-rate tests, and Release/Beta builds. Stop on the first red prerequisite. Fixes follow the `test-driven-development` and `debugging-and-error-recovery` skills when the user authorized changes.

### 5. Prove installed runtime behavior

Install the exact signed candidate and test the installed artifact, not only the build tree. Close hosts before replacement, restart/rescan after installation, and verify that the loaded module version and hash match the candidate.

Exercise all applicable host, lifecycle, focus, zoom, multi-instance, first-run licensing, renderer, channel-layout, state, and latency gates in the full matrix. Standalone is useful but is not a substitute for DAW testing.

### 6. Reproduce known red conditions

The checklist contains regression scenarios learned from shipped failures. Execute the actual trigger: second editor, rapid close, 0x0 construction, oversized block, silent sidechain, release/prepare while an editor remains open, a host modal, a smallest-display zoom, or the relevant equivalent. A happy-path smoke test is insufficient.

### 7. Issue the verdict

Report:

1. `RELEASE READY` or `NOT RELEASE READY`;
2. all `FAIL` and `BLOCKED` items first;
3. coverage totals by section;
4. exact untested matrix cells;
5. evidence paths and candidate identity;
6. permitted follow-up work without silently changing product behavior.

Any applicable `FAIL`, `BLOCKED`, missing evidence, unsigned artifact, version mismatch, dirty release tree, or untested first-run path makes the verdict `NOT RELEASE READY`.

## Mandatory Rules

- Test both Release and Beta whenever their compile-time behavior differs.
- Test the first-run/trial path in Release; Beta bypasses are not proof.
- Test at least two simultaneous editors and rapid create/destroy loops.
- Test the actual supported DAWs on each supported OS.
- Test installed artifacts after signing and packaging.
- Test state from fresh, current, legacy, corrupt, and quick-close cases.
- Test every advertised zoom at display limits and across session reopen.
- Test host keyboard shortcuts immediately after every text field, dropdown, modal, and WebView interaction.
- Test exact current block lengths, changing block sizes, zero/mono transitional buffers, and oversized blocks.
- Preserve stable parameter IDs and AU version hints; never “repair” compatibility by renaming existing IDs.
- Do not loosen a regression bound merely to obtain a green result. Document any justified contract change in the test.
- Do not substitute an estimator for a promised real input/output visualization.

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| “The code uses `SafePointer`, so teardown is safe.” | Other raw callbacks, workers, timers, menus, or hosted windows may still outlive the editor. Run the lifecycle trigger. |
| “Standalone works.” | DAWs add callback locks, wrapper focus, bus negotiation, state timing, and renderer differences. |
| “The software snapshot is correct.” | CoreGraphics, Metal, WebView2, Retina, and clipped image blits have failed while snapshots passed. |
| “One instance is smooth.” | Second-instance reentrancy and multiple editor repaint pressure caused prior freezes. |
| “Zoom is saved in state.” | Global new-instance preference and per-project restoration have different ownership and precedence. |
| “The host reports the sidechain enabled.” | The actual bus buffer may still have zero channels or a different layout. |
| “The prepared block size is the block size.” | Hosts may deliver smaller, larger, or changing blocks. |
| “Beta opens, so licensing works.” | Beta commonly bypasses the exact first-run and expiration paths that fail in Release. |
| “The validator failure is probably a validator bug.” | Prove the tool version and isolate the artifact; do not assume either the product or validator is wrong. |
| “The installer succeeded.” | An open DAW can retain the old in-memory module, and stale bundle files can survive a partial copy. |

## Verification

Before presenting a passing verdict, confirm:

- [ ] The complete checklist was read and every ID has a status.
- [ ] Candidate commit, version, flavor, hashes, and installed paths are recorded.
- [ ] No `FAIL`, `BLOCKED`, `UNKNOWN`, or unexplained `N/A` remains.
- [ ] Repository tests and all declared product-specific gates are green.
- [ ] Release and Beta were built and their differing paths were tested.
- [ ] Supported formats, OSes, architectures, hosts, sample rates, block sizes, and channel layouts have evidence.
- [ ] Focus, lifecycle, multi-editor, zoom-memory, renderer, state, first-run license, and install regressions have runtime proof.
- [ ] VST3/AU metadata and visible UI versions match the source version.
- [ ] Built and installed artifacts are signed, hashed, and identical where expected.
- [ ] `git diff --check` passes and the release tree contains no unintended changes or diagnostics.

## Output Format

```markdown
# Native Plugin Proof Report — <product> <version>

Verdict: NOT RELEASE READY
Candidate: <commit>, <flavor>, <artifact hashes>
Coverage: <pass>/<applicable>; <fail> failed; <blocked> blocked; <n/a> justified

## Release blockers
- FOCUS-04 — FAIL — Ableton Live 12.2 / Windows 11: Space remains captured after dropdown selection. Evidence: ...

## Untested matrix
- Logic Pro / AU / macOS Intel — BLOCKED — Intel runner unavailable.

## Section results
- Build and identity: 18/18 PASS
- Host focus: 11/12 PASS, 1 FAIL

## Evidence index
- <path or command> — <what it proves>
```

## Troubleshooting

- If the script reports no CMake file, pass the actual plug-in root rather than a monorepo parent.
- If a host keeps loading an old version, close the host, remove stale bundles, reinstall, rescan, restart the platform component registrar when applicable, and verify the loaded module path/hash.
- If a test cannot run on the present machine, record `BLOCKED`; do not convert it to `PASS` or `N/A`.
- If the product has a stricter local release flow, run both this checklist and the product flow. The stricter requirement wins.
