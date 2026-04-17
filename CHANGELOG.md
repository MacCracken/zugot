# Changelog

All notable changes to zugot will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/).

## [Unreleased]

### Straggler SHA Population (2026-04-17)

- **`base/gn.cyml`** — pinned to commit `ab5eb178` (main-branch head 2026-04-17); version field `20260417-ab5eb178`. SHA256 verified (`5fbe3e56...`). googlesource archive endpoint requires `Accept: application/x-gzip` header; documented in recipe comment.
- **`browser/chromium.cyml`** — SHA256 populated (`8430437c...`). 5.3GB tarball fetched + hashed in one pass (~3.5 min on this host); the prior "too large" note overstated the difficulty. No bug, but now reproducible by default.

### Directory rename (2026-04-17) — `desktop/` → `desktops/`

Completing the plural-pluralisation initiated in the groups-field rename:
- Moved 176 recipe files via `git mv desktop/ desktops/` (history preserved)
- `build-order.txt` path entries updated (70 `desktop/X` → `desktops/X`)
- `README.md` tree diagram + category table
- `CLAUDE.md` tree diagram
- `docs/development/roadmap.md` all recipe path references

Downstream consumers that hardcode the recipe directory path must update to `desktops/`.

### Validator Closure (2026-04-17) — 151 → 0 unresolved

Full sweep of issues surfaced by `scripts/validate_recipes.py`. Validator now reports **`OK: all recipes validate clean`**.

#### Mass renames (convention fixes)
- `python3` → `python` across 21 recipes
- `libpipewire` → `pipewire` across 9 recipes
- All `-dev` suffixes stripped from deps (openssl-dev, zlib-dev, pam-dev, sqlite-dev, wayland-dev, postgresql-dev, etc.)
- `pam` → `linux-pam`; `freetype2` → `freetype`; `postgresql`/`postgresql-dev` → `postgresql17`; `systemd-libs` → `elogind`

#### New recipes — 30 added

Build tools: `brotli` 1.2.0, `c-ares` 1.34.6, `docbook-xsl` 1.79.2, `gyp` 0.22.0, `gn` 20260410, `autoconf2.13`, `squashfs-tools` 4.7.5, `bun` 1.3.12, `ruby` 3.4.9

Libraries: `libpsl` 0.21.5, `libyaml` 0.2.5, `mimalloc` 3.3.0, `parted` 1.9.0, `cbindgen` 0.29.2, `at-spi2-core` 2.60.0, `dbus-glib` 0.100.2, `libgtop` 2.41.3, `libsoup` 3.6.6, `libxmlb` 0.3.26, `libxdamage` 1.1.7, `libxcomposite` 0.4.7, `webkit2gtk-4.1` 2.52.3, `extra-cmake-modules` 6.25.0

Meta-package aliases (depend on canonical package, zero build): `clang` → llvm, `lld` → llvm, `gfortran` → gcc, `libuuid` → util-linux, `libltdl` → libtool, `libgbm` → mesa, `libseat` → seatd, `pipewire-jack` → pipewire

#### Filename/package-name mismatches fixed

Renames via `git mv`:
- `python/cpython-3.12.cyml` → `python3.12.cyml` (+ 3.13, 3.13-freethreaded→3.13t, 3.14)
- `database/pgvector-0.8.cyml` → `pgvector.cyml`
- `database/postgresql-17.cyml` → `postgresql17.cyml`
- `database/redis-7.cyml` → `redis7.cyml`
- `edge/kernel.cyml` → `kernel-edge.cyml`

Package-name edits (filename kept):
- `desktop/libsigcpp.cyml` — package renamed `libsigc++` → `libsigcpp`
- `browser/zen.cyml` — package renamed `zen-browser` → `zen`

### P3 Roadmap — Tooling (2026-04-17)

- **`scripts/validate_recipes.py`** — new. Parses every `*.cyml` via stdlib `tomllib` and reports:
  1. TOML/CYML parse errors (also catches the class of lax-parser-accepts-but-strict-parser-fails issues like `\.` inside `"""..."""`)
  2. Filename ≠ `[package].name` mismatches
  3. Empty `sha256` without a `# TODO` comment
  4. Unresolved `[depends].runtime` / `[depends].build` entries

  Supports `--check-against <path>` for cross-checking bazaar against zugot. First run against the current tree surfaced 151 legitimate issues (mostly `python3→python` renames never applied to `ai/*.cyml`; a handful of missing recipes: gfortran, docbook-xsl, brotli, c-ares, gyp) — enumerated in roadmap under "Follow-ups surfaced by the validator".

- **`.github/workflows/validate-recipes.yml`** — new. Runs the validator on every push to `main` and every PR.

### P2 Roadmap — Upstream Transitions (2026-04-17)

Four recipes needed coordinated updates for upstream changes:

- **`base/libcap-ng.cyml`** 0.8.5 → **0.9.3**. Switched source from `people.redhat.com` (stuck at 0.8.5) to GitHub archive (`stevegrubb/libcap-ng`). Added `autogen.sh` in pre_build and `autoconf`/`automake`/`libtool` to build deps since GitHub tarballs ship without pre-generated `configure`. SHA256 verified (`fe11ebbb...`).
- **`desktop/nvidia-driver.cyml`** 570.133.07 → **595.58.03** (production stable channel). SHA256 verified from download.nvidia.com (423MB .run installer).
- **`desktop/zathura.cyml`** 0.5.14 → **2026.03.27**. Upstream switched from semver to date-based versioning; URL and version updated. SHA256 verified.
- **`desktop/girara.cyml`** 0.4.5 → **2026.02.04**. Same date-based versioning transition. SHA256 verified.

