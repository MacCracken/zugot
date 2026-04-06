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

### Version Bumps

#### Security-critical (base)
- openssh: 10.2p1 → 10.3p1 (shell injection fix)
- xz: 5.8.2 → 5.8.3 (CVE buffer overflow fix)
- zlib: 1.3.1 → 1.3.2 (security audit fixes)
- linux: 6.6.130 → 6.6.132 (LTS point release)

#### Base
- binutils: 2.45 → 2.46
- glibc: 2.42 → 2.43
- gnupg: 2.4.8 → 2.4.9
- grub: 2.12 → 2.14
- gawk: 5.3.2 → 5.4.0
- perl: 5.42.1 → 5.42.2
- pkgconf: 2.5.1 → 3.0.0
- shadow: 4.19.0 → 4.19.4

#### Desktop
- mesa: 26.0.3 → 26.0.4
- wayland: 1.24.0 → 1.25.0
- wayland-protocols: 1.47 → 1.48
- pipewire: 1.4.11 → 1.6.2
- harfbuzz: 13.2.1 → 14.0.0
- fontconfig: 2.16.0 → 2.17.1
- gtk3: 3.24.43 → 3.24.52
- vulkan-loader: 1.4.341 → 1.4.348
- poppler: 26.03.0 → 26.04.0

#### Network
- openssh: 10.0p1 → 10.3p1 (security fix)
- ca-certificates: 2025.12 → 2026.03
- iw: 6.9 → 6.17
- libnl: 3.11.0 → 3.12.0

#### Desktop (continued)
- ffmpeg: 7.1.1 → 8.1 (major version bump)

#### Browser
- firefox: 140.9.0 → 149.0 (switched from ESR to standard release)
- chromium: 146.0.7680.169 → 147.0.7727.49 (SHA256 TODO — tarball too large)
- brave: 1.90.79 → 1.91.9
- zen: 1.19.5b → 1.19.6b
- falkon: 24.12.3 → 25.12.3
- midori: 11.5.1 → 11.6.4

#### AI
- llama-cpp: b8579 → b8664
- ollama: 0.18.3 → 0.20.2
- vllm: 0.18.0 → 0.19.0
- rocm: 6.4.0 → 7.2.1
- python-pandas: 3.0.1 → 3.0.2
- python-safetensors: 0.5.3 → 0.7.0
- python-transformers: 5.4.0 → 5.5.0
- huggingface-hub-cli: 1.8.0 → 1.9.0
- jupyter-server: 2.15.0 → 2.17.0
- vulkan-compute-tools: 1.4.309 → 1.4.341
- cni-plugins: 1.6.2 → 1.9.1
- conmon: 2.1.12 → 2.2.1
- crun: 1.20 → 1.22
- slirp4netns: 1.3.1 → 1.3.3

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
