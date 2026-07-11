# Seven-Product Native Changelog Audit

Date: 2026-07-11

## Why this audit exists

The first checklist draft scanned 13 repository changelogs and extracted many real lessons, but it did not prove a deliberate audit of the seven established native products. A broad source count and keyword scan were incorrectly presented as if they guaranteed semantic completeness. This document corrects the scope, records the exact corpus, distinguishes mechanical coverage from human judgment, and lists the gates added after the second pass.

## Canonical seven

The seven established native products represented by the Software Center and used as the primary inherited baseline are:

1. Manta (`mantanative`)
2. Yasha (`yashanative`)
3. Scepter (`scepternative`)
4. Vanguard (`vanguardnative`)
5. Dagon (`dagon`)
6. Shard (`splitter`)
7. Janggo (`janggonative`)

Scope evidence: `mercurial-tones-software-center/manifest/release-manifest.json` contains exactly these seven product IDs at lines 6, 43, 80, 116, 153, 190, and 227.

Tether is the new consumer of the baseline. Its newly observed failures are valid additions to the checklist, but Tether is not substituted for one of the seven historical products.

## Corpus identity and line accounting

Run:

```bash
python3 scripts/audit-native-changelog-corpus.py /Users/yalcinefe/mt-dev > native-changelog-corpus.json
```

The tool hashes the untouched raw files, removes embedded NUL bytes only for text parsing, splits physical lines only on LF, enumerates every version block, records exact line ranges and per-block hashes, and verifies that preamble plus blocks accounts for the entire file. Keyword categories route review; every emitted entry deliberately remains `requires_human_review`.

| Product | Lines | Version blocks | Unrouted blocks | Raw SHA-256 |
|---|---:|---:|---:|---|
| Janggo | 775 | 28 | 0 | `5891f9cca124ff7b2643394f034857135a881019b63cc3fba5a8a218deab3ced` |
| Manta | 14,456 | 430 | 0 | `8699fcab4498a2740291411fa28617f74c63945c02c17a9215ceb4b66ee9f494` |
| Scepter | 16,862 | 866 | 3 | `becb85070b05040ed067e2cee45402936aee37e1af827152fe9d471cb3054668` |
| Shard | 1,489 | 59 | 1 | `22344f10dd1d193c3ea02cd435a7f379c0578c67feafb5369b53700d986fa45e` |
| Vanguard | 7,163 | 214 | 2 | `cb584889460b37e64ed1f78c31ba55113a0f69c43caf628681154d8e42c349c7` |
| Yasha | 5,600 | 116 | 0 | `bd5d16d20dc9adac473b10dcdaaddd94f33c1f9a914104269472a5c63f0f6348` |
| Dagon | 3,927 | 129 | 0 | `ca5a332ce49d6206a5a3ecf1bae01281277812b2b01a832b2ed21eea51e19eb5` |
| **Total** | **50,272** | **1,842** | **6** | — |

All 50,272 physical lines are accounted for. The six keyword-unrouted blocks were inspected explicitly:

- Scepter `v1.8.79`, `v1.8.71-v1.8.78`, and `v1.8.65-v1.8.70`: three-line range/continuity entries with no additional resilience lesson in their bodies.
- Shard `v0.1.0` initial WebView implementation: explicitly superseded by the native rewrite; transferable WebView lessons are covered by Scepter/Yasha and the later Shard lifecycle history.
- Vanguard `v0.15.60`: product-specific 5 kHz crossover/DSP calibration.
- Vanguard `v0.15.39`: product-specific knob-face asset replacement.

These are explicit exclusions, not silently dropped entries.

## Semantic review method

The second pass used four layers:

