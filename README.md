# Zugot

**Zugot** (Hebrew: זוּגוֹת — pairs) — Recipe repository for AGNOS.
Current release: **1.0.0** (2026-04-17) — see [CHANGELOG.md](./CHANGELOG.md).

Named after the paired creatures that entered the ark. Each recipe is a *zug* — a matched pair of definition and source that [ark](https://github.com/MacCracken/ark) carries to build the system. Without zugot, ark is an empty vessel.

## What Zugot Is

Zugot is the package database for AGNOS. Every package that can be built or installed — from the C library to the desktop compositor to the science crates — has a recipe here. Recipes are CYML files (Cyrius Markup Language — TOML syntax, `.cyml` extension) that define what to download, how to build it, what it depends on, and how to harden it.

**1.0.0 ships 561 recipes** across 10 categories with a validator, CI, a dated CVE audit process, and documented naming conventions.

Zugot is consumed by:
- **[ark](https://github.com/MacCracken/ark)** — the package manager (installs from recipes)
- **[nous](https://github.com/MacCracken/nous)** — the resolver (reads dependency graphs from recipes)
- **[takumi](https://github.com/MacCracken/takumi)** — the build system (executes build steps from recipes)

## Structure

```
zugot/
├── VERSION                       — 1.0.0
├── base/                         — 163 recipes (toolchain, kernel, core libs, build tools, crypto, auth)
├── desktops/                     — 196 recipes (Wayland, GTK/Qt, fonts, A/V codecs, Hyprland, XFCE, X11 libs)
├── marketplace/                  — 111 recipes (AGNOS-native MacCracken/* packages)
├── ai/                           —  31 recipes (CUDA, ONNX, PyTorch, container runtimes)
├── edge/                         —  31 recipes (fleet, IoT, minimal profile)
├── network/                      —  10 recipes (nftables, iproute2, wireless, VPN)
├── browser/                      —   8 recipes (Firefox, Chromium, Brave, LibreWolf, Zen, Vivaldi, Midori, Falkon)
├── python/                       —   4 recipes (cpython 3.12, 3.13, 3.13t, 3.14)
├── database/                     —   3 recipes (postgresql17, redis7, pgvector)
├── sandbox/                      —   3 recipes (AGNOS sandbox images)
├── bazaar/                       — community recipes (cross-referenced via separate repo)
│
├── build-order.txt               — 225 packages in dependency order (base + desktops)
│
├── scripts/validate_recipes.py   — recipe validator (parse, naming, SHA, dep resolution)
├── .github/workflows/            — CI (validate-recipes runs on every push/PR)
│
└── docs/
    ├── adr/                      — Architecture Decision Records
    ├── audit/                    — dated security/CVE audit reports
    └── development/
        └── roadmap.md            — active work items (P1/P2/P3)
```

## Recipe Format

Every recipe is a `.cyml` file (TOML syntax, parsed by Cyrius's CYML parser) with these sections:

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
| **base** | 163 | GCC 15.2, Rust 1.95, Linux 6.6.134 LTS, glibc 2.43, crypto, auth, build tools, compression, archive, init |
| **desktops** | 196 | Mesa, Wayland, PipeWire, GTK3/4, Qt6 stack, X11 libs, A/V codecs, Hyprland support, XFCE, fonts |
| **marketplace** | 111 | AGNOS-native `MacCracken/*` packages (cyrius, agnos-kernel, ifran, etc.) |
| **ai** | 31 | CUDA, ONNX, PyTorch, whisper.cpp, llama.cpp, vllm, container runtimes (containerd, runc, fuse-overlayfs) |
| **edge** | 31 | Minimal profile, fleet agents, ESP32, IoT, hardened kernel |
| **network** | 10 | nftables, iproute2, iptables, wireless tools, dhcpcd, OpenSSH, rsync |
| **browser** | 8 | Firefox, Chromium, Brave, LibreWolf, Zen, Vivaldi, Midori, Falkon |
| **python** | 4 | cpython 3.12, 3.13, 3.13t (free-threaded), 3.14 |
| **database** | 3 | postgresql17, redis7, pgvector |
| **sandbox** | 3 | Hardened AGNOS sandbox images (sy-agnos family) |

Total: **561 recipes** as of 1.0.0.

## Naming Conventions

Zugot's package names are Linux-distribution-agnostic. See [CLAUDE.md §Naming Conventions](./CLAUDE.md) for the full list. Short version:

- No `-dev` split — headers ship with the runtime package
- `python` (not `python3`), `pkgconf` (not `pkg-config`), `nodejs` (not `npm` or `nodejs-dev`)
- `"desktops"` (plural) in `groups = [...]`
- `linux-pam` (not `pam`), `x264` (not `libx264`)
- PyPI packages don't get zugot recipes; apps use `python -m pip install` in a virtualenv

Bazaar contributors should cross-check against the zugot naming rules above (and CLAUDE.md §Naming Conventions).

## Build Order

`build-order.txt` contains 225 packages in dependency-sorted order for building the complete base + desktops system from source. This is the self-hosting critical path — AGNOS builds AGNOS using these recipes in this order.

## Recipe Rules

Every recipe change requires a full field audit ([feedback_recipe_audit](https://github.com/MacCracken/agnosticos/blob/main/docs/development/applications/first-party-standards.md)):

- **version** must match the actual upstream or repo version
- **sha256** must be populated from the release tarball (empty = not yet released, requires `# TODO` comment)
- **license** must use SPDX `-only` suffix (`GPL-3.0-only`, not `GPL-3.0`)
- **depends** must list all runtime and build dependencies
- **security.hardening** must include appropriate flags
- **marketplace.min_agnos_version** must be current
- Every dep must resolve to a recipe in zugot (or bazaar if cross-checked) — enforced by `scripts/validate_recipes.py`

## Validation

Run the validator before any PR:

```sh
./scripts/validate_recipes.py                            # zugot-only
./scripts/validate_recipes.py --check-against ../bazaar  # cross-check bazaar deps
```

CI (`.github/workflows/validate-recipes.yml`) runs this on every push/PR. The validator catches: TOML/CYML parse errors, filename ↔ `[package].name` mismatches, empty SHAs without `# TODO` comments, and unresolved dependencies.

## Security

Dated CVE audits live in [`docs/audit/`](./docs/audit/). Current report: [`2026-04-17.md`](./docs/audit/2026-04-17.md). Active monitoring items are tracked in [`docs/development/roadmap.md`](./docs/development/roadmap.md).

Report vulnerabilities per [`SECURITY.md`](./SECURITY.md).

## Licensing

Recipes in zugot are GPL-3.0-only (the build instructions themselves). Third-party packages built by recipes retain their upstream licenses as specified in each recipe's `license` field (SPDX identifier).

## Related

- [ark](https://github.com/MacCracken/ark) — Package manager (the vessel that carries the zugot)
- [nous](https://github.com/MacCracken/nous) — Package resolver (reads dependency graphs from recipes)
- [takumi](https://github.com/MacCracken/takumi) — Build system (executes build steps from recipes)
- [mela](https://github.com/MacCracken/mela) — Marketplace (discovers and distributes packages)
- [sigil](https://github.com/MacCracken/sigil) — Trust verification (signs built packages)
- [bazaar](https://github.com/MacCracken/bazaar) — Community recipe overlay (cross-checked against zugot)
- [AGNOS Philosophy](https://github.com/MacCracken/agnosticos/blob/main/docs/philosophy.md) — Why zugot is named after the pairs that entered the ark

## Contributing

See [CONTRIBUTING.md](./CONTRIBUTING.md). Contributor quick path:
1. Pick a category and copy the closest existing recipe as a template
2. Fill every field (SHA256 can be empty with a `# TODO` comment for unreleased packages)
3. Run `./scripts/validate_recipes.py` — must pass before PR
4. Update `build-order.txt` if adding a base/desktops package
5. Add a CHANGELOG entry

## License

GPL-3.0-only
