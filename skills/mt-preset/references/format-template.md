# Preset Format Template

## Default for a new full preset

Use one opaque extension, preferably `.<product>preset`. The example below
shows JSON as an internal encoding; callers and file choosers expose only the
product extension.

```json
{
  "format": "com.mercurialtones.manta.preset",
  "schemaVersion": 1,
  "productId": "manta",
  "presetKind": "main",
  "coverage": "complete",
  "presetId": "018f10d7-4a8a-7cc2-b9d0-5bb22d6f3b1c",
  "metadata": {
    "name": "Wide Echo",
    "author": "",
    "category": "Space"
  },
  "parameters": {
    "delayTimeMs": 375.0,
    "feedbackPercent": 42.0,
    "mixPercent": 25.0
  },
  "state": {
    "timedTapMask": "10101010",
    "leftEnvelope": [],
    "rightEnvelope": []
  }
}
```

Use the product’s real stable IDs and units. Keep metadata nonfunctional unless
the contract explicitly says otherwise. `presetId` is opaque and survives
rename, category changes, and save; only an explicit “Save as copy” creates a
new ID.

## Declared-subset variant

Sparse documents need an unmistakable kind and scope:

```json
{
  "format": "com.mercurialtones.manta.preset",
  "schemaVersion": 1,
  "productId": "manta",
  "presetKind": "postEq",
  "coverage": "declared-subset",
  "target": "postEq",
  "ownedFields": [
    "postEq.band1.enabled",
    "postEq.band1.frequencyHz",
    "postEq.band1.gainDb",
    "postEq.band1.q"
  ],
  "parameters": {
    "postEq.band1.enabled": true,
    "postEq.band1.frequencyHz": 120.0,
    "postEq.band1.gainDb": -2.5,
    "postEq.band1.q": 0.8
  }
}
```

The loader validates `ownedFields` against the exact allowlist for `postEq`.
Fields outside that scope are rejected. Omitted owned fields either default or
are invalid according to that preset kind’s documented rule.

## Content-bearing presets and kits

Use a manifest inside the product-specific container:

```json
{
  "content": {
    "assets": [
      {
        "id": "pad.01.sample",
        "mode": "embedded",
        "path": "assets/pad-01.wav",
        "mediaType": "audio/wav",
        "sha256": "<64 lowercase hex characters>",
        "decodedFrames": 88200,
        "channels": 2
      },
      {
        "id": "pad.02.sample",
        "mode": "factory",
        "factoryContentId": "golem.factory.snare.crispy.v1",
        "sha256": "<64 lowercase hex characters>"
      }
    ]
  }
}
```

The outer `.golempreset` or `.golemkit` may be a bounded archive rather than
plain JSON. Validate the manifest before extraction, keep every path under a
temporary extraction root, enforce compressed and decoded limits, verify
digests, prepare every pad, then replace the live kit once. An external-path
mode must be explicitly nonportable and cannot use the path as its only
identity.

## Reader shape

Implement the reader as a transaction:

```text
read bounded bytes
  -> parse bounded document
  -> validate envelope
  -> dispatch exact schema
  -> migrate to CurrentPreset
  -> validate every current invariant
  -> resolve content into a prepared replacement
  -> apply once
  -> publish identity and clear dirty
```

Do not call parameter setters while parsing.

## Writer shape

```text
capture CurrentPreset
  -> canonical serialize
  -> same-directory unique temp
  -> write + flush
  -> decode and validate temp
  -> atomic replace
  -> update catalog and identity
```

Keep the old canonical file intact until replacement succeeds.

## Version rules

- `schemaVersion` is an integer.
- The exact format marker namespaces the schema. A new branded format may start
  at schema 1 even when a legacy JSON schema also used 1, provided dispatch
  selects a distinct legacy adapter before interpreting the number.
- Readers accept only explicitly supported versions.
- Readers reject a version newer than the current implementation.
- Writers emit only the current version.
- Each historical schema has a test fixture and deterministic expected current
  model.
- Range, enum, unit, ID, and structural changes require a migration decision,
  not only a number bump.

## Extension migration

For a product moving from `.json` to a native extension:

1. Scan native files first and legacy JSON second.
2. Resolve the explicit precedence matrix. Within one provenance/logical
   identity native wins legacy; user content should not be displaced by a
   factory-native duplicate.
3. Fully decode and validate candidates before deduplication. An invalid
   preferred candidate is diagnosed but cannot suppress a valid fallback.
4. Legacy loader validates the historical JSON contract.
5. Loading does not rewrite implicitly unless product policy explicitly permits
   it.
6. The next user save writes only the native extension/current schema.
7. A bulk migration writes and verifies every native file, produces a report,
   and archives legacy input before any deletion.

If legacy files have no stable ID, specify a deterministic namespaced migration
ID or persist a conversion map. Define delete/tombstone behavior so removing a
native user file cannot reveal an older legacy sibling unexpectedly.

For Manta, a new name such as `.mantapreset` is clearer than continuing generic
`.json`, but the rollout must retain read compatibility and must not copy
Manta’s current loose outer-envelope validation into the new format.

## Coverage checklist

Before finalizing a schema, inventory:

- all host parameters;
- sound-bearing non-parameter state;
- embedded or referenced content;
- legacy/retired parameters;
- instance-only and UI-only fields;
- choice lists and their stable meanings;
- defaults for every supported historical version;
- constraints spanning more than one field;
- maximum byte/count/depth/string sizes;
- factory/user identity and library behavior.
