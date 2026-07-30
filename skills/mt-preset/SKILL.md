---
name: mt-preset
description: Audit, design, migrate, harden, and verify Mercurial Tones native audio plug-in preset systems. Use for product-specific preset extensions, JUCE or Skia preset save/load code, schema and migration design, factory and user preset libraries, complete versus sparse preset semantics, missing-parameter state leakage, corrupt or hostile preset files, atomic saves, path traversal, import/export, dirty state, host notifications, audio-safe preset switching, or cross-product preset hygiene reviews.
---

# MT Preset Hygiene

Treat every preset as an untrusted, versioned product document that must define
sound state predictably without carrying instance-only state.

## Start Here

1. Freeze repository identity:
   - record branch, commit, dirty state, product version, and active source root;
   - trace `CMakeLists.txt` or the project file to the compiled preset code;
   - do not treat copied managers, plans, generated assets, or embedded mirrors
     as active implementation.
2. Read [references/standard.md](references/standard.md), then consult
   [references/product-map.md](references/product-map.md) for precedents and
   known gaps.
3. Run `python3 scripts/audit_presets.py <active-source-root>` for a
   deterministic lead inventory. Treat every result as a candidate to inspect,
   never as proof.
4. Use [references/format-template.md](references/format-template.md) when
   defining or revising a format.
5. Label conclusions:
   - `runtime-proven`: exercised in a real plug-in/host or fault-injection run;
   - `tested`: covered by a deterministic automated test;
   - `active-static`: present in the compiled source path;
   - `documented`: stated by an authoritative spec but not otherwise proven;
   - `proposed`: recommended change only;
   - `open-risk`: relevant behavior remains unverified or unsafe.

Say explicitly when inspection proves a mechanism but not host, OS, filesystem,
audio-transition, or failure behavior.

## Define the Preset Contract First

Before editing code, answer:

- What artifact is this: full product preset, layer/module preset, kit, project,
  reference target, or UI preference?
- Is coverage `complete` or an intentionally `declared-subset`?
- Which stable parameter IDs and non-parameter sound state does it own?
- Which instance, host, UI, cache, license, path, and runtime fields must never
  travel?
- What is the canonical extension, exact format marker, product identifier,
  preset kind, coverage marker, current schema, minimum readable schema, and
  migration chain?
- Are values stored in real units, stable symbolic enum values, or another
  explicitly versioned representation?

Never mix full-snapshot and sparse-patch semantics. A complete preset resets
missing historical fields only through a named migration with explicit
defaults; a current-schema complete preset with a missing owned field is
invalid. A declared subset preserves fields outside its owned set by design.

## Non-Negotiable Hygiene

- Give canonical saves one opaque product-specific extension. Prefer
  `.<product>preset` for a new format. Preserve an already-shipped branded
  extension when changing it would create needless migration.
- Put an exact format marker, a separate stable product identifier, preset kind,
  coverage marker, and integer schema version inside the file. Validate every
  discriminator with exact types; writing fields that are never checked is not
  a format contract.
- Do not use generic `.json` for new canonical preset files. JSON may remain the
  internal encoding. Read legacy `.json` only through an explicit compatibility
  adapter and never write new legacy files.
- Parse, bound, migrate, and fully validate into a temporary model before
  touching live state. A rejected preset is a clean no-op.
- Use stable parameter IDs and canonical real units. Reject non-finite and
  out-of-contract values rather than relying on incidental casts or clamps.
- Capture all sound-bearing state owned by the preset. Exclude editor geometry,
  selection, preset-browser identity, undo history, caches, runtime pointers,
  license data, serials, and machine-specific absolute paths.
- Bound file bytes, nesting, collection sizes, strings, recursion, and catalog
  count. Treat imports and user directories as hostile filesystems.
- Keep managed-library paths contained under their canonical root; reject dot
  segments, symlink/reparse escapes, irregular files, and unsafe names.
- Save through a same-directory temporary file, verify the written payload, and
  atomically replace the destination. Never expose a truncated canonical file.