1. **Exact line/block ledger** — proves no file range disappeared during extraction.
2. **Full version-body routing** — every block is searched as a whole across focus, zoom, UI lifecycle/performance, realtime audio, bus/sidechain, latency/bypass, state/automation, presets/filesystem, rendering, licensing, build/install/validation, identity/hygiene, and untrusted-input categories.
3. **Existing complete fix extractions** — the previously produced sibling audits consolidate iterative sagas and distinguish shared framework failures from product-only DSP/UI changes:
   - `dagon/docs/sibling-fix-audit/scepternative-all-fixes.md`: 221 consolidated Scepter fixes, 149 shared and 72 product-specific.
   - `dagon/docs/sibling-fix-audit/vanguardnative-all-fixes.md`: 99 consolidated Vanguard fixes, 42 shared and 57 product-specific.
   - `dagon/SIBLING-PLUGIN-FIX-AUDIT.md`: 117 distinct shared concerns cross-checked against Dagon.
   - `splitter/REFERENCE-FIXES-AUDIT.md`: Vanguard, Scepter, and Manta fixes cross-checked against Shard, including explicit gaps.
4. **Direct product review** — complete short histories for Janggo and Shard; Yasha's release/audit/hardening entries; Dagon's host-freeze, performance, packaging, state, and release entries; Manta's close-crash, focus, zoom, renderer, state, and native-cutover sagas; current source/tests/release scripts for mechanism checks.

Product-specific sound tuning is not blindly promoted into a universal resilience gate. It is included only when it exposes a transferable engineering failure such as wrong internal sample rate, discontinuous nonlinear state, unbounded memory, invalid block assumptions, stale mode state, or a misleading visualization.

## Omissions found in the first draft

The completion re-audit added or made explicit the following proof requirements:

| New gate | Missing lesson made explicit | Principal source |
|---|---|---|
| `EVID-09` | Exact changelog line/block accounting and semantic mapping | Completion re-audit |
| `HYGIENE-11` | Test/capture environment variables must not leak into normal sessions | Scepter 1.1.27–1.1.28 |
| `BUILD-11` | Windows header/API portability and `NOMINMAX` | Yasha 0.4.22–0.4.23 |
| `BUILD-12` | Assert actual universal slices after build | Vanguard 0.15.129, Dagon audit |
| `RT-13` | Bound multi-hour histories/statistics/queues | Scepter 0.1.268 |
| `RT-14` | Oversized offline bounce must not truncate or allocate unsafely | Scepter 0.1.255–0.1.267 |
| `RT-15`, `VALID-13` | Budget host state save/restore and multi-instance close latency | Scepter 0.1.346/1.0.7 |
| `RT-16` | Guard integer narrowing, byte/sample multiplication, and malformed metadata | Scepter 0.1.243/0.1.264/0.1.271/0.1.275 |
| `RT-17` | Coefficients/smoothers use actual native/oversampled rate | Vanguard 0.9.3/0.9.11 |
| `RT-18` | Reset/recompute nonlinear and recursive state on coefficient/topology changes | Vanguard, Yasha |
| `RT-19` | Sanitize at signal boundaries without poisoning hot UI/audio loops | Manta/Scepter |
| `BUS-10` | Sidechain availability and user toggle self-heal after delayed UI readiness | Scepter SC saga |
| `STATE-14` | Validator-safe boolean/discrete restoration | Scepter 1.1.14, Vanguard 0.15.129 |
| `STATE-15` | Bound and defer large serialized blobs | Scepter reference-state fixes |
| `STATE-16` | Neutralize retired hidden legacy controls | Vanguard migrations |
| `PRESET-09`, `SEC-02` | Encode JSON/JS bridge values rather than concatenate strings | Scepter 0.1.246/1.8.105 |
| `PRESET-10` | Upgrade stale factory presets without overwriting users | Scepter preset repair series |
| `SEC-01` | WebView CSP and resource/navigation allowlist | WebView product audits |
| `SEC-03` | Cap external files before decode and validate decoded size | Scepter 0.1.264/0.1.271 |
| `SEC-04` | Symlink/canonical-path containment | Preset/export/license filesystem audits |
| `SEC-05`–`SEC-08` | URL allowlisting, secret hygiene, bounded parsers, redacted errors | Licensing/update audits |
| `LIFE-13` | Detect HWND/native-peer reparent and recreate/attach safely | Scepter 0.1.206/1.1.11, Yasha 0.4.17/0.4.20 |
| `LIFE-14` | Essential host-visible refresh cannot trust JUCE visibility or peer heuristics | Tether 0.5.0–0.5.2 Ableton regression |
| `PERF-13` | Dropped async completion must not permanently wedge pending counters | Scepter 0.1.260, Yasha 0.9.23 |
| `PERF-14` | Hidden/reopened editors cannot burst-drain stale visual backlog | Scepter 0.1.33/0.1.44 |
| `ZOOM-15` | Compose OS text scale, host scale, DPR, and user zoom exactly once | Scepter 0.1.79/1.1.1/1.1.3 |
| `RENDER-14` | Transparent cached images need explicit clear semantics | Manta ghosting fixes |
| `RENDER-15` | JUCE image overloads can change panel luminance by renderer | Vanguard 0.15.140–0.15.146 |
| `RENDER-16` | Pointer coordinates must match painted scale under host scaling | Scepter 0.1.65/0.1.79 |
| `LIC-15` | Normal DAW launch must not trigger OS credential prompts | Scepter 0.1.406 |
| `HOSTER-09` | Sanitize hostile third-party plug-in output and metadata | Shard audit gap G3 |
| `INSTALL-13` | Release shell scripts must quote paths, avoid reserved names, and fail closed | Scepter validator history |
| `INSTALL-14` | Post-install host validation must use a process launched after bundle replacement | Tether 0.5.2 Ableton reinstallation |

