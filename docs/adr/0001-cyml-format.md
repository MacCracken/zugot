# ADR 0001 — Adopt CYML format for recipes

- **Status:** accepted
- **Date:** 2026-04-16
- **Deciders:** Robert MacCracken
- **Context for:** consumers (ark, nous, takumi, mela) and recipe authors

## Context

Zugot shipped recipes as `.toml` files from the start. Cyrius (the AGNOS
systems language) added CYML — a superset of TOML with a `.cyml` extension and
an optional markdown body after a `---` delimiter.

Two options were on the table for zugot:
1. Keep `.toml`
2. Move to `.cyml` to stay consistent with the rest of the Cyrius-built
   AGNOS ecosystem

## Decision

Rename every recipe `*.toml → *.cyml` via `git mv` (history preserved).
Content unchanged: CYML parses single-entry files (no `---` delimiter) as
plain TOML, so every existing recipe continues to parse without modification.

## Consequences

**Positive:**
- One file format across all AGNOS repositories
- Future-proofs recipes if we ever want to attach prose bodies (e.g. multi-
  line install scripts as markdown fenced blocks) without another migration
- Cyrius's CYML parser is the reference implementation; tooling consolidates

**Negative / requires work:**
- Downstream consumers (ark, nous, takumi, mela) must accept both or be
  updated to `.cyml`
- IDE syntax highlighting for `.cyml` is weaker than `.toml`; workarounds:
  file-type association to TOML mode

**Mitigations:**
- Strict TOML-compatible parsers (Python `tomllib`, Rust `toml` crate) accept
  CYML single-entry files unchanged — zero ecosystem cost for tooling
- The validator (`scripts/validate_recipes.py`) uses `tomllib` and therefore
  doubles as a lint against any invalid escape sequences that the lax CYML
  parser might tolerate

## Alternatives considered

- **Keep `.toml`** — rejected: splits the ecosystem's file convention and
  makes the future prose-body option a second migration
- **Dual-extension period** — rejected: resolvers would need to handle both
  for an indefinite window; clean cut was simpler

## Related

- CHANGELOG.md [1.0.0] — "Recipe file format: `.toml` → `.cyml`"
- 426 recipes renamed in the same commit as this ADR was drafted
