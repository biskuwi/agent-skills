# Native Product Preset Evidence Map

## Snapshot identity

Snapshot: 2026-07-30. Findings describe the active working trees at the listed
commits. Some repositories were dirty in unrelated files or generated output;
the preset evidence paths cited below were clean at inspection time.

| Product | Version | Branch | Commit | Dirty entries |
|---|---:|---|---|---:|
| Aegis | 0.2.12 | `store/aegis-product-page` | `17d85e12647b` | 1 |
| Radiant | 0.5.0 | `feature/filter-22k-response` | `5ffdad762782` | 1 |
| Daedalus | 1.0.61 | `feature/codex-m0-m6` | `f9e69d0c135b` | 12 |
| Dagon | 1.0.34 | `feat/dagon-lowcpu-dsp-perf` | `ad78e64ce3e7` | 44 |
| Golem | 0.1.0 | `main` | `66fbb61c21d1` | 0 |
| Janggo | 1.13.4 | `main` | `8f3264f401f5` | 1 |
| Manta | 1.1.12 | `release/manta-1.1.5` | `4f58ceb17d46` | 9 |
| Scepter | 1.7.35 | `main` | `d69052260569` | 4 |
| Dire | 0.2.3 | `main` | `4a47df977be3` | 3 |
| Shard | 1.0.2 | `shard-ui-band-header-frost` | `8ae7762a0e7c` | 3 |
| Tether | 1.2.0 | `feat/skia-ui` | `e704d1b7881b` | 1 |
| Vanguard | 0.15.173 | `main` | `9d48ddb6ee0c` | 1 |
| Wavetable Editor | 0.1.0 | `main` | `7826def5a210` | 0 |

Use this map as seeded evidence, not as a permanent claim. Re-freeze identity
before applying a precedent.

Evidence level: findings below are `active-static` unless an actual run is
recorded. Tether's current `TetherProcessorTest` was run and passed during the
forward test, but its preset test seams were disabled; that run promotes only
the exercised assertions, not the unexercised host, filesystem, audio, or stale
scan behavior. Other mentioned test coverage means source inspection only.

## Product findings

### Aegis

- Active source: `Aegis/plugins/Aegis/Source/PresetManager.{h,cpp}`. The
  top-level `Aegis/Source/PresetManager` is not the active CMake source.
- Canonical extension: `.aegis`; legacy `.json` remains readable.
- Strong: exact format/plugin/kind markers, schema 9 with minimum readable
  schema 3, explicit multi-version migrations, native-before-legacy discovery,
  path normalization, an explicit flagged factory-override mechanism,
  temporary-file writes, and validation of temporary and final payloads.
- Gap: saving a selected factory preset can persist a user override under the
  factory path, so factory immutability is not strict.
- Reuse for: long-lived schema adapters and verified native conversion.

### Radiant (`component-synth`)

- Active source: `Source/plugin/ui/Presets.{h,cpp}` and
  `docs/spec/ui/preset-bar.md`.
- Canonical extension: `.cspreset`; XML-encoded ValueTree.
- Strong: captures the same state model used by session restore, strips serial,
  editor size, factory program, and other instance-only fields, validates root
  type/size/element count, rejects symlinks, and uses a validated temporary
  replacement.
- Gap: scanning/loading is deliberately message-thread synchronous in v1;
  compatibility policy deserves stricter future-schema review.
- Reuse for: separating sound state from instance state.

### Daedalus

- Active source: `Source/daedalus/state/PresetCodec.{h,cpp}` and
  `PresetLibrary.{h,cpp}`; tests in `tests/state/`.
- Canonical extension: `.daedpreset`.
- Strong: versioned real-unit JSON, bounded parser and recursion, 1 MiB payload
  limit, 4096 catalog limit, canonical serialization, complete decode before
  apply, stable IDs/provenance, decoded immutable catalog snapshots, root
  containment, symlink/reparse refusal, `O_NOFOLLOW`, regular-file checks,
  restrictive temp permissions, and atomic platform replacement.
- Reuse for: hostile filesystems, size/count limits, and immutable catalogs.

### Dagon