### P1 Roadmap Items Resolved (2026-04-17)

First pass through the P1 items in `docs/development/roadmap.md`:

#### `base/cyrius.cyml` — rewritten (0.9.0 → 5.2.0)
Switched from the stale `release_asset = "cc2"` pattern to a direct `url` pointing at the pre-built `cyrius-5.2.0-x86_64-linux.tar.gz` release tarball. Install now copies the full 5.x toolchain (`cc5`, `cyrius`, `cyrc`, `cyrfmt`, `cyrlint`, `cyrdoc`, `ark`, helper scripts, stdlib) from the tarball. SHA256 populated (`537da95c...`). Downstream build references to `cc2` updated to `cc5` in `kybernet` and `agnos-kernel`.

#### `base/kybernet.cyml` (0.9.0 → 1.0.1)
Switched from `release_asset = "kybernet-x86_64"` (pre-built binary) to building from `kybernet-1.0.1-src.tar.gz` via `cc5`. SHA256 populated (`f9c88e97...`).

#### `base/agnos-kernel.cyml` (1.0.0 → 1.22.0)
Clarified naming in header comment (upstream repo is `MacCracken/agnos`, recipe name `agnos-kernel` describes the kernel component). Switched to building from `agnos-1.22.0-src.tar.gz` via `cc5`. SHA256 populated (`177bf9e8...`).

#### `base/gvisor.cyml` — pinned (`latest` → `20260413.0`)
Replaced the rolling `/release/latest/` URL (SHA would silently drift) with pinned `/release/20260413/x86_64/runsc`. SHA256 updated to match pinned build (`c97966a7...`).

#### SHA population backlog
- `base/boost.cyml` — SHA256 populated (`9e6bee9a...`; tarball verified at 51MB)
- `desktop/luajit.cyml` — pinned to commit `18b087cd` (v2.1 branch snapshot), version field `2.1-18b087cd`, SHA256 populated (`88a592af...`)
- `browser/chromium.cyml` — still TODO (6GB tarball); noted in roadmap for dev-machine fetch before release build

### Version Bumps — Marketplace (39 AGNOS-native packages)

Marketplace audit against upstream `MacCracken/*` GitHub tags (`git ls-remote` after API rate-limit). All SHA256 values remain TODO per existing convention for unreleased `release_asset` bundles — SHAs get populated when consumers build against the actual release tarball.

#### Tier 1 (>1.0 major version bumps)
- abaco: 1.1.0 → 2.1.0
- ai-hwaccel: 1.0.0 → 2.0.0
- hoosh: 1.2.0 → 2.0.0
- itihas: 1.0.1 → 2.2.0
- hisab: 1.4.0 → 2.2.0
- majra: 1.0.4 → 2.2.0
- sankhya: 1.0.0 → 2.0.0
- shabda: 1.1.0 → 2.0.0
- shabdakosh: 1.1.0 → 2.0.0
- svara: 1.1.1 → 2.0.0
- t-ron: 0.90.0 → 2.0.0
- vidya: 1.0.0 → 2.1.0

#### Tier 2 (sub-1.0 → 1.x, big jumps)
- agnos-kernel: 1.0.0 → 1.22.0
- agnoshi: 0.90.0 → 1.0.0
- agnostik: 0.90.0 → 0.96.0
- agnosys: 0.51.0 → 0.97.2
- argonaut: 0.90.0 → 1.2.0
- ark: 0.1.0 → 0.8.0
- aethersafta: 0.25.3 → 0.50.0
- avatara: 1.0.1 → 2.3.0
- bote: 0.92.0 → 2.5.1
- cyrius: 0.1.0 → 5.2.0 (recipe massively stale; upstream now at 5.x)
- daimon: 0.6.0 → 1.1.1
- kiran: 0.26.3 → 1.0.0
- kybernet: 0.51.0 → 1.0.1
- nein: 0.90.0 → 1.0.0
- nous: 0.1.0 → 1.1.1
- phylax: 0.5.0 → 1.0.0
- ranga: 0.29.4 → 1.0.0
- selah: 0.29.4 → 2026.3.17
- sigil: 1.0.0 → 2.4.2
- szal: 1.0.1 → 1.1.0
- sharira: 1.0.0 → 1.1.0
- shravan: 1.0.1 → 2.3.2
- tarang: 0.21.3 → 2026.3.18
- yukti: 0.25.3 → 1.2.0

#### Tier 3 (point-release bumps)
- dhvani: 1.0.0 → 1.1.0
- ifran: 1.2.0 → 1.3.0
- rasa: 2026.3.18 → 2026.3.23

### Flagged — Recipe AHEAD of upstream (no action)
These have recipe versions newer than current upstream tags — likely pre-release staging:
- secureyeoman, secureyeoman-agent, secureyeoman-lite, secureyeoman-primary, secureyeoman-sqlite: recipe 2026.3.28 vs upstream 2026.3.19
- stiva: recipe 2.0.0 vs upstream 1.0.0

