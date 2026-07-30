# Mercurial Tones Preset Hygiene Standard

## Purpose

This is the normative review standard for native Mercurial Tones products. It
combines the strongest verified mechanisms found across the product corpus; it
does not declare any one repository universally correct.

## 1. Artifact identity

Every persistent artifact must have exactly one role.

| Artifact | Typical coverage | Canonical extension |
|---|---|---|
| Full plug-in preset | Complete sound snapshot | `.<product>preset` |
| Layer/module preset | Declared owned subset | `.<product><kind>` or an established branded extension |
| Kit/project | Complete content document | Established product-specific kit/project extension |
| Reference/analysis target | Declared analysis data | Dedicated reference extension |
| UI preference | Machine/user preference only | Never masquerades as a sound preset |

For a new sound-preset format, prefer `.<product>preset`. JSON may be the
encoding, but `.json` is not the product identity. Existing shipped extensions
such as `.tether`, `.aegis`, `.direpreset`, `.daedpreset`, `.cspreset`,
`.shardpreset`, `.golemkit`, or `.wte` are stable compatibility surfaces and
must not be renamed casually.

The outer document must include:

- a stable, exact format marker;
- a stable product identifier;
- an integer schema version;
- a preset kind;
- an explicit coverage mode;
- metadata separated from sound-bearing data.

The reader must validate every discriminator it relies on. Merely serializing a
schema or product field is insufficient.

The format marker and product identifier are distinct fields even if their
strings contain overlapping information. Validate the schema as an exact
integer type; never coerce strings, booleans, or fractional numbers into a
version.

## 2. Coverage semantics

### Complete snapshot

A full preset defines every field it owns.

- New saves serialize the complete current schema.
- Missing current fields are invalid unless a named historical migration owns
  them.
- A supported historical schema migrates missing new fields to explicit
  defaults.
- Applying preset B after arbitrary preset A produces the same result as
  applying B to a fresh instance.

This is the Tether/Daedalus/Dire direction and the intended behavior behind
Manta/Vanguard default restoration.

### Declared subset

A module/layer/reference preset changes only a declared scope.

- The document declares its kind, target, and owned fields.
- Values outside that owned set are preserved intentionally.
- The UI names the scope so users do not confuse it with a full preset.
- The loader rejects fields outside the allowed subset.

Never infer sparse behavior from missing keys in a document that otherwise
looks like a full preset.

## 3. State inclusion policy

Include:

- stable host parameter IDs and their canonical real values;
- non-parameter state that changes sound;
- embedded or portable content required to reproduce the sound;
- content references only when they are stable, portable, and resolved under a
  documented policy.

Exclude:

- editor width, height, scale, active tab, selection, scroll, or browser state;
- current preset path/name as sound data;
- serial number, license, account, machine ID, preferences, and telemetry;
- caches, analyzer history, scratch buffers, runtime pointers, thread state,
  undo history, or transient generation state;
- absolute machine-specific file paths as the only content identity.

Radiant strips serial and editor size while reusing its session migration path.
Shard strips editor geometry and preset identity from `.shardpreset` payloads.
These are useful precedents.

### Content portability

Choose one policy per content class and encode it explicitly:

- Factory content: stable logical content ID plus an expected digest; resolve
  only from approved installed roots.
- User/generated content: embed it in a bounded container, or copy it into a
  manifest-controlled sidecar bundle with relative paths and digests.
- External reference: declare the preset nonportable, store a digest and useful
  metadata, and fail visibly when the exact content cannot be resolved.

Never make an absolute path the sole identity. For archives/bundles, reject
absolute paths, `..`, symlinks, duplicate names, decompression bombs, excessive
file counts, unsupported codecs, and decoded sample/frame limits. Verify every
digest before applying. Resolve/decode heavy content away from the message and
audio threads.

Do not embed factory or third-party content unless its redistribution rights
explicitly permit that export. A digest proves integrity, not publisher
authenticity; add a trusted signature policy only when the product accepts
signed publisher packs or other cross-origin content.

The session codec and preset codec may share a validated intermediate model and
migrations, but remain distinct artifact boundaries. A preset uses an explicit
allowlist/exclusion policy instead of serializing the entire DAW instance chunk
unchanged.

## 4. Values and parameter identity

- Parameter IDs are public persistence identifiers. Do not rename or reuse them
  without a migration.