The first draft contained 197 gates. The corrected catalog contains 235 unique gates.

## Core seven product findings retained

### Janggo

- Host notifications such as latency changes must occur outside non-reentrant prepare/drain barriers.
- Global window preference and per-project editor size require provenance and precedence, a 0x0 guard, debounced writes, and destructor flush.
- Dialogs and popup callbacks must use safe ownership and release host focus on teardown.
- Multi-editor pressure mode must shed decoration while preserving automation and meaningful signal geometry.
- A move-to-only JUCE path can still report empty; waveform connectivity needs explicit state and a pixel guard.
- Sidechain processing must inspect the actual bus buffer, and validators require a real program name.

### Manta

- Begin shutdown before child destruction; stop timers/workers, dismiss transient UI, detach LookAndFeel/callbacks, and release shared font caches.
- Every queued callback needs safe ownership; menu-row callbacks must copy what they need before an action can destroy the menu.
- Focus requests made at 0x0 fail silently; intentional modal focus must wait for real bounds/peer. Passive canvas actions must never grab host focus.
- Native zoom must relayout/reraster actual geometry, not stretch the component; persistence and host-fit behavior require separate proof.
- Zero/mono transitional buffers and mono dry/wet paths require explicit handling.
- Cached transparent layers need explicit clearing, and renderer-agnostic vector coverage is required beneath image effects.
- Native-only and licensing UI must be enforced together; a processor gate without an activation UI is not a release.

### Scepter

- WebView2 focus requires top-level HWND handoff with form-control exclusions; reparenting and delayed real-peer creation need explicit handling.
- Message/analysis work needs backpressure, dropped-callback recovery, bounded reopen backlog, and ordered thread shutdown.
- GUI/analyzer buffers need lock-free or bounded access across prepare/release and editor lifetime.
- External files, decoded sample counts, float formatting, progress math, session histories, and state blobs all need size/overflow bounds.
- Sidechain behavior must use the real bus buffer and self-heal UI availability after reload/readiness races.
- Retina logical pixels, Windows text scaling, host-fit scaling, and non-100% pointer coordinates are distinct compatibility gates.
- Preset/bridge strings require real serialization, factory presets require revisioned replacement, and state caches must reset coherently.
- AU cache settling, installed-version verification, WebView2 data folders/static linking, signing, and installer component/domain behavior are release gates.

### Shard