- Active source: `Source/native/controllers/MantaNativePresetController.cpp`
  plus `Source/PluginProcessor.cpp`. `Source/PresetManager.cpp` is not compiled
  by the active top-level CMake target.
- Canonical user extension: `.dgx`; legacy/factory `.json` remains visible.
- Strong: branded extension, native precedence, product-scoped parameter
  allowlist, complete-save inventory tests, path segment normalization, and
  exclusion of retired Manta/Volume state.
- Gaps: the outer payload is still loose schema-1 Manta JSON, has no enforced
  Dagon marker, writes with `replaceWithText`, and applies through a parser that
  does not fully validate before mutation.
- Reuse for: product-scoping inherited state; do not copy its write boundary.

### Golem

- Active source: `Source/PluginProcessor.cpp` and `Source/PluginEditor.cpp`.
- Canonical kit extension: `.golemkit`; binary JUCE state/XML.
- Strong: product-specific artifact and full kit capture.
- Gaps: no explicit kit schema/product-envelope enforcement, imported files are
  applied through session restore without complete prevalidation, sample
  identity is an absolute source path, byte/count limits are absent, and the
  painted preset selector is not a real managed preset library.
- Reuse for: extension precedent only; harden before treating kits as portable.

### Janggo

- Active source: `Source/state/PresetManager.{h,cpp}`.
- Canonical files currently use generic `.json`; new saves emit unified schema
  5 with `kind: janggoPreset`.
- Strong: unified Free/Pro model, stable IDs and categories, plain values,
  complete module chain, schemas 1–4 and legacy chain adapters, choice-list
  migrations, default restoration, locked-trigger subset semantics, and
  compiled factory/user identity.
- Gaps: `.json` remains canonical, the `kind` marker is written but not enforced
  on the unified read path, saves use `replaceWithText`, and user scans lack
  hostile-file bounds/containment.
- Reuse for: product-family unification and explicit locked-subset behavior.

### Manta

- Compiled sources include `Source/PluginEditor.cpp`,
  `Source/native/controllers/MantaNativePresetController.cpp`, and
  `Source/PluginProcessor.cpp`; the native-only release surface routes preset
  actions through the controller. `Source/PresetManager.cpp` is not compiled by
  the active top-level target.
- Canonical files currently use generic `.json`.
- Strong: sanitized hierarchical paths, standard/fallback directories, legacy
  storage migration, complete saves, missing-field default restoration,
  real-unit application, dirty suppression, single host refresh, undo
  baseline, and fade-out/commit/fade-in transition for live audio.
- Gaps: generic extension, no exact product/format marker, schema written but
  not enforced, no outer byte/depth bound, direct `replaceWithText`, and a
  dynamic-object payload can succeed without a valid `params` object.
- Reuse for: runtime apply behavior, not file-format identity.

### Scepter

- Active global-preset path: `Source/native/ScepterNativeEditor.cpp` plus
  `Source/PluginProcessor.cpp`. `Source/PresetManager.cpp` is not in the active
  CMake source list.
- Canonical global/reference/bass files currently use generic `.json`.
- Strong: several reference-preset parsers validate their own typed analysis
  arrays and schemas; factory/user inventory caches exist.
- Gaps in global presets: schema 1 is written but not checked, no product
  marker, import accepts any object containing `schemaVersion`, values are
  applied while parsing, missing fields preserve prior state inconsistently,
  and writes use `replaceWithText`.
- Reuse for: negative test cases around partial mutation and artifact confusion.

### Dire (`skadi`)

- Active source: `Source/skadi/state/preset/Preset.{h,cpp}`,
  `Source/skadi/state/libraries/Libraries.cpp`, and
  `docs/spec/02-preset-format.md`.
- Canonical extension: `.direpreset`; marker `direpreset`, current version 2.
- Strong: complete real-unit snapshot plus typed non-parameter state, full
  validation before apply, future-version refusal, explicit v1 migration,
  stable ordering/precision/locale, 20 MiB and depth-32 bounds, cross-field
  validation, embedded-content checks, off-thread content resolution, and
  newer-load-wins generation.
