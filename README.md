# Zugot

**Zugot** (Hebrew: זוּגוֹת — pairs) — Recipe repository for AGNOS.

Named after the paired creatures that entered the ark. Each recipe is a *zug* — a matched pair of definition and source that [ark](https://github.com/MacCracken/ark) carries to build the system. Without zugot, ark is an empty vessel.

## What Zugot Is

Zugot is the package database for AGNOS. Every package that can be built or installed — from the C library to the desktop compositor to the science crates — has a recipe here. Recipes are TOML files that define what to download, how to build it, what it depends on, and how to harden it.

Zugot is consumed by:
- **[ark](https://github.com/MacCracken/ark)** — the package manager (installs from recipes)
- **[nous](https://github.com/MacCracken/nous)** — the resolver (reads dependency graphs from recipes)
- **[takumi](https://github.com/MacCracken/takumi)** — the build system (executes build steps from recipes)

## Structure

```
zugot/
├── base/              — 116 recipes (toolchain, kernel, core libs — LFS Ch. 5-8)
├── desktop/           — 112 recipes (Wayland, PipeWire, GPU, fonts, themes, apps)
├── marketplace/       — 111 recipes (AGNOS crates + consumer apps)
├── ai/                — 25 recipes (CUDA, ONNX, PyTorch, whisper, llama.cpp)
├── edge/              — 31 recipes (fleet management, IoT, minimal profile)
├── network/           — 9 recipes (nftables, iproute2, wireless)
├── browser/           — 8 recipes (Firefox ESR, Chromium)
├── python/            — 4 recipes (Python runtime)
├── database/          — 3 recipes (database systems)
├── sandbox/           — 3 recipes (sandbox/container recipes)
├── build-order.txt    — 225 packages in dependency order (base + desktop)
└── bazaar/            — community-contributed recipes (planned)
```

## Recipe Format

Every recipe is a TOML file with these sections:

```toml
[package]
name = "example"
version = "1.0.0"
description = "Example — one-line description"
license = "GPL-3.0-only"
groups = ["category", "tags"]
release = 1
arch = "x86_64"            # or "any" for pure Rust/noarch

[source]
# For upstream open-source packages:
url = "https://example.org/releases/example-1.0.0.tar.gz"
sha256 = "abc123..."
patches = []

# For AGNOS-native packages:
github_release = "MacCracken/example"
release_asset = "example-*-linux-amd64.tar.gz"
sha256 = ""                 # Populate from release tarball

[depends]
runtime = ["glibc", "openssl"]
build = ["gcc", "make"]     # or ["rust"] for Rust crates

[build]
strip = true
install_docs = false
pre_build = ""
configure = "./configure --prefix=/usr"
make = "make -j$(nproc)"
check = "make check"
install = "make DESTDIR=$PKG install"
post_install = ""

[security]
hardening = ["pie", "fullrelro", "fortify", "stackprotector", "bindnow"]
cflags = "-O2 -pipe"
ldflags = "-Wl,--as-needed"

# For marketplace packages only:
[marketplace]
category = "library"
runtime = "rust-crate"      # or "native-binary"
publisher = "AGNOS"
tags = ["relevant", "tags"]
min_agnos_version = "2026.3.31"

[marketplace.sandbox]
seccomp_mode = "basic"
network_access = false
```

## Recipe Categories

| Category | Count | Description |
|----------|-------|-------------|
| **base** | 116 | GCC 15.2, Rust 1.89, Linux 6.6.72, glibc 2.42, full LFS toolchain |
| **desktop** | 112 | Mesa, PipeWire, Wayland, foot, helix, mpv, GTK, Qt |
| **marketplace** | 111 | AGNOS library crates, consumer apps, OS subsystems, cyrius, agnos-kernel |
| **ai** | 25 | CUDA, ONNX, PyTorch, whisper.cpp, llama.cpp, vllm |
| **edge** | 31 | Minimal profile, fleet agents, ESP32, IoT |
| **network** | 9 | nftables, iproute2, wireless tools |
| **browser** | 8 | Firefox ESR, Chromium |
| **python** | 4 | Python runtime and pip |
| **database** | 3 | Database engines |
| **sandbox** | 3 | Container/sandbox recipes |

## Build Order

`build-order.txt` contains 225 packages in dependency-sorted order for building the complete base + desktop system from source. This is the self-hosting critical path — AGNOS builds AGNOS using these recipes in this order.

## Recipe Rules

Every recipe change requires a full field audit ([feedback_recipe_audit](https://github.com/MacCracken/agnosticos/blob/main/docs/development/applications/first-party-standards.md)):

- **version** must match the actual upstream or repo version
- **sha256** must be populated from the release tarball (empty = not yet released)
- **license** must use SPDX `-only` suffix (`GPL-3.0-only`, not `GPL-3.0`)
- **depends** must list all runtime and build dependencies
- **security.hardening** must include appropriate flags
- **marketplace.min_agnos_version** must be current

## Licensing

All recipes in zugot define how to build GPL-3.0-only packages. The recipes themselves are GPL-3.0-only. Third-party packages (base/, desktop/, browser/) retain their upstream licenses as specified in each recipe's `license` field.

## Related

- [ark](https://github.com/MacCracken/ark) — Package manager (the vessel that carries the zugot)
- [nous](https://github.com/MacCracken/nous) — Package resolver (reads dependency graphs from recipes)
- [takumi](https://github.com/MacCracken/takumi) — Build system (executes build steps from recipes)
- [mela](https://github.com/MacCracken/mela) — Marketplace (discovers and distributes packages)
- [sigil](https://github.com/MacCracken/sigil) — Trust verification (signs built packages)
- [AGNOS Philosophy](https://github.com/MacCracken/agnosticos/blob/main/docs/philosophy.md) — Why zugot is named after the pairs that entered the ark

## License

GPL-3.0-only
