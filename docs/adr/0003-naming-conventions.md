# ADR 0003 — Canonical package naming conventions

- **Status:** accepted
- **Date:** 2026-04-17
- **Deciders:** Robert MacCracken

## Context

The first bazaar cross-reference audit (pass 1) found 91 unresolved
dependencies between bazaar recipes and zugot — most of them the same class
of bug: contributors reaching for Debian/Ubuntu naming conventions that
don't exist in zugot.

- `wayland-dev`, `ncurses-dev`, `openssl-dev`, etc. (the `-dev` split)
- `python3` (zugot has `python`)
- `pkg-config` (zugot has `pkgconf`)
- `pam` (zugot has `linux-pam`)
- `libx264` (zugot has `x264`)

Contributors kept re-inventing these names, and recipes kept failing to
resolve. The problem wasn't the names themselves; it was the absence of a
canonical list.

## Decision

Publish a named-and-numbered list of conventions in CLAUDE.md's "Naming
Conventions" section, referenced from README.md. Every rule has a one-line
rationale.

The nine rules:

1. **No `-dev` split.** Headers and `.pc` files ship with the runtime
   package. Dep on `wayland`, not `wayland-dev`.
2. **`python`, not `python3`.** The `python` recipe provides Python 3.
3. **`pip` ships with `python`.** Invoke `python -m pip`; don't list as
   a dep.
4. **`npm` ships with `nodejs`.** Dep on `nodejs`.
5. **`pkgconf`, not `pkg-config`.** `pkgconf` installs a compat symlink but
   recipes depend on the canonical name.
6. **Groups use plural `"desktops"`** — see ADR 0002.
7. **`linux-pam`, not `pam`.** Recipe name includes the `linux-` prefix.
8. **`x265`, not `libx265`; `x264`, not `libx264`.** Upstream project names
   don't carry the `lib` prefix.
9. **PyPI packages** (e.g. `pycups`, `pycurl`): don't create zugot recipes
   unless needed as a system runtime. Apps use `python -m pip install` in a
   virtualenv during build.

Meta-package aliases exist for historically-common Debian/Ubuntu names that
keep surfacing (`pip`, `npm`, `pkg-config`, `clang`, `lld`, `gfortran`,
`libuuid`, `libltdl`, `libgbm`, `libseat`, `pipewire-jack`). Each alias is a
zero-build recipe that depends only on the canonical package.

## Consequences

**Positive:**
- Bazaar cross-ref dropped from 91 unresolved → 0 after the meta-package
  aliases landed
- New contributors hit a consistent convention instead of reverse-engineering
  it from whichever recipe they copied

**Negative:**
- Meta-packages add nine "fake" recipes to the tree. Mitigation: they're
  cheap (empty `[build]` sections), clearly labeled with "meta" in groups,
  and documented in header comments.

## Alternatives considered

- **No canonical names, accept whatever contributors write** — rejected: the
  bazaar audit proved this path multiplies resolution failures
- **Rewrite every bazaar recipe to zugot conventions in-tree** — rejected:
  bazaar is a separate repo; we don't own its source. Meta-packages let us
  accept both spellings without owning bazaar's churn.

## Related

- CLAUDE.md §Naming Conventions (rules 1-9)
- `scripts/validate_recipes.py` — enforces dep resolution against these names
