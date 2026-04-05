# Zugot — Claude Code Instructions

## Project Identity

**Zugot** (Hebrew: זוּגוֹת — pairs, as in the paired creatures that entered the ark) — Recipe repository for AGNOS

- **Type**: Recipe database (TOML files, not a Rust crate)
- **License**: GPL-3.0-only
- **Version**: 0.1.0
- **Genesis repo**: [agnosticos](https://github.com/MacCracken/agnosticos)
- **Philosophy**: [AGNOS Philosophy & Intention](https://github.com/MacCracken/agnosticos/blob/main/docs/philosophy.md)
- **Standards**: [First-Party Standards](https://github.com/MacCracken/agnosticos/blob/main/docs/development/applications/first-party-standards.md)

## What This Is

Zugot is the package database for AGNOS. Every package that can be built or installed — from the C library to the desktop compositor to the science crates — has a recipe here. Recipes are TOML files consumed by ark (package manager), nous (resolver), and takumi (build system).

Zugot is NOT a Rust crate. There is no Cargo.toml, no src/ directory, no compilation. The "code" is TOML recipe files. The quality gates are validation scripts, not cargo clippy.

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
7. **Build order validation** — if touching base/desktop recipes, verify `build-order.txt` is correct and complete
8. **Structural audit** — verify install blocks are in the correct TOML section (`[build]` not `[security]`), no duplicate fields, no stale references
9. **Documentation** — update CHANGELOG with all findings and fixes

### Work Loop (continuous)

1. **Work phase** — new recipes, version bumps, category additions, upstream sync
2. **Validation** — run `takumi validate` or equivalent on all changed recipes
3. **Cross-check** — verify versions against upstream (crates.io, GitHub, project sites)
4. **SHA256** — download actual tarballs and compute SHA256 for any new or bumped recipes
5. **Dependency check** — verify all runtime and build deps are listed and current
6. **Build order** — if base/desktop recipe changed, verify `build-order.txt` is still correct
7. **Review** — check for stale comments, wrong license suffixes, missing fields
8. **If heavy changes → return to step 2** — keep validating until clean
9. **Documentation** — update CHANGELOG with changes. Group by category. Note version bumps with old → new. Update roadmap if applicable
10. Return to step 1

### Task Sizing

- **Low/Medium effort** (single recipe bump, new marketplace recipe): Batch freely — multiple recipes per work loop cycle
- **Large effort** (base system version bump, new category, build-order changes): Small bites only — one recipe at a time, verify each before moving to the next. Base system recipes affect everything downstream
- **If unsure**: Treat it as large. A wrong base recipe breaks the entire build

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

1. Determine category (base, desktop, marketplace, ai, edge, network, browser, python, database, sandbox, bazaar)
2. Copy the closest existing recipe as a template
3. Fill ALL fields — no empty fields except SHA256 for unreleased packages (must have `# TODO` comment)
4. Verify build steps actually work
5. Add to `build-order.txt` if it's a base/desktop package (respect dependency ordering)
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
├── base/              — 116 recipes (LFS toolchain, kernel, core libs)
├── desktop/           — 112 recipes (Wayland, PipeWire, GPU, fonts, apps)
├── marketplace/       — 111 recipes (AGNOS crates + consumer apps)
├── ai/                — 25 recipes (CUDA, ONNX, PyTorch)
├── edge/              — 31 recipes (fleet, IoT, minimal)
├── network/           — 9 recipes (nftables, iproute2)
├── browser/           — 8 recipes (Firefox ESR, Chromium)
├── python/            — 4 recipes
├── database/          — 3 recipes
├── sandbox/           — 3 recipes
├── bazaar/            — community recipes (planned)
├── build-order.txt    — dependency-sorted build sequence
├── README.md          — what zugot is, recipe format, category descriptions
├── CHANGELOG.md       — every change, grouped by category
├── LICENSE            — GPL-3.0-only
└── CLAUDE.md          — this file
```

## CHANGELOG Format

Follow [Keep a Changelog](https://keepachangelog.com/). Group changes by category (base, desktop, marketplace, etc.). Note version bumps with old → new. Include SHA256 status (verified/placeholder).