- Keep factory data immutable. Persist an opaque stable ID for each native
  managed entry, independent of path and display name. Give factory and user
  entries deterministic precedence, deduplication, sorting, and explicit delete
  rules. An invalid preferred representation must not suppress a valid one.
- Keep disk scans and content resolution off the audio thread. Move large
  catalogs off the message thread, publish immutable snapshots, and reject stale
  async completions.
- Suppress dirty tracking while applying, update host display once where
  appropriate, and preserve real-time safety. Add a bounded transition when the
  product has tails or discontinuous state that can click.

## Audit Workflow

Inspect in this order:

1. Format identity: extension, marker, schema, product and preset kind.
2. Coverage: complete/sparse rules, stable IDs, real units, non-parameter state,
   and excluded instance state.
3. Read boundary: byte/depth/count limits, parser behavior, version refusal,
   migrations, finite/range checks, and unknown-field policy.
4. Apply boundary: validate-before-mutate, default restoration, rollback/no-op,
   host notification batching, dirty state, undo, and audio transition.
5. Write boundary: name/path handling, root containment, symlinks, permissions,
   temporary file, verification, atomic replacement, and failure recovery.
6. Library lifecycle: standard directories, writable fallback, factory/user
   precedence, deduplication, stable identity, scan scheduling, cancellation,
   generation ordering, and multi-instance changes.
7. Tests and runtime evidence.

Report each issue with active file and line, evidence label, failure mode,
severity, smallest safe correction, and missing verification. Use `critical`
for corruption/security/data loss, `high` for state, audio, host, or common
workflow failure, `medium` for bounded compatibility/UX failure, and `low` for
latent hygiene with limited impact. State uncertainty instead of inflating
severity. Do not call the whole product clean because a regex inventory or
round-trip happy path passes.

## Migration Rules

Use dual-read/single-write migration:

1. Within the same provenance/logical identity, discover the native extension
   before legacy `.json`; preserve the product's explicit user-versus-factory
   precedence.
2. Parse legacy input with its declared historical schema.
3. Convert it into the current temporary model.
4. Validate the current model completely.
5. Apply it transactionally.
6. On an explicit save or approved migration, write only the native extension.
7. Verify the native file before hiding, archiving, or deleting a legacy copy.

Reject future schemas cleanly. Keep migrations deterministic and sequential;
test every supported historical version. Do not silently reinterpret the same
number after enum choices or parameter ranges change.

## Verification Gate

Require tests proportional to the format:

- canonical serialization and fresh-instance round trip;
- A-to-B leakage test proving missing fields default or preserve exactly as the
  declared coverage requires;
- corrupt, truncated, oversized, deeply nested, wrong-marker, wrong-product,
  unsupported-version, non-finite, out-of-range, and unknown-ID cases;
- path traversal, absolute path, separator, trailing-dot/space, symlink,
  irregular-file, and overwrite/factory-protection cases;
- interrupted write, orphan temp, destination collision, read-only directory,
  disk-full/write-failure simulation, and post-write validation;
- factory/user identity, precedence, deduplication, legacy migration, stale
  async publish, and teardown; test rename/delete when supported, and record
  their absence as a capability decision rather than a defect unless required;
- dirty flag, undo baseline, single host refresh, automation reflection, rapid
  switching, active audio, editor closed, and at least two instances;
- sound-bearing embedded/reference content at maximum supported size;
- real-host validation when the failure depends on a DAW, wrapper, OS, or live
  audio transition.

Stop at `open-risk` when a relevant failure or host gate is unrun.

## Cross-Product Judgment

Do not copy one product wholesale. The current strongest composite is:

- Tether for a useful compact typed format and asynchronous library scaffold,
  while correcting its catalog-validation, identity, apply, and write gaps;
- Daedalus for hostile-file and atomic-write discipline;
- Dire for rich schema, validation, migration, and content resolution;
- Aegis for long-lived version adapters and validated native conversion;
- Manta for default restoration, dirty/host behavior, and audio transitions;
- Radiant and Shard for excluding instance-only state.

Manta is a strong runtime precedent, not the current file-format gold standard:
its active canonical path still uses generic `.json` and does not enforce its
written schema envelope on read.
