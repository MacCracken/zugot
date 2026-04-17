# Contributing to Zugot

Thanks for helping harden the recipe database. Zugot is the foundation every
AGNOS install builds on; small drift here becomes large drift everywhere else.

## Prerequisites

- Git
- Python 3.11+ (for the validator)
- `curl` (for SHA256 verification of release tarballs)

## Quick path

1. **Pick a category.** Every recipe lives in exactly one of: `base/`,
   `desktops/`, `marketplace/`, `ai/`, `edge/`, `network/`, `browser/`,
   `python/`, `database/`, `sandbox/`.
2. **Copy the closest existing recipe** as a template. The recipe format is
   documented in [`README.md`](./README.md) and [`CLAUDE.md`](./CLAUDE.md).
3. **Fill every field.** `sha256` can be empty (`""`) only if followed by a
   `# TODO` comment for packages that haven't released yet.
4. **Run the validator:**
   ```sh
   ./scripts/validate_recipes.py
   ```
   Must exit `0`. CI will block the PR otherwise.
5. **Update `build-order.txt`** if you added a `base/` or `desktops/`
   recipe. Respect the dependency ordering — a recipe's build deps must
   precede it.
6. **Add a CHANGELOG entry** under `## [Unreleased]`, grouped by category,
   stating version bump (old → new) or whatever changed.

## Naming conventions

Canonical package names are NOT Debian/Ubuntu-style. Full list in
[`CLAUDE.md` §Naming Conventions](./CLAUDE.md). Most common gotchas:

- **No `-dev` suffix.** Use `wayland`, not `wayland-dev`.
- **`python`**, not `python3`.
- **`pkgconf`**, not `pkg-config`.
- **`linux-pam`**, not `pam`.
- **`nodejs`** (ships npm); **`python`** (ships pip).
- Group tag is **`"desktops"`** (plural), not `"desktop"`.

The validator enforces all of these. If you're adding a recipe and the
validator says "unresolved dep `X`", the fix is usually a rename per the
conventions above (or a new recipe if `X` genuinely isn't packaged).

## Security-sensitive recipes

If you bump a package with a security-relevant CVE, cite the CVE in the
recipe header comment and the CHANGELOG entry. Example:

```
# OpenSSL — TLS/SSL toolkit
# Bumped 2026-04-17 to 3.5.6 addressing CVE-2026-28386 (memory corruption
# in X.509 verification). See docs/audit/2026-04-17.md.
```

Monthly CVE audits live in [`docs/audit/`](./docs/audit/). If you spot a
vulnerability between audits, flag it in the CHANGELOG's `### Security`
subsection and optionally open a roadmap item in
[`docs/development/roadmap.md`](./docs/development/roadmap.md) §P1 or §P2.

## What counts as a "recipe bump"

A bump is **never** just a `version =` field change. Every bump requires:

1. `version` field updated
2. `[source] url` updated (the version typically appears in the URL)
3. `sha256` re-verified against the new tarball (download it; don't trust
   the upstream's own checksum file without fetching)
4. Header comment version references updated
5. Install-step comments / version-suffixed paths updated (common in
   `cpython`, `linux` kernel, `lvm2`)
6. Dependency list re-verified — upstream may have added or dropped deps
7. CHANGELOG entry

## Style

- **License field:** always SPDX identifier. GPL/LGPL/AGPL use `-only` suffix
  (`GPL-3.0-only`, not `GPL-3.0`).
- **Multi-line strings in `[build]` sections:** prefer `'''...'''` literal
  strings over `"""..."""` basic strings when the body contains shell
  escapes (`\;`, regex `\.`). The validator catches invalid escapes via
  `tomllib`, but literal strings sidestep the issue entirely.
- **Security hardening flags:** the default stack is
  `["pie", "fullrelro", "fortify", "stackprotector", "bindnow"]`. Override
  only with a comment explaining why (e.g. `libcap-ng` disables some flags
  because autoconf can't detect them when bootstrapping from autogen).

## PR checklist

- [ ] Recipe(s) updated with all fields audited
- [ ] SHA256 verified against the actual release tarball
- [ ] `./scripts/validate_recipes.py` exits clean
- [ ] `build-order.txt` updated if adding to `base/` or `desktops/`
- [ ] CHANGELOG entry added under `## [Unreleased]`
- [ ] Header comment reflects current version and any CVE rationale

## Cross-referencing bazaar

Bazaar (the community recipe overlay) is cross-checked against zugot via
`scripts/validate_recipes.py --check-against ../bazaar`. If a bazaar recipe
needs a package that zugot doesn't provide, either:

- Rename to zugot's canonical name (most common case — see
  `noted-issues-bazaar-finds.md` for examples), or
- Add the missing recipe to zugot under the appropriate category

## License

By contributing, you agree that your changes are licensed under GPL-3.0-only
(the same license as the rest of zugot).