- Reuse for: rich presets, embedded content, validation, and async resolution.

### Shard (`splitter`)

- Active source: `Source/PluginProcessor.cpp` and
  `Source/native/ShardPresetBar.cpp`.
- Canonical extension: `.shardpreset`; binary `Shard` ValueTree state.
- Strong: product-specific extension and root type, strips editor geometry and
  prior preset identity, sanitizes hostile names, validates root before live
  restore, preserves destination editor size, and has
  round-trip/corrupt-no-op/path tests.
- Gaps: outer schema is not enforced by the preset loader, file size and nested
  content bounds are not evident, complete nested validation before
  `setStateInformation` is not proven, and `replaceWithData` plus a source
  comment is not sufficient evidence of atomic replacement.
- Reuse for: instance-state exclusion and corrupt-file no-op tests.

### Tether

- Active source: `Source/state/PresetManager.{h,cpp}`.
- Canonical extension: `.tether`; marker
  `MercurialTones.TetherPreset`, current schema 2; schema-1 `.json` read-only.
- Strong: branded extension, a 256 KiB pre-read user-file check plus a
  256K-character parser check, real units, collect-before-apply, factory/user
  deduplication, native-before-legacy precedence, background user scanning,
  cancellation, generation tokens, stale-publish rejection, and bounded UI
  delivery.
- Gaps: schema values are coercively cast and missing schema becomes v1; only v2
  validates the marker; v2 can omit three current parameters; UI preference
  parameters are serialized/required but not applied; catalog entries are
  published before full load validation and lack persistent stable IDs; an
  invalid user duplicate can suppress a valid factory entry; file/depth/count,
  symlink, and scan-to-click defenses are incomplete; apply publishes parameters
  one by one without Manta-style host/audio transaction; dirty suppression uses
  a cross-thread plain boolean; and `TemporaryFile` is not re-opened and
  validated before replacement. Synchronous rescans and multi-instance
  propagation also remain unresolved.
- Tested: the current `TetherProcessorTest` passed on this snapshot, but
  `TETHER_PRESET_TEST_SEAMS=0` excluded stale-scan/selection-remap assertions.
  No real host, live-audio, fault-injection, or cross-OS run was performed.
- Reuse for: a compact typed and asynchronous lifecycle scaffold, not a
  universal gold standard.

### Vanguard

- Active source: `Source/PluginProcessor.cpp` and
  `Source/native/VanguardNativeEditor.cpp`.
- Canonical files currently use generic `.json`, schema 1.
- Strong: current-schema completeness detection, safe reset path for
  sparse/legacy data, real-unit values, explicit old-mode migrations, path
  traversal guards, catalog cache/invalidation, batched host refresh, and
  round-trip/audio-switch tests.
- Gaps: no product marker, generic extension, direct `replaceWithText`, permissive
  numeric coercion/clamping, and no outer byte/depth/symlink bounds.
- Reuse for: default restoration, host batching, and inventory invalidation.

### Wavetable Editor

- Active source: `Source/state/WavetableStateCodec.{h,cpp}` and document methods
  in `Source/PluginEditor.cpp`.
- Canonical project extension: `.wte`.
- Strong: product-specific project document, root type, project/product/schema
  fields, multi-slot complete replacement, embedded wavetable data, metadata,
  and decode-before-editor replacement.
- Gaps: decoder checks the root but not the written product/schema fields, no
  outer byte/depth bound is evident, and saves use direct replacement without a
  separately validated temp transaction.
- Reuse for: project versus preset separation and embedded-content modeling.

## Composite conclusion

No single product owns every best practice. The preferred standard combines:

- Tether: compact typed and asynchronous lifecycle scaffold, with the gaps
  above corrected;
- Daedalus: hostile filesystem and atomicity;
- Dire: rich schema and content validation;
- Aegis: migration longevity;
- Manta: apply/host/audio behavior;
- Radiant and Shard: instance-state exclusion.

Any claim that “Manta has the best preset hygiene” must be narrowed: Manta has
some of the best runtime apply hygiene, while its current file identity and
outer validation lag the strongest products above.
