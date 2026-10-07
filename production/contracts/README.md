# production/contracts: the pinned publishing contract

**PROPOSED** (Feltwillow Blueprint v3, change set G3; nothing here is in use yet).

This folder holds a copy of the publishing contract that `production/export_handoff.py` writes
against. The contract is authored only in the publishing repository (`jeilealr/feltwillow-publishing`,
`publishing/schemas/`). Production never edits it; it pins a released copy.

```
production/contracts/
  CONTRACT.lock                         which contract package is pinned (record kind contract-lock, v1)
  feltwillow-contracts/<version>/             the released files, unmodified (schemas/*.schema.json, ...)
  feltwillow-contracts-<version>.tar          optional: the release archive; if present its sha256 is checked
  README.md                             this file
```

## What `CONTRACT.lock` says

| Field | Meaning |
|---|---|
| `package.name` | always `feltwillow-contracts` |
| `package.version` | release version, e.g. `0.2.0-h2` (draft) or `1.0.0`; also the folder name under `feltwillow-contracts/` |
| `package.archive_sha256` | sha256 of the release tar the publishing repo produced; copied into every handoff (`contract_package`) |
| `package.source_repository`, `source_commit`, `released_at` | where and when it was released |
| `canonicalization` | always `feltwillow-canonical-json-v1` |
| `files[]` | every pinned file with its sha256; the exporter refuses if a file differs, is missing, or an unlisted file is present |
| `producer_emits.production-handoff` | the handoff schema version this production exporter must write (now `1`) |
| `example` | `true` only for examples; a handoff exported under an example lock is itself marked `example: true` and a real import refuses it |

The `CONTRACT.lock` delivered in this change set is an **example**: version `0.2.0-h2`,
`canonicalization: feltwillow-canonical-json-v1`, `example: true`, a synthetic `archive_sha256` (the same
placeholder as the publishing scaffold's examples; no contract package has been released),
`source_commit: null`. Its `files[]` are the real digests of the 36 H2 schemas in the publishing scaffold
(`publishing/contracts/schemas/`), identical to the scaffold's `contract-lock.example.json`.

## Updating the pinned contract (owner)

1. In `feltwillow-publishing`, release the contract (proposed command `python -m feltwillow_publish.contracts release
   --version X.Y.Z`); it prints the archive sha256 and writes a `contract-lock` record.
2. Copy the release tar and the lock record to this machine (ordinary file copy).
3. Extract the tar into `production/contracts/feltwillow-contracts/X.Y.Z/`, replace `CONTRACT.lock`, optionally
   keep the tar as `production/contracts/feltwillow-contracts-X.Y.Z.tar`.
4. Check: `python3 production/export_handoff.py verify-contract` must print `"result": "ok"`.
5. Commit (owner does all git). The exporter refuses to export while anything under
   `production/contracts/` is uncommitted (`CONTRACT_PIN_DIRTY`).

Never edit a pinned file by hand; a hand edit is caught as `CONTRACT_LOCK_MISMATCH`. Rolling back means
pinning the previous release again (lock change only). Publishing accepts a set of handoff versions,
so production may switch only after publishing supports the new version (consumer first).
