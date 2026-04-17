# ADR 0004 — Recipe validator + CI workflow

- **Status:** accepted
- **Date:** 2026-04-17
- **Deciders:** Robert MacCracken

## Context

Zugot's recipe correctness was being validated ad-hoc during PR review.
Pass 1 of the bazaar cross-reference audit surfaced 151 issues that had been
sitting in the tree unnoticed — stale `python3` deps, `libpipewire` vs
`pipewire` spelling drift, `-dev` split violations, filename ↔
`[package].name` mismatches, empty SHAs without TODO markers, four TOML parse
errors (unescaped `\.` in `"""..."""` strings that the lax Cyrius parser
tolerated but strict consumers rejected).

Manual review caught these eventually, but the signal was buried in reviewer
attention. A machine check would catch them at PR time instead of audit time.

## Decision

1. **`scripts/validate_recipes.py`** — Python stdlib-only validator. Four
   classes of check:
   - TOML/CYML parse errors (via `tomllib` — also serves as strict-parser
     lint; rejects `\.` inside `"""..."""` which the lax Cyrius CYML parser
     would silently accept)
   - Filename stem ≠ `[package].name` mismatches
   - Empty `sha256` values without an adjacent `# TODO` comment
   - Unresolved `[depends].runtime` / `[depends].build` entries (package
     must exist in zugot, or in a cross-referenced tree via
     `--check-against`)

2. **`.github/workflows/validate-recipes.yml`** — CI workflow runs the
   validator on every push to `main` and every pull request. Any failure
   blocks merge.

3. **`--check-against <path>`** flag — cross-reference mode. Used by bazaar's
   CI to fail PRs that reference packages not in zugot.

## Consequences

**Positive:**
- 151 legitimate issues surfaced + fixed in a single session; validator
  remains clean for future PRs
- Bazaar's PR flow can call `validate_recipes.py --check-against ../zugot`
  without duplicating logic; one source of truth
- The TOML parser doubles as an escape-sequence lint — fixed 4 real parse
  errors that strict consumers (Python `tomllib`, Rust `toml`) were rejecting

**Negative:**
- One more CI job — ~2 seconds of GitHub Actions time per PR
- Stdlib-only requirement rules out nice dependency graphs via `networkx`;
  validator intentionally stays Python stdlib only for portability

## Alternatives considered

- **`cargo`-style `takumi validate`** — rejected for now: takumi doesn't
  exist yet as a cross-recipe validator, and blocking zugot CI on future
  takumi work slows everything down
- **Recipe-format schema (JSON Schema)** — rejected: would require
  maintaining a schema file in sync with every recipe-format evolution, plus
  translating TOML to a schema-validated representation. The Python code is
  simpler and directly enforces the semantics we care about.

## Related

- `scripts/validate_recipes.py`
- `.github/workflows/validate-recipes.yml`
- CHANGELOG [1.0.0] — "P3 Roadmap — Tooling (2026-04-17)"
- CLAUDE.md §Validator
