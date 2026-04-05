# Zugot — Claude Code Instructions

## Project Identity

**Zugot** (Hebrew: זוּגוֹת — pairs, as in the paired creatures that entered the ark) — Recipe repository for AGNOS

- **Type**: Recipe database (TOML files, not a Rust crate)
- **License**: GPL-3.0-only
- **Version**: 0.1.0
- **Genesis repo**: [agnosticos](https://github.com/MacCracken/agnosticos)
- **Philosophy**: [AGNOS Philosophy & Intention](https://github.com/MacCracken/agnosticos/blob/main/docs/philosophy.md)
- **Standards**: [First-Party Standards](https://github.com/MacCracken/agnosticos/blob/main/docs/development/applications/first-party-standards.md)

## Consumers

- **[ark](https://github.com/MacCracken/ark)** — package manager (installs from recipes)
- **[nous](https://github.com/MacCracken/nous)** — resolver (reads dependency graphs from recipes)
- **[takumi](https://github.com/MacCracken/takumi)** — build system (executes build steps from recipes)
- **[mela](https://github.com/MacCracken/mela)** — marketplace (distributes marketplace packages)

## Development Process

### Recipe Work

Every recipe change requires a full field audit — never just bump a version.

1. Verify: name, version, SHA256, license (`-only` suffix), tags, build commands, `min_agnos_version`, dependencies
2. Cross-check version against crates.io, GitHub release tags, or upstream release
3. Verify SHA256 against actual release tarball
4. Confirm license matches the actual repo LICENSE file
5. Confirm dependencies are complete (runtime and build)
6. Confirm security hardening flags are appropriate
7. Test with `takumi validate` if available

### Adding a New Recipe

1. Determine category (base, desktop, marketplace, ai, edge, network, browser, python, database, sandbox)
2. Copy the closest existing recipe as a template
3. Fill all fields — no empty fields except SHA256 for unreleased packages
4. Verify build steps actually work
5. Add to `build-order.txt` if it's a base/desktop package (respect dependency ordering)

### Version Bumps

1. Update `version` field
2. Update `[source]` URL and SHA256
3. Update header comment version references
4. Check if any install script comments reference the old version
5. Verify dependencies haven't changed upstream
6. Test build if possible

## DO NOT

- **Do not commit or push** — the user handles all git operations
- **NEVER use `gh` CLI** — use `curl` to GitHub API only
- Do not add recipes with dummy SHA256 without a `# TODO` comment
- Do not change license fields without verifying against the actual repo
- Do not reorder `build-order.txt` without understanding the full dependency chain

## Structure

```
zugot/
├── base/              — 116 recipes (LFS toolchain, kernel, core libs)
├── desktop/           — 71 recipes (Wayland, PipeWire, GPU, fonts)
├── marketplace/       — 109 recipes (AGNOS crates + consumer apps)
├── ai/                — 25 recipes (CUDA, ONNX, PyTorch)
├── edge/              — 31 recipes (fleet, IoT, minimal)
├── network/           — 9 recipes (nftables, iproute2)
├── browser/           — 8 recipes (Firefox ESR, Chromium)
├── python/            — 4 recipes
├── database/          — 3 recipes
├── sandbox/           — 3 recipes
├── bazaar/            — community recipes (planned)
├── build-order.txt    — dependency-sorted build sequence
├── README.md
├── CHANGELOG.md
├── LICENSE
└── CLAUDE.md
```

## CHANGELOG Format

Follow [Keep a Changelog](https://keepachangelog.com/). Group changes by category (base, desktop, marketplace, etc.). Note version bumps with old → new.
