# Zugot — Claude Code Instructions

## Project Identity

**Zugot** (Hebrew: זוּגוֹת — pairs, as in the paired creatures that entered the ark) — Recipe repository for AGNOS

- **Type**: Recipe database (CYML files, not a Rust crate)
- **License**: GPL-3.0-only
- **Version**: 1.0.0 (released 2026-04-17)
- **Genesis repo**: [agnosticos](https://github.com/MacCracken/agnosticos)
- **Philosophy**: [AGNOS Philosophy & Intention](https://github.com/MacCracken/agnosticos/blob/main/docs/philosophy.md)
- **Standards**: [First-Party Standards](https://github.com/MacCracken/agnosticos/blob/main/docs/development/applications/first-party-standards.md)

## What This Is

Zugot is the package database for AGNOS. Every package that can be built or installed — from the C library to the desktop compositor to the science crates — has a recipe here. Recipes are CYML files (`.cyml`, TOML syntax parsed by Cyrius's CYML parser) consumed by ark (package manager), nous (resolver), and takumi (build system).

Zugot is NOT a Rust crate. There is no Cargo.toml, no src/ directory, no compilation. The "code" is CYML recipe files. The quality gates are validation scripts, not cargo clippy.

## Consumers

- **[ark](https://github.com/MacCracken/ark)** — package manager (installs from recipes)
- **[nous](https://github.com/MacCracken/nous)** — resolver (reads dependency graphs from recipes)
- **[takumi](https://github.com/MacCracken/takumi)** — build system (executes build steps from recipes)
- **[mela](https://github.com/MacCracken/mela)** — marketplace (distributes marketplace packages)

## Development Process

### P(-1): Recipe Hardening (before adding new recipes)

The P(-1) process for zugot is a full audit of existing recipes before any new work begins. Recipes accumulate drift — versions fall behind, SHAs become stale, upstream dependencies change. P(-1) catches this.

0. Read the roadmap and CHANGELOG — know what was intended and what changed recently
1. **Version audit** — for every recipe category being touched, cross-check recipe versions against actual upstream releases (crates.io, GitHub tags, upstream project pages)
2. **SHA256 verification** — verify all SHA256 hashes against actual release tarballs. Flag any empty or placeholder hashes
3. **License audit** — verify every recipe's `license` field matches the actual LICENSE file in the source repo. Must use SPDX `-only` suffix (`GPL-3.0-only`, not `GPL-3.0`)
4. **Dependency audit** — verify runtime and build dependencies are complete and current. Check if upstream has added or removed dependencies
5. **Field completeness** — every recipe must have: name, version, description, license, groups, source, depends, build steps, security hardening flags. Marketplace recipes must also have: category, runtime, publisher, tags, min_agnos_version
6. **Header comment sync** — verify header comments match the actual version and status. Fix stale "Scaffolded v0.1.0" comments on stable crates
7. **Build order validation** — if touching base/desktops recipes, verify `build-order.txt` is correct and complete
8. **Structural audit** — verify install blocks are in the correct CYML section (`[build]` not `[security]`), no duplicate fields, no stale references
9. **Documentation** — update CHANGELOG with all findings and fixes

### Work Loop (continuous)

1. **Work phase** — new recipes, version bumps, category additions, upstream sync
2. **Validation** — run `takumi validate` or equivalent on all changed recipes
3. **Cross-check** — verify versions against upstream (crates.io, GitHub, project sites)
4. **SHA256** — download actual tarballs and compute SHA256 for any new or bumped recipes
5. **Dependency check** — verify all runtime and build deps are listed and current
6. **Build order** — if base/desktops recipe changed, verify `build-order.txt` is still correct
7. **Review** — check for stale comments, wrong license suffixes, missing fields
8. **If heavy changes → return to step 2** — keep validating until clean
9. **Documentation** — update CHANGELOG with changes. Group by category. Note version bumps with old → new. Update roadmap if applicable
10. Return to step 1

### Task Sizing

- **Low/Medium effort** (single recipe bump, new marketplace recipe): Batch freely — multiple recipes per work loop cycle
- **Large effort** (base system version bump, new category, build-order changes): Small bites only — one recipe at a time, verify each before moving to the next. Base system recipes affect everything downstream
- **If unsure**: Treat it as large. A wrong base recipe breaks the entire build

### Naming Conventions (for recipe authors and downstream consumers)

Packages in zugot follow Linux-distribution-agnostic naming. The short rules:

1. **No `-dev` split.** Headers and `.pc` files ship with the runtime package. Do not reference `wayland-dev`, `ncurses-dev`, `libevent-dev`, etc. — use the plain name (`wayland`, `ncurses`, `libevent`).
2. **Python packages use `python`, not `python3`.** The `python` recipe provides Python 3; `python3` is not a valid dep name.
3. **`pip` ships with `python`.** Do not list `pip` as a separate dep. Invoke `python -m pip` in build scripts.
4. **`npm` ships with `nodejs`.** Same pattern — depend on `nodejs`.
5. **Use `pkgconf`, not `pkg-config`.** The `pkgconf` recipe provides a `pkg-config` compatibility symlink at install time, but recipes should depend on the canonical name (`pkgconf`).
6. **Groups use plural `"desktops"`, not `"desktop"`.** Multiple desktop environments are planned; the group tag reflects that.
7. **Use `linux-pam`, not `pam`.** The recipe name includes the `linux-` prefix.
8. **Use `x265`, not `libx265`; `x264`, not `libx264`.** Upstream project names don't have the `lib` prefix.
9. **PyPI packages** (e.g. `pycups`, `pycurl`): don't create zugot recipes unless needed as a system runtime. Applications should invoke `python -m pip install <pkg>` in a virtualenv during build, or list the pip package in an app-level manifest.

See `noted-issues-bazaar-finds.md` for cross-referenced examples from the bazaar audit.

### Recipe Work Rules

Every recipe change requires a full field audit — **never just bump a version**.

1. Verify: name, version, SHA256, license (`-only` suffix), tags, build commands, `min_agnos_version`, dependencies
2. Cross-check version against crates.io, GitHub release tags, or upstream release
3. Verify SHA256 against actual release tarball
4. Confirm license matches the actual repo LICENSE file
5. Confirm dependencies are complete (runtime and build)
6. Confirm security hardening flags are appropriate
7. Test with `takumi validate` if available

### Adding a New Recipe

1. Determine category (base, desktops, marketplace, ai, edge, network, browser, python, database, sandbox, bazaar)
2. Copy the closest existing recipe as a template
3. Fill ALL fields — no empty fields except SHA256 for unreleased packages (must have `# TODO` comment)
4. Verify build steps actually work
5. Add to `build-order.txt` if it's a base/desktopss package (respect dependency ordering)
6. Update CHANGELOG

### Version Bumps

1. Update `version` field
2. Update `[source]` URL and SHA256
3. Update header comment version references
4. Check if any install script comments reference the old version
5. Verify dependencies haven't changed upstream
6. Test build if possible
7. Update CHANGELOG with old → new version

## DO NOT

- **Do not commit or push** — the user handles all git operations
- **NEVER use `gh` CLI** — use `curl` to GitHub API only
- Do not add recipes with dummy SHA256 without a `# TODO` comment
- Do not change license fields without verifying against the actual repo
- Do not reorder `build-order.txt` without understanding the full dependency chain
- Do not bump a version without auditing ALL fields in the recipe
- Do not assume upstream dependencies haven't changed — check every time

## Documentation Structure

```
zugot/
├── VERSION                              — current release (1.0.0)
├── README.md                            — what zugot is, recipe format, categories
├── CHANGELOG.md                         — every change, grouped by category
├── CLAUDE.md                            — this file (AI-agent instructions)
├── LICENSE                              — GPL-3.0-only
├── CONTRIBUTING.md                      — contributor guide
├── SECURITY.md                          — security reporting
├── noted-issues-bazaar-finds.md         — bazaar cross-reference audit
│
├── build-order.txt                      — 225-package dependency-sorted sequence
│
├── base/                                — 163 recipes (LFS toolchain + kernel + core libs + build tools + auth + crypto + ...)
├── desktops/                            — 196 recipes (Wayland, PipeWire, GPU, fonts, apps, toolkits, Hyprland stack, ...)
├── marketplace/                         — 111 recipes (AGNOS-native MacCracken/* packages)
├── ai/                                  —  31 recipes (CUDA, ONNX, PyTorch, container runtimes)
├── edge/                                —  31 recipes (fleet, IoT, minimal profile)
├── network/                             —  10 recipes (nftables, iproute2, wireless, VPN)
├── browser/                             —   8 recipes (Firefox, Chromium, Brave, variants)
├── python/                              —   4 recipes (python3.12, 3.13, 3.13t, 3.14)
├── database/                            —   3 recipes (postgresql17, redis7, pgvector)
├── sandbox/                             —   3 recipes (local AGNOS sandbox images)
├── bazaar/                              —   community recipes (via separate repo; cross-checked)
│
├── scripts/
│   └── validate_recipes.py              — parse + filename-match + SHA + dep-resolution checks
│
├── .github/workflows/
│   └── validate-recipes.yml             — CI workflow: validator runs on every push/PR
│
└── docs/
    ├── adr/                             — Architecture Decision Records
    ├── audit/                           — dated security/CVE audit reports
    └── development/
        └── roadmap.md                   — current open work items, P1/P2/P3 tracked
```

## CHANGELOG Format

Follow [Keep a Changelog](https://keepachangelog.com/). Group changes by category (base, desktops, marketplace, etc.). Note version bumps with old → new. Include SHA256 status (verified/placeholder).

## Validator

Every PR must pass `scripts/validate_recipes.py`:
1. TOML/CYML parse errors (stdlib `tomllib`)
2. Filename ≠ `[package].name` mismatches
3. Empty `sha256` without a `# TODO` comment
4. Unresolved `[depends].runtime` / `[depends].build`

Usage: `scripts/validate_recipes.py` (zugot-only) or `scripts/validate_recipes.py --check-against ../bazaar` (cross-check).

CI wired in `.github/workflows/validate-recipes.yml`.
