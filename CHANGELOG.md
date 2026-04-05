# Changelog

All notable changes to zugot will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/).

## [0.1.0] - 2026-04-05

### Added

- Migrated all recipes from agnosticos/recipes/:
  - base: 116 recipes (LFS toolchain, kernel, core libs)
  - desktop: 112 recipes (Wayland, PipeWire, GPU, fonts, apps)
  - marketplace: 109 recipes (AGNOS crates + consumer apps)
  - ai: 25 recipes (CUDA, ONNX, PyTorch, whisper, llama.cpp)
  - edge: 31 recipes (fleet, IoT, minimal profile)
  - network: 9 recipes (nftables, iproute2, wireless)
  - browser: 8 recipes (Firefox ESR, Chromium, Zen, Falkon)
  - python: 4 recipes
  - database: 3 recipes
  - sandbox: 3 recipes
  - synapse.toml (root-level LLM management recipe)
- Migrated build-order.txt (224 packages in dependency order)

### Added (post-migration)

- marketplace/cyrius.toml — Cyrius self-hosting systems language and compiler toolchain (v0.1.0, pre-release)
- marketplace/agnos-kernel.toml — AGNOS sovereign kernel written in Cyrius (v0.9.0, pre-release)

### Fixed (P-1 Recipe Hardening)

#### License audit — 139 recipes fixed
- Added missing SPDX `-only` suffix to bare GPL/LGPL identifiers across all categories
- base/bzip2.toml: `BSD` -> `BSD-3-Clause` (invalid SPDX identifier)
- base/intel-ucode.toml: `Intel` -> `LicenseRef-Intel` (non-standard SPDX)

#### Structural fixes — 94 recipes fixed
- marketplace: Moved `install` block from `[security]` to `[build]` in 93 recipes (TOML parser would silently misplace the install step)
- edge/secureyeoman-edge.toml: Same `install` block fix

#### Field completeness — 60 recipes fixed
- Added missing `release = 1` and `arch = "x86_64"` to 60 recipes (4 base, 56 desktop)

#### synapse.toml structural fix
- Added missing `[package]` table header
- Added missing `[security]` section with standard hardening flags

#### Browser hardening — 4 recipes fixed
- firefox.toml, falkon.toml, midori.toml, zen.toml: `relro` -> `fullrelro`, added `bindnow`

#### SHA256 placeholders — 2 recipes fixed
- browser/chromium.toml: `sha256 = "VERIFY"` -> `sha256 = ""` with `# TODO` comment
- browser/firefox.toml: same fix

#### Header comment fixes — 3 recipes
- marketplace/murti.toml, salai.toml, tanur.toml: `Scaffolded` -> `Released` status

#### Other fixes
- marketplace/sutra-community.toml: Added missing `build = []` in `[depends]`

### Known Issues (flagged for review)

#### build-order.txt
- Actual line count is 224, not 309 as README states
- base/bazaar not listed (not toolchain — possible oversight)
- Three packages duplicated across base/ and desktop/: dbus, linux-pam, eudev
- Dependency ordering concerns: zstd before lz4, gawk before mpfr, coreutils before gmp

#### Recipes needing attention
- marketplace/stiva.toml: Uses `GPL-3.0-or-later` (all others use `-only` — verify intent)
- marketplace/sutra-community.toml: Empty `hardening = []` (noarch module pack — may be correct)
- edge/dbus.toml: License `AFL-2.1` — D-Bus is dual-licensed AFL-2.1 OR GPL-2.0-or-later