- Store canonical real units, not incidental normalized positions, when range
  or skew changes could reinterpret old data.
- Prefer stable symbolic enum tokens when feasible. If an index is required,
  version every choice-list change and migrate explicitly.
- Reject NaN, infinity, wrong types, and out-of-contract values.
- Decide and test the unknown-field policy. For exact current-schema parameter
  sets, rejection is safest. If additive fields are intentionally tolerated,
  ignore them with diagnostics, never accidentally.
- Serialize deterministically: stable key order, locale-independent numbers,
  and enough precision for exact supported round trips.

## 5. Read transaction

The read path is:

1. Open an allowed regular file without following an untrusted link.
2. Enforce the byte limit before allocating the full payload.
3. Parse with bounded nesting and collection sizes.
4. Validate marker, product, preset kind, coverage, and schema.
5. Convert supported old schemas through sequential migrations.
6. Validate IDs, types, finite values, ranges, invariants, referenced content,
   and cross-field constraints.
7. Build an immutable temporary model.
8. Resolve heavy content away from the audio and message threads.
9. Apply the whole model under the product’s preset-load guard.
10. Publish identity/dirty/UI state only after success.

Any error before step 9 leaves live state unchanged. If apply itself can fail,
prepare the complete replacement state first or provide rollback.

Dire is the strongest rich-state precedent. Daedalus builds a decoded
`PresetData` before apply. Tether collects candidate parameter changes before
mutation, but its current completeness and type rules still need hardening.

## 6. Write transaction

The managed-library write path is:

1. Normalize a single filename or validated hierarchy.
2. Prove the destination remains under the user-preset root.
3. Reject dot segments, separators in a leaf, reserved device names where
   relevant, trailing dots/spaces, symlinks/reparse points, and non-regular
   collisions.
4. Serialize the current model to canonical bytes.
5. Create a unique temporary file in the destination directory with restrictive
   permissions.
6. Write all bytes and flush as required by the platform/risk.
7. Re-open and decode/validate the temporary file.
8. Atomically replace the destination.
9. Optionally fsync the parent directory where durability matters.
10. Publish catalog/identity/dirty changes only after success.

Clean orphan temp files under a bounded, unmistakable naming policy. Never
overwrite factory content. Daedalus is the strongest hostile-filesystem
precedent; Aegis validates temporary and final payloads; Tether uses JUCE
temporary-file replacement.

`replaceWithText()` by itself is not evidence of atomicity.
For the selected JUCE/platform implementation, document the actual replacement
primitive, same-filesystem assumption, collision semantics, restrictive
permissions, flush/durability policy, and orphan cleanup; prove failure behavior
with fault injection.

## 7. Library lifecycle

- Use standard OS product directories with a documented writable fallback.
- Keep read-only preferred locations discoverable when save falls back.
- Give native managed entries opaque stable IDs independent of display names
  and paths. Persist the ID in the document or a validated signed/compiled
  manifest; path/name/provenance alone is not a stable native identity.
- Record factory/user provenance.
- Define a complete precedence matrix. The safe default for the same logical
  identity is user-native, user-legacy, factory-native, then factory-legacy;
  native wins legacy within a provenance, while user content continues to
  shadow factory content.
- Deduplicate deterministically and sort independently of filesystem order.
- Decode and fully validate a catalog entry before it participates in
  precedence or deduplication. An invalid native/user entry must be diagnosed
  but must not hide an otherwise valid legacy/factory entry.
- Bound recursion, files, bytes, and catalog entries.
- Derive concrete bounds from the largest legitimate artifact plus a documented
  safety margin and peak decoded-memory/time budget. Freeze the numbers in the
  format spec and test just below, at, and just above every boundary.
- Scan on open, explicit refresh, or known mutation—not every UI timer tick.
- Freeze a message-thread latency and memory budget. Scan and decode off the
  message thread whenever the maximum supported library can exceed it; a vague
  “large catalog” threshold is not a contract.
- Publish immutable catalog snapshots with cancellation and generation tokens.
- Reject stale completions and make teardown safe.
- A load should use the catalog’s validated identity/snapshot or revalidate the
  file; it must not trust a path that changed between scan and click.

Tether is a useful compact asynchronous-lifecycle scaffold, but its current
catalog validation and stable identity are incomplete. Daedalus publishes a
decoded catalog so selection does not reparse a changed file.