- Hosted plug-in creation/installation/removal is split-phase; the audio thread never waits on structure locks or destroys third-party objects.
- Message-thread access uses bounded try-lock/snapshot behavior to avoid callback-lock deadlocks and buzz.
- Scanner, activation, detached windows, shared caches, and hosted processors have explicit owner/join/close order.
- Bypass delay remains primed and latency-compensated across normal, bypassed, and license-muted transitions.
- Offline signed licensing uses canonical fixtures and transactional adoption; activation survives editor closure.
- Preset names remain inside the root, corrupt loads are non-destructive, and notifications are batched.
- Detached hosted windows do not grab keyboard focus; search focus is click-only.
- Third-party output/non-finite containment, transient zero/mono buffers, default program naming, and full packaging/notarization are inherited proof gates even when previously recorded as Shard gaps.

### Vanguard

- Eliminate duplicate refresh loops, disk scans, and full repaints; use revisions, dirty gates, bounded open-sync fallback, and hidden-editor idling.
- Programmatic panel resize must preserve user scale; final scale persists on close, not on every resize event.
- Native-child/popups/async callbacks require safe teardown, per-editor state, and focus deferral until a real peer/bounds exist.
- Zero/mono transitional buffers and non-finite stage boundaries must be safe.
- Preset fast paths require complete schemas; legacy/sparse paths reset/migrate, synchronize live atomics, batch notifications, and cache inventories.
- Latency/bypass transitions stay aligned and host notifications stay off realtime paths.
- Internal oversampling rates, nonlinear history, coefficient smoothing, and mode-switch state are part of correctness resilience.
- Built architecture, installed identity/version, official validator version, stale VST3 metadata, and host-open Windows installation are explicit release checks.

### Yasha

- WebView creation waits for a real peer and uses per-process WebView2 state; HWND reparenting is recoverable.
- AU parameter version hints are monotonic, and mode initialization/state restore remains coherent outside the UI.
- Transport-stop debounce is time-based so host focus/stop glitches do not create pops or kill intended tails.
- BBD/nonlinear state is bounded and applied from the smoothed controls actually consumed by DSP.
- Power/mode switches reset or preserve wet memory according to the product contract.
- Windows API/header portability, identity/export, installer workflows, standalone bounds, native text/help, and Lite/full coexistence are regression gates.
- Offline activation is transactional and the trial badge remains anchored/reachable through panel changes.

### Dagon

- Drag repaint/frost work is cadence-capped and dirty-driven; Low CPU and multi-editor pressure have measured render budgets.
- Audio-thread parameters are cached; no strings/allocations/fast-math drift occur in the processing path.
- `releaseResources` does not mean the editor closed; visualization gates survive suspend/reprepare.
- Real renderer coverage uses unconditional opaque/vector bases beneath glass/texture layers.
- Presets apply to live atomics, save paths are truthful, and product/manual/default identity remains synchronized.
- External sidechain, mono layout, finite output, universal architecture, licensing flavor policy, and installed validation are explicitly proved.
- Performance optimization requires bit-exact audio and full null/pixel/lifecycle/stress gates.

## Supplemental sources

The following histories supplied additional gates but are not counted as substitutes for the seven:

- **Aegis:** explicit product-shortcut focus exception, shared paint/hit geometry, truthful signal visualization, installed-host version confusion.
- **Golem:** short-history products still need full identity/build/state/install evidence.
- **MT Host:** standalone hosting/scanner/cache and child containment.
- **Legacy Vanguard tree:** historical context cross-checked against canonical VanguardNative.
- **Wavetable Editor:** usable-display initial bounds, aspect constraints, and editor zoom limits.
- **Tether:** new regressions added after the seven-product baseline—dropdown styling scope, selected-mode tooltips, actual wet/dry history, misleading gradients, first-run opacity/overlay visibility, zoom parity, essential refresh that survives unreliable JUCE host visibility/peer state, and a hard pre-install host barrier with fresh-process post-install proof.

## Audit limitation and maintenance rule

The JSON ledger proves textual coverage, not correctness of interpretation. When any of the seven changelogs changes, its raw hash will change and this audit must be rerun. Every new escaped compatibility/resilience defect must add or strengthen a checklist gate and a reproducing test. A future claim of “complete” must cite the exact ledger artifact and the semantic mapping delta; it may not rely on elapsed time, file counts, or keyword totals alone.