### Flagged — No upstream tags yet (no action)
22 recipes where `git ls-remote` returns no tags — repos may exist but haven't had a release cut. Left at current recipe versions:
abacus, aegis, aethersafha, agnova, cyrius-seed, jantu, jivanu, kavach, libro, mabda, mastishk, mela, mneme, muharrir, murti, nazar, salai, samay, seema, shakti, takumi, tanur

### Fixed (bazaar-finds pass 2)

Four recipes had unescaped backslashes in `"""..."""` basic strings. TOML only accepts `\b \t \n \r \" \\ \uXXXX \UXXXXXXXX` as escapes — sequences like `\.` and `\;` are parse errors. Cyrius's current CYML parser is lax enough to accept them, but strict TOML-compatible consumers (Python `tomllib`, Rust `toml` crate) fail. Converted the offending blocks to literal multi-line strings (`'''...'''`) which don't process escapes:
- `base/shadow.cyml` (pre_build block with `sed 's/...\.N ...'` patterns)
- `base/nss.cyml` (install block with `find ... -exec ... \;`)
- `desktop/noto-fonts.cyml` (install block, same `\;` pattern)
- `edge/kernel.cyml` (install block, same `\;` pattern)

### Added (meta-packages — bazaar-finds pass 2 closure)

Three thin alias recipes so bazaar deps `pkg-config`, `pip`, `npm` resolve without requiring bazaar contributors to learn zugot's canonical naming:
- `base/pkg-config.cyml` — alias for `pkgconf` (real implementation already creates /usr/bin/pkg-config symlink)
- `base/pip.cyml` (name `pip`) — alias for python's bundled pip; installs `/usr/bin/pip → pip3`
- `base/npm.cyml` (name `npm`) — alias for nodejs's bundled npm

Initial filenames were `python-pip.cyml`/`nodejs-npm.cyml` (flagged in pass 3 for filename/package-name mismatch) and renamed here to match the `[package].name` convention used by the rest of zugot.

### Added (pass 3 closure)

- `ai/pycups.cyml` 2.0.4 — Python CUPS bindings (was `NOT added` in pass 2 per CLAUDE.md rule 9; pass-3 rationale revisited — these are small C extensions with clean deps on `python + cups`, so ship them as first-party recipes instead of pushing bazaar to do `pip install` in build scripts)
- `ai/pycurl.cyml` 7.45.7 — Python libcurl bindings (same reasoning)

This closes bazaar's unresolved count to **0**.

### Added

#### Base (new build tools — addresses bazaar cross-ref audit)
- nasm 2.16.03 (x86 assembler — unblocks firefox, librewolf, zen in browser/ and ffmpeg downstream)
- intltool 0.51.0 (i18n for GNOME/XFCE — unblocks avahi in edge/ and 6 bazaar recipes)
- itstool 2.0.7 (XML translation — unblocks 4 bazaar recipes)
- desktop-file-utils 0.28 (unblocks 4 bazaar recipes)
- vala 0.56.19 (unblocks 3 bazaar recipes)

#### Desktop (new Qt 6 stack — unblocks falkon + bazaar Qt consumers)
- qt6-base 6.10.3 (core modules)
- qt6-declarative 6.10.3 (QML/Quick)
- qt6-wayland 6.10.3 (Wayland integration)
- qt6-tools 6.10.3 (Linguist/Designer)
- qt6-webengine 6.10.3 (Chromium-based web engine for falkon)
- All Qt SHA256 values taken from Qt's `.tar.xz.sha256` sidecar files published alongside each tarball.

#### Base (remaining priority 1 build tools — bazaar audit)
- swig 4.4.1, xmlto 0.0.29, mm-common 1.0.7, gnome-doc-utils 0.20.10 (EOL upstream), hyprwayland-scanner 0.4.5

#### Base (zugot-internal gap closers — runtimes/tools)
- git 2.53.0 (used by base/bazaar, marketplace/delta, + 4 bazaar recipes)
- nodejs 24.15.0 (LTS; bundles npm — used by brave, chromium, midori, open-webui)
- nspr 4.38.2 (dep of nss)
- nss 3.122.1 (used by firefox, chromium, brave, thunderbird)
- protobuf 34.1 (dep of ifran, onnxruntime)
- fuse 3.18.2 (libfuse 3 — dep of lmstudio, container runtimes)
- abseil-cpp 20260107.1 (dep of protobuf)
- yasm 1.3.0 (dep of libvpx; nasm preferred elsewhere)
- boost 1.90.0 (recipe scaffolded with SHA256 TODO — 110MB tarball not auto-downloaded)
- unzip 6.0, zip 3.0 (Info-ZIP — libreoffice build deps)
- tree 2.3.2 (pass dep)

#### Desktop (GTK/GNOME ecosystem — 15 recipes)
- libhandy 1.8.3, libsecret 0.21.7, libnma 1.10.6, libpwquality 1.4.5, libportal 0.9.1
- gtk-layer-shell 0.10.1, adwaita-icon-theme 50.0, appstream 1.1.2, iso-codes 4.20.1
- libsigc++ 3.6.0, glibmm 2.88.0, cairomm 1.19.0, pangomm 2.56.1, atkmm 2.36.3, gtkmm3 3.24.10

#### Desktop (transitive deps for new recipes)
- xcb-util 0.4.1, hicolor-icon-theme 0.18, cracklib 2.10.3, speexdsp 1.2.1, pugixml 1.15

#### Desktop (XFCE stack — 7 recipes)
- exo 4.20.0, xfconf 4.20.0, libxfce4util 4.20.1, libxfce4ui 4.20.2
- libice 1.1.2, libsm 1.2.6, startup-notification 0.12 (upstream frozen)

#### Desktop (Hyprland support — 6 recipes)
- tomlplusplus 3.4.0, sdbus-cpp 2.2.1, xcb-util-wm 0.4.2, aquamarine 0.10.0, hyprcursor 0.1.13, libzip 1.11.4

#### Desktop (audio/video/codecs — 10 recipes)
- x264 (stable snapshot — note: rolling tarball, re-verify SHA on each build)
- libvpx 1.16.0, opus 1.5.2, lame 3.100, libwebp 1.6.0, giflib 6.1.3
- mbedtls 4.1.0, jansson 2.15.0, wxwidgets 3.3.2, portaudio 19.7.0
- pulseaudio 17.0 (legacy — PipeWire preferred; kept for browser/brave/chromium/firefox compat)

#### Desktop (C/C++ system libraries — 18 recipes)
- seatd 0.9.2 (blocks sway/wlroots/hyprland), libevent 2.1.12, libsodium 1.0.22
- libxinerama 1.1.6, libxslt 1.1.45, hunspell 1.7.2, oniguruma 6.9.10, libuv 1.52.1
- tree-sitter 0.26.8, luajit (rolling v2.1 branch — SHA256 TODO), msgpack-c 6.1.0, unibilium 2.1.2
- fmt 12.1.0, spdlog 1.17.0, minizip 4.1.0, libxt 1.3.1, graphite2 1.3.14, hwdata 0.406, libdvdread 7.0.1

#### Desktop/app-specific libs (5 recipes)
- babl 0.1.126, gegl 0.4.70 (GIMP engine); gsl 2.8, gdl 3.40.0 (Inkscape deps)

#### AI/containers stack additions
- cython 3.2.4 (Python C extension compiler)
- containerd 2.2.3 (CRI runtime)
- runc 1.4.2 (OCI reference runtime — zugot's crun is a drop-in alternative)
- fuse-overlayfs 1.16 (rootless container OverlayFS)

#### Network (legacy compat)
- iptables 1.8.13 (kept alongside nftables for containers/VPN tools)

### Documentation
- CLAUDE.md: expanded "Naming Conventions" section. Added rules for `linux-pam` (not `pam`), `x264/x265` (not `libx264/libx265`), and PyPI-package-policy (don't create zugot recipes for pip-installable Python packages like `pycups`, `pycurl` — use `python -m pip` in app-level manifests). Cross-references `noted-issues-bazaar-finds.md`.

### Changed
- Recipe file format: `.toml` → `.cyml` (Cyrius Markup Language). All 426 recipe files renamed via `git mv`. Content unchanged — CYML parses TOML syntax for single-entry (no `---` delimiter) files. Downstream consumers (ark, nous, takumi, mela) must update readers to accept `.cyml`.
- Group name: `"desktop"` → `"desktops"` (plural) in 130 recipes' `groups = [...]` field. Wayland will not be the only desktop AGNOS ships long-term, so the namespace is pluralized. Applied only to `groups` field — `seccomp_mode = "desktop"`, `tags = [..., "desktop", ...]`, `boot_mode = ["desktop"]`, and descriptive text with "desktop" in it are preserved. Downstream consumers that filter by group tag must update to `"desktops"`.

### Version Bumps

#### Python
- python3.13: 3.13.12 → 3.13.13 (SHA256 verified from python.org tarball)
- python3.13t: 3.13.2 → 3.13.13 (freethreaded; was 10 patches behind; SHA256 verified)
- python3.14: 3.14.3 → 3.14.4 (SHA256 verified from python.org tarball)

#### Network
- dhcpcd: 10.3.0 → 10.3.1 (SHA256 verified from release tarball)

#### Base (security-critical)
- linux kernel: 6.6.132 → 6.6.134 (LTS point release, SHA256 verified; install paths updated)
- openssl: 3.5.5 → 3.5.6 (3.5.x LTS, SHA256 verified)

#### Base (interpreters/languages)
- python: 3.13.12 → 3.13.13 (SHA256 verified from python.org)
- rust: 1.94.1 → 1.95.0 (SHA256 verified from static.rust-lang.org stable channel)
- llvm: 22.1.2 → 22.1.3 (SHA256 verified from GitHub release)

#### Base (init/system tools)
- kbd: 2.8.0 → 2.9.0 (SHA256 verified)
- iwd: 3.5 → 3.12 (7 versions behind, SHA256 verified)

#### Base (common libraries)
- libcap: 2.77 → 2.78 (SHA256 verified)
- libxcrypt: 4.4.38 → 4.5.2 (SHA256 verified)
- libunistring: 1.3 → 1.4.2 (SHA256 verified)

#### Base (auth/security)
- linux-pam: 1.7.1 → 1.7.2 (SHA256 verified from GitHub release)

#### Base (small libraries)
- libnftnl: 1.2.8 → 1.3.1 (SHA256 verified from netfilter.org)
- libpng: 1.6.56 → 1.6.58 (SHA256 verified)
- gettext: 0.26 → 1.0 (major version bump — first 1.x release, SHA256 verified from ftp.gnu.org)

#### Base (shell/text tools)
- file: 5.46 → 5.47 (SHA256 verified)
- groff: 1.23.0 → 1.24.1 (SHA256 verified)
- man-pages: 6.15 → 6.17 (SHA256 verified)
- dropbear: 2025.88 → 2025.89 (SHA256 verified)
- elfutils: 0.194 → 0.195 (SHA256 verified)

#### Base (build tools — meson/ninja)
- meson: 1.10.2 → 1.11.0 (SHA256 verified)
- ninja: 1.13.1 → 1.13.2 (SHA256 verified)

#### Base (network/firewall)
- nftables: 1.1.1 → 1.1.6 (SHA256 verified; matches edge/nftables)

#### Base (kernel/firmware)
- amd-ucode: 20260309 → 20260410 (SHA256 verified from cdn.kernel.org)
- linux-firmware: 20260309 → 20260410 (SHA256 verified from cdn.kernel.org)
- linux-api-headers: 6.6.130 → 6.6.134 (matches linux kernel bump, SHA256 verified)
- dracut: 105 → 110 (dracut-ng, 5 releases behind, SHA256 verified)

#### Base (sandbox/runtime)
- firecracker: 1.15.0 → 1.15.1 (SHA256 verified)

#### Base (other)
- iana-etc: 20250807 → 20260409 (SHA256 verified)

#### Base (filesystem/storage)
- cryptsetup: 2.8.4 → 2.8.6 (2.8.x LTS, SHA256 verified)
- lvm2: 2.03.28 → 2.03.39 (11 patch releases behind, SHA256 verified)

#### Base (core utilities)
- coreutils: 9.7 → 9.10 (SHA256 verified)
- texinfo: 7.2 → 7.3 (SHA256 verified)
- which: 2.21 → 2.23 (SHA256 verified)

#### Base (build tools)
- m4: 1.4.20 → 1.4.21 (SHA256 verified)
- autoconf: 2.72 → 2.73 (SHA256 verified)

#### Base (compression/archive)
- libarchive: 3.8.6 → 3.8.7 (SHA256 verified from GitHub)

#### Base (crypto/trust stack)
- libgcrypt: 1.12.1 → 1.12.2 (SHA256 verified)
- libgpg-error: 1.51 → 1.59 (8 minor versions, SHA256 verified)
- libksba: 1.6.7 → 1.6.8 (SHA256 verified)
- libtasn1: 4.19.0 → 4.21.0 (SHA256 verified)
- nettle: 3.10.1 → 3.10.2 (3.10.x stable track, SHA256 verified)
- p11-kit: 0.25.5 → 0.26.2 (SHA256 verified)

#### Desktop (batch 4 — libs/apps)
- sqlite: 3.51.3 → 3.53.0 (autoconf-3510300 → 3530000, SHA256 verified)
- udisks: 2.10.1 → 2.11.1 (SHA256 verified)
- upower: 1.90.6 → 1.91.2 (SHA256 verified)
- wl-clipboard: 2.2.1 → 2.3.0 (SHA256 verified)
- xorgproto: 2024.1 → 2025.1 (SHA256 verified)
- zathura-pdf-poppler: 0.3.3 → 0.3.4 (SHA256 verified)

#### Desktop (batch 3 — X11/libs/apps)
- libusb: 1.0.27 → 1.0.29 (SHA256 verified)
- libx11: 1.8.10 → 1.8.13 (SHA256 verified)
- libxau: 1.0.11 → 1.0.12 (SHA256 verified)
- libxext: 1.3.6 → 1.3.7 (SHA256 verified)
- libxfixes: 6.0.1 → 6.0.2 (SHA256 verified)
- libxml2: 2.15.2 → 2.15.3 (SHA256 verified)
- libxrandr: 1.5.4 → 1.5.5 (SHA256 verified)
- linux-pam (desktop): 1.7.0 → 1.7.2 (matches base/linux-pam, SHA256 verified)
- lua: 5.4.7 → 5.4.8 (5.4.x stable; 5.5.0 is new major — staying on 5.4, SHA256 verified)
- mako: 1.10.0 → 1.11.0 (SHA256 verified)
- polkit: 125 → 127 (SHA256 verified)

#### Desktop (batch 2 — libs)
- icu: 76.1 → 78.3 (2 major versions, SHA256 verified)
- json-glib: 1.10.6 → 1.10.8 (SHA256 verified)
- kitty: 0.46.1 → 0.46.2 (SHA256 verified)
- libass: 0.17.3 → 0.17.4 (SHA256 verified)
- libblockdev: 3.2.1 → 3.4.0 (minor series bump, SHA256 verified)
- libde265: 1.0.15 → 1.0.18 (SHA256 verified)
- libevdev: 1.13.3 → 1.13.6 (SHA256 verified)
- libnotify: 0.8.4 → 0.8.8 (SHA256 verified)
- librsvg: 2.62.0 → 2.62.1 (SHA256 verified)
- libtiff: 4.7.0 → 4.7.1 (SHA256 verified)

#### Desktop (batch 1 — libs/apps)
- bolt: 0.9.8 → 0.9.11 (SHA256 verified)
- dbus: 1.16.0 → 1.16.2 (SHA256 verified, matches base/edge)
- djvulibre: 3.5.28 → 3.5.29 (SHA256 verified)
- elogind: 255.5 → 255.22 (URL tag uses `V` prefix, SHA256 verified)
- gdk-pixbuf: 2.42.12 → 2.44.6 (minor series bump, SHA256 verified)
- gtk4: 4.22.1 → 4.22.2 (SHA256 verified; 4.23 is dev)

#### Desktop (fonts/text)
- harfbuzz: 14.0.0 → 14.1.0 (SHA256 verified)
- noto-fonts: 2025.03.01 (noto-monthly-release-25.3.1) → 2026.04.01 (noto-monthly-release-2026.04.01, SHA256 verified)
- pango: 1.56.1 → 1.56.4 (SHA256 verified from download.gnome.org)

#### Desktop (graphics/wayland)
- libinput: 1.31.0 → 1.31.1 (SHA256 verified from freedesktop gitlab)
- libxkbcommon: 1.11.0 → 1.13.1 (2 major bumps, SHA256 verified)
- mesa: 26.0.4 → 26.0.5 (SHA256 verified from mesa.freedesktop.org)
- vulkan-headers: 1.4.341 → 1.4.349 (SHA256 verified)
- vulkan-loader: 1.4.348 → 1.4.349 (SHA256 verified)
- xwayland: 24.1.9 → 24.1.10 (SHA256 verified from xorg)

#### Desktop (audio/multimedia)
- flac: 1.4.3 → 1.5.0 (major version bump, SHA256 verified from xiph)
- gstreamer: 1.28.1 → 1.28.2 (SHA256 verified)
- gst-plugins-base: 1.28.1 → 1.28.2 (SHA256 verified)
- gst-plugins-good: 1.28.1 → 1.28.2 (SHA256 verified)
- libogg: 1.3.5 → 1.3.6 (SHA256 verified from xiph)
- pipewire: 1.6.2 → 1.6.3 (SHA256 verified from GitHub)

#### Edge
- ca-certificates: 2025.12.02 → 2026.03.19 (match network/ recipe, SHA256 verified from curl.se)
- coreutils: 9.7 → 9.10 (SHA256 verified)
- curl: 8.12.1 → 8.19.0 (SHA256 verified)
- dbus: 1.16.0 → 1.16.2 (SHA256 verified)
- device-mapper (LVM2): 2.03.28 → 2.03.39 (SHA256 verified)
- dhcpcd: 10.1.0 → 10.3.1 (match network/ recipe, SHA256 verified)
- e2fsprogs: 1.47.2 → 1.47.4 (SHA256 verified)
- jq: 1.7.1 → 1.8.1 (SHA256 verified)
- kernel-edge: 6.6.130 → 6.6.134 (LTS point release, SHA256 verified; install paths updated for new version)
- kmod: 33 → 34 (SHA256 verified)
- libcap: 2.73 → 2.78 (SHA256 verified)
- ncurses: 6.5 → 6.6 (SHA256 verified)
- nftables: 1.1.1 → 1.1.6 (SHA256 verified from netfilter.org)
- openssh: 10.0p1 → 10.3p1 (match network/ recipe, security fix, SHA256 verified)
- openssl: 3.5.5 → 3.5.6 (3.5.x LTS, SHA256 verified)
- readline: 8.2.13 → 8.3 (SHA256 verified)
- wireguard-tools: 1.0.20210914 → 1.0.20260223 (SHA256 verified)
- zlib: 1.3.1 → 1.3.2 (SHA256 verified)

#### AI
- crun: 1.22 → 1.27 (SHA256 verified)
- go: 1.26.1 → 1.26.2 (SHA256 verified from go.dev)
- huggingface-hub-cli: 1.9.0 → 1.11.0 (SHA256 verified)
- llama-cpp: b8664 → b8815 (build tag bump, SHA256 verified)
- nccl: 2.29.7 → 2.30.3 (URL tag v2.30.3-1, SHA256 verified)
- ollama: 0.20.2 → 0.20.7 (SHA256 verified)
- podman: 5.8.1 → 5.8.2 (SHA256 verified)
- python-transformers: 5.5.0 → 5.5.4 (SHA256 verified)
- rocm: 7.2.1 → 7.2.2 (SHA256 verified)

#### Browser
- brave: 1.91.9 → 1.91.64 (SHA256 verified from GitHub tarball)
- chromium: 147.0.7727.49 → 147.0.7727.101 (SHA256 remains TODO — tarball ~6GB)
- falkon: 25.12.3 → 26.04.0 (KDE release-service bump, SHA256 verified)
- firefox: 149.0 → 149.0.2 (SHA256 verified from mozilla.org)
- librewolf: 149.0-1 → 149.0.2-2 (SHA256 verified from codeberg)
- midori: 11.6.4 → 11.6.5.1 (SHA256 verified from GitHub tarball)
- vivaldi: 7.9.3970.45 → 7.9.3970.55 (SHA256 verified from .deb; pre_build command updated)
- zen-browser: 1.19.6b → 1.19.8b (SHA256 verified from GitHub tarball)

### Fixed

#### Base
- zlib 1.3.2: corrected SHA256 `d7a0654783a4...` → `bb329a0a2cd02...` (prior hash did not match actual tarball at recipe URL; would have broken download verification)
- binutils: URL fixed (`binutils-2.46.tar.xz` returned 404 → `binutils-2.46.0.tar.xz`; GNU changed 2.46 tarball naming to include patch digit) + version field `2.46` → `2.46.0` + SHA256 corrected to match actual tarball (`80c3fe2a...` → `d75a94f4...`)
- pkgconf: version `3.0.0` → `2.5.1` (3.0.0 does not exist upstream, URL returned 404; prior bump was erroneous — latest pkgconf is 2.5.1). SHA256 corrected against actual tarball.
- util-linux 2.42: SHA256 corrected `38bef8cb64da4...` → `3452b260bbaa7...` (prior hash did not match actual tarball at recipe URL; would have broken download verification)

#### Database
- redis7: license `RSALv2+SSPLv1` → `LicenseRef-RSALv2 OR SSPL-1.0` (valid SPDX expression; RSALv2 has no SPDX identifier, SSPLv1 is `SSPL-1.0`)

#### Root
- ifran.cyml: version `2026.3.10` → `1.3.0` (upstream release format; prior tag did not exist), SHA256 populated (was TODO placeholder), cross-reference to marketplace/ifran.cyml corrected (was .toml)

### Known Issues (flagged for review)

- libcap-ng: recipe at 0.8.5 (released 2023). Upstream latest is 0.9.3 but redhat.com mirror stops at 0.8.5 and GitHub archive tarballs lack pre-generated `configure` script (only `autogen.sh` present). Bumping requires adding autotools to build deps and running `autogen.sh` in pre_build — left at 0.8.5 pending decision.
- cyrius (base recipe): recipe at 0.9.0 with empty SHA256 and `release_asset = "cc2"`. Upstream at 5.1.12 and compiler renamed cc2 → cc5. Bumping requires updating version + release_asset name + filling SHA — deferred, needs coordinated change across recipes that depend on cyrius.
- kybernet (base recipe): recipe at 0.9.0 with empty SHA256 (TODO). Upstream at 1.0.1. Release asset exists but SHA needs manual verification from release tarball.
- gvisor: recipe pinned to literal string `"latest"` with rolling-release URL pointing to `/release/latest/x86_64/runsc`. SHA256 populated but will drift silently with each upstream release. Either pin to a specific version tag or document this behavior.
- agnos-kernel: recipe at 1.0.0 (bumped previously); GitHub API returns no tags for `MacCracken/agnos-kernel` — recipe `github_release` points to `MacCracken/agnos` (different repo). Unable to verify independently via curl.

#### Desktop
- fontconfig: URL fixed (freedesktop.org/.../release/ returned 404) → gitlab.freedesktop.org generic package endpoint; SHA256 updated from working tarball
- gtk3: version `3.24.52` → `3.24.43` (3.24.52 does not exist upstream — latest stable 3.24.x is 3.24.43; prior bump was erroneous; SHA256 corrected)

### Audited

#### Database
- postgresql17 17.9 — current upstream (major=17, latestMinor=9 per postgresql.org versions.json), SHA256 populated
- redis7 7.4.8 — current upstream 7.x stable, SHA256 verified against release tarball
- pgvector 0.8.2 — current upstream, SHA256 verified against release tarball

#### Python
- python3.12 3.12.13 — current upstream, SHA256 populated

#### AI (at current upstream, SHA256 populated)
- cni-plugins 1.9.1, conmon 2.2.1, jupyter-server 2.17.0, lapack 3.12.1, onnxruntime 1.24.4, openblas 0.3.32, python-numpy 2.4.4, python-pandas 3.0.2, python-pytorch 2.11.0, python-safetensors 0.7.0, python-scipy 1.17.1, slirp4netns 1.3.3, vllm 0.19.0, vulkan-compute-tools 1.4.341, yajl 2.1.0, nvidia-cuda-toolkit 12.8.1

#### Base (toolchain at current upstream)
- gcc 15.2.0 (SHA256 verified against upstream tarball), glibc 2.43 (SHA256 verified)

#### Base (GCC deps — all current, SHA256 verified)
- gmp 6.3.0, mpfr 4.2.2, mpc 1.3.1, bc 7.0.3

#### Base (build tools at current upstream, SHA256 verified)
- make 4.4.1, gawk 5.4.0, bison 3.8.2, flex 2.6.4, automake 1.18.1, libtool 2.5.4, gperf 3.3

#### Base (interpreters at current upstream)
- perl 5.42.2 (5.42.x stable; 5.43.x is dev)

#### Base (core utilities at current upstream)
- sed 4.9, grep 3.12, findutils 4.10.0, diffutils 3.12, patch 2.8

#### Base (filesystem/storage at current upstream, SHA256 verified)
- util-linux 2.42 (SHA corrected — see Fixed), e2fsprogs 1.47.4, dosfstools 4.2, eudev 3.2.14, kmod 34.2

#### Base (common libraries at current upstream, SHA256 verified)
- attr 2.5.2, acl 2.3.2, expat 2.7.5, libffi 3.5.2, libseccomp 2.6.0, libargon2 20190702 (upstream EOL), libnghttp2 1.68.1, libpipeline 1.5.8

#### Base (init/system tools at current upstream)
- procps-ng 4.0.6, psmisc 23.7, sysvinit 3.14, sysklogd 2.7.2, inetutils 2.6, iproute2 6.19.0

#### Base (auth/security at current upstream, SHA256 verified)
- shadow 4.19.4, sudo 1.9.17p2, audit 4.0.2

#### Base (small libraries at current upstream)
- json-c 0.18 (tag json-c-0.18-20240915), libaio 0.3.113, libmnl 1.0.5, ncurses 6.6, readline 8.3, gdbm 1.26, freetype 2.14.3

#### Base (shell/text tools at current upstream)
- bash 5.3, less 692, man-db 2.13.1

#### Base (build/network/firmware at current upstream)
- cmake 4.3.1, curl 8.19.0 (matches edge), dbus 1.16.2 (matches edge), grub 2.14, intel-ucode microcode-20260227

#### Base (compression/archive at current upstream)
- bzip2 1.0.8 (upstream end-of-life at 1.0.8), cpio 2.15, gzip 1.14, lz4 1.10.0, tar 1.35, xz 5.8.3 (SHA256 verified), zlib 1.3.2 (SHA256 corrected above), zstd 1.5.7

#### Edge (at current upstream)
- avahi 0.8, bash 5.3 (SHA256 verified), busybox 1.37.0, cryptsetup 2.7.5 (recipe tracks v2.7 LTS path), eudev 3.2.14, iproute2 6.19.0, tpm2-tools 5.7, tpm2-tss 4.1.3, util-linux 2.40.4 (recipe tracks v2.40 LTS path)

#### Desktop (audio/multimedia at current upstream)
- alsa-lib 1.2.15.3, alsa-utils 1.2.15.2, bluez 5.86, cups 2.4.16, ffmpeg 8.1, libvorbis 1.3.7, wireplumber 0.5.14

#### Desktop (graphics/wayland at current upstream)
- glslang 16.2.0, libdrm 2.4.131, wayland 1.25.0, wayland-protocols 1.48

#### Desktop (fonts/text at current upstream)
- cairo 1.18.4, fcft 3.3.3, fribidi 1.0.16, pixman 0.46.4

#### Desktop (batch 1 — current upstream, SHA256 populated)
- atk 2.38.0, cliphist 0.7.0, duktape 2.7.0, eudev 3.2.14, foot 1.26.1, fuzzel 1.14.1, glib 2.88.0, gobject-introspection 1.86.0, graphene 1.10.8, greetd 0.10.3, helix 25.07.1

#### Desktop (batch 2 — current upstream)
- imv 5.0.1, lcms2 2.18, libatasmart 0.19 (upstream unmaintained), libepoxy 1.5.10, libheif 1.21.2, libjpeg-turbo 3.1.4.1, libplacebo 7.360.1, libsass 3.6.6 (newer v1.0.1/v2.0 tags appear pre-release), libsndfile 1.2.2, libspectre 0.2.12

#### Desktop (batch 3 — current upstream)
- libva 2.23.0, libxcb 1.17.0, libxdmcp 1.1.5, libxi 1.8.2, libxrender 0.9.12, mpv 0.41.0, mtdev 1.1.7, pcre2 10.47

#### Desktop (batch 4 — current upstream)
- poppler 26.04.0, sassc 3.6.2, scdoc 1.9.7, simde 0.8.2, tllist 1.1.0, tuigreet 0.9.1, utf8proc 2.11.3, wlroots 0.20.0, x265 4.1, xcb-proto 1.17.0, xxhash 0.8.3, yazi 26.1.22, zathura-djvu 0.2.11

#### Desktop (batch 1 flagged — no action)
- girara 0.4.5: recipe URL exists but upstream switched to date-based versioning (latest: 2026.02.04). Keeping at 0.4.5 for now; bumping requires URL format rework
- agnos-desktop 2026.3.25: local/AGNOS-native, no upstream to verify

#### Desktop (batch 3 flagged — no action)
- nvidia-driver: recipe at 570.133.07; upstream latest production stable is 595.58.03. Bumping proprietary NVIDIA drivers requires careful version selection (branch/ML/beta distinctions). Flagged for deliberate decision.

#### Desktop (batch 4 flagged — no action)
- zathura: recipe at 0.5.14 but upstream pwmt.org switched to date-based versioning (latest: 2026.03.27). Same issue as girara. Bumping requires URL format rework.

#### Edge (local builds — no upstream)
- agnos-edge-agent 2026.3.11, esp32-agent 2026.3.18, glibc 2.42 (local build), secureyeoman-edge 2026.3.18

#### Sandbox (local builds — no upstream)
- sy-agnos-init 2026.3.18, sy-agnos-nftables 2026.3.18, sy-agnos-rootfs 2026.3.18

#### Network
- ca-certificates 2026.03 (cacert-2026-03-19.pem) — current upstream
- iw 6.17 — current upstream (kernel.org)
- libnl 3.12.0 — current upstream
- networkmanager 1.51.4 — current stable (rc1/rc2 exist but not tracking pre-releases)
- openssh 10.3p1 — current upstream
- rsync 3.4.1 — current upstream
- wget 1.25.0 — current upstream
- wpa-supplicant 2.11 — current upstream

### Version Bumps

#### Base
- agnos-kernel: 0.9.0 → 1.0.0 (first stable release, SHA256 verified from release asset)

#### Marketplace
- agnos-kernel: 0.9.0 → 1.0.0 (status updated from pre-release to stable, SHA256 verified)

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