## 8. Host and audio behavior

- Suppress dirty tracking during apply, then clear dirty only after success.
- Avoid per-parameter host-notification storms; update host display once unless
  a wrapper requires another proven path.
- Establish a fresh undo baseline after load; a failed load changes no undo
  state.
- Keep parsing, file I/O, allocation, content decode, and locks off the audio
  thread.
- Reset or replace internal DSP state explicitly.
- Crossfade or otherwise transition when tails, delay buffers, oscillators, or
  discontinuous topology can click.
- Record the product-specific apply decision: immutable block-boundary swap,
  state reset, bounded crossfade, or a proven combination. Derive it from DSP
  tails and discontinuities, then verify it with active audio rather than from
  notification calls alone.
- Test with the editor closed and multiple instances. Catalog changes and
  preferences may be shared even when live sound state is not.

Manta provides the strongest current transition/default/dirty precedent.
Vanguard demonstrates host refresh batching and inventory invalidation.

## 9. Migration policy

Use dual-read/single-write:

- New code reads the native extension first and supported legacy formats second.
- Native-first applies within one provenance/logical identity and must not make
  a factory-native file unexpectedly defeat a user-legacy override.
- New saves always use the current native schema and extension.
- Each migration maps one declared source schema to the next or directly to one
  fully validated current model.
- Future versions are refused, not guessed.
- Automatic conversion never destroys the sole readable source before the
  native replacement is written and validated.
- Rename, category, and stable-ID changes preserve identity intentionally.
- Factory content upgrades are versioned and cannot overwrite user data.
- If a legacy format has no stable ID, define the migration identity algorithm
  before conversion. A namespaced deterministic ID derived from product,
  provenance, and normalized logical path is suitable when collision handling
  and platform case rules are tested; otherwise persist an explicit conversion
  map.
- Define logical delete behavior while both formats coexist. Deleting a user
  entry must not silently resurrect its shadowed legacy sibling; remove/archive
  all user representations with explicit confirmation or persist a tombstone.
  Factory representations remain immutable.
- State how long legacy factory mirrors remain installed for downgrade or
  side-by-side compatibility, and test clean install, upgrade, downgrade, and
  rollback against that support window.

Historically permissive loaders are not a schema. Inventory shipped factory
assets and representative user files, classify the variants actually accepted,
and write explicit adapters for the variants the product chooses to support.
Quarantine/report the rest instead of preserving accidental coercion forever.

Aegis is the strongest multi-version precedent. Dire is the strongest
validation-heavy schema migration precedent.

## 10. Minimum test matrix

### Format and semantics

- deterministic/canonical serialization;
- every current field round-trips at min/default/max and representative values;
- supported historical schemas migrate to the expected current model;
- future schema, wrong marker/product/kind, missing discriminator, and ambiguous
  coverage are rejected;
- A-to-B-to-fresh equivalence for complete presets;
- declared-subset preservation and rejection outside the owned set;
- unknown IDs/fields follow the documented policy.

### Hostile data and filesystem

- empty, corrupt, truncated, oversized, deeply nested, huge count/string;
- wrong types, NaN/infinity, under/overflow, out-of-range, duplicate IDs;
- traversal, absolute path, separators, reserved names, trailing dot/space;
- symlink/reparse escape, irregular file, collision, read-only directory;
- interrupted/short write, disk-full simulation, orphan temp, replacement
  failure, post-write validation failure;
- factory overwrite/delete refusal;
- native/legacy shadow deletion when both coexist; test rename/delete only when
  the product exposes those operations, and otherwise record the unsupported
  capability explicitly.

### Runtime

- failed load is byte/state-equivalent no-op;
- dirty, preset identity, undo, and host refresh are correct;
- rapid switch and active-audio behavior is finite and click-safe;
- editor closed, reopen, two instances, teardown during scan/load;
- stale async result never wins over a newer request;
- referenced/embedded content at maximum supported size;
- standalone plus reported host/OS/wrapper when behavior is host-specific.

## 11. Evidence discipline

Static patterns are leads. A product-specific extension does not prove its
contents are typed; a schema field does not prove the loader enforces it;
`TemporaryFile` does not prove every failure path is correct; a happy-path
round trip does not prove no state leakage.

Record the active source location, exact revision, tests run, host/OS, and
remaining unrun gates. Mark those gaps `open-risk`.
