# Changelog

All notable changes to zugot will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/) and
[Semantic Versioning](https://semver.org/).

## [Unreleased]

### marketplace — drift sweep (local repos → recipes, SHA verified)

Sweep of the locally checked-out `MacCracken/*` projects against their marketplace recipes (`VERSION` / git tag / CHANGELOG cross-checked, then each repo's GitHub `releases/<tag>` confirmed to publish the asset). **9 recipes bumped**, each SHA256 downloaded and recomputed against the upstream release asset (matched the published `SHA256SUMS` / `.sha256` companion). Full field audit per recipe — a license error surfaced and was fixed (see below). Validator clean.

- **`base/cyrius.cyml`** + **`marketplace/cyrius.cyml`** 6.2.11 → **6.2.12** (`cyrius-6.2.12-x86_64-linux.tar.gz`, `ff2f05eb…`; both bumped in lockstep).
- **`itihas.cyml`** 2.3.4 → **2.3.5** (bare `itihas` asset = `build/itihas`, `527e9283…`).
- **`shakti.cyml`** 0.6.2 → **0.7.0** (`shakti-0.7.0-x86_64-linux`, `332e212f…`; upstream 0.x releases flagged pre-release, so `releases/latest` lags — confirmed against the explicit `0.7.0` release). Header verification note advanced 0.6.2 → 0.7.0.
- **`sigil.cyml`** 3.7.14 → **3.7.16** (`sigil-3.7.16.tar.gz`, `236dc72a…`).

### SecureYeoman 0.5.0 → 0.5.3 + license fix (AGPL)

- All five **`marketplace/secureyeoman*.cyml`** recipes 0.5.0 → **0.5.3**, SHA verified per variant: main/primary `secureyeoman-0.5.3-linux-x64` (`678c0576…`); agent/lite `secureyeoman-0.5.3-agent-linux-x64` (`a4d55c93…`); sqlite `secureyeoman-0.5.3-sqlite-linux-x64` (`0146caa3…`). Hardcoded `release_asset` + install-script asset names advanced 0.5.0 → 0.5.3 in the main and primary recipes.
- **`edge/secureyeoman-edge.cyml`** 0.5.0 → **0.5.3** (`secureyeoman-0.5.3-edge-linux-x64`, `57db4048…`) — caught in the full-tree sweep; this variant lives in `edge/` and was missed by the initial marketplace pass. License field here was already `AGPL-3.0-only`.
- **License corrected `GPL-3.0-only` → `AGPL-3.0-only`** on all five. Upstream `LICENSE` is GNU AGPLv3, and `package.json` / README both declare `AGPL-3.0-only` (a commercial dual-license is offered separately). The prior `GPL-3.0-only` field was wrong.

### Third-party version sync — full-tree sweep (SHA verified, deps re-checked)

Swept all 563 recipes against upstream. GitHub-sourced recipes (282) checked via `git ls-remote --tags`, then **de-noised against authoritative `releases/latest`** — the raw tag scan threw ~39 false positives from junk historical tags (`curl-7_19_4`, `FIPS_098_TEST_1`, `twitter-20100825`, stale CalVer). 32 confirmed behind; **22 low-risk/fast-moving bumped here**, each tarball downloaded, archive-type-checked, and SHA256 recomputed. Major base/system bumps (openssl, elogind, llvm, firecracker) and brave/aquamarine deferred to deliberate per-recipe passes.

- **base** — `abseil-cpp` 20260107.1 → **20260526.0** (`6e1aee53…`). `cbindgen` 0.29.2 → **0.29.4** (`9b5757e9…`). `iana-etc` 20260511 → **20260612** (`f12153a2…`). `protobuf` 35.0 → **35.1** (`22775f93…`).
- **desktops** — `fmt` 12.1.0 → **12.2.0** (`a2f4a8d5…`). `graphite2` 1.3.14 → **1.3.15** (`c6bc8b42…`). `harfbuzz` 14.2.0 → **14.2.1** (`a54a5d8e…`). `hwdata` 0.407 → **0.408** (`ac7c34ef…`). `kitty` 0.47.0 → **0.47.4** (`85c21929…`). `libde265` 1.1.0 → **1.1.1** (`fd48a927…`). `libheif` 1.22.2 → **1.23.0** (`4c9182b1…`). `libxkbcommon` 1.13.1 → **1.13.2** (`acc4d5f7…`). `msgpack-c` 6.1.0 → **7.0.1** (`2d80f190…`; release-tag scheme `c-7.0.1`). `pugixml` 1.15 → **1.16** (`357bcab8…`).
- **ai** — `fuse-overlayfs` 1.16 → **1.17** (`cefffecf…`). `runc` 1.4.2 → **1.4.3** (`e0a89f9e…`). `huggingface-hub-cli` 1.16.4 → **1.19.0** (`a2a89bf5…`). `jupyter-server` 2.18.2 → **2.19.0** (`08bca832…`). `ollama` 0.24.0 → **0.30.8** (`9f353130…`). `python-transformers` 5.9.0 → **5.12.1** (`c27e47bc…`). `vllm` 0.21.0 → **0.23.0** (`a32a008b…`). `rocm` 7.2.2 → **7.2.4** (`a80fc166…`). System-level deps (`python`, `glibc`, `go`, `pytorch`, `numpy`, `cmake`) unchanged across these bumps — pip-level deps resolve at build time.

### Major / high-blast-radius bumps (worked individually, SHA verified)

- **OpenSSL 3.5.6 → 3.5.7** (`base/openssl.cyml` + `edge/openssl.cyml`, SHA `a8c0d28a…`). Stayed on the **3.5 LTS line** rather than jumping to the newly-released 4.0.1: 4.0 bumps `SHLIB_VERSION` 3 → 4 (`libcrypto.so.3` → `.so.4`), a hard ABI break requiring a coordinated rebuild of every OpenSSL consumer. 3.5.7 is a drop-in patch (soname unchanged), supported to 2030. License `Apache-2.0` and `./config` unchanged.
- **elogind 255.25 → 257.16** (`desktops/elogind.cyml`, SHA `3c814640…`). Major series jump; verified the recipe's only meson flag (`-Dcgroup-controller=elogind`) still exists in 257.16's `meson_options.txt`, and deps (`dbus`, `polkit`, `linux-pam`) + `LGPL-2.1-only` license unchanged.
- **llvm 22.1.6 → 22.1.8** (`base/llvm.cyml`, SHA `922f1817…`) — patch within 22.1.x, cmake build unchanged.
- **firecracker 1.15.1 → 1.16.0** (`base/firecracker.cyml`, SHA `bd04e269…`) — binary release tarball; install uses version-wildcard globs, no build change.
- **brave 1.91.64 → 1.91.172** (`browser/brave.cyml`, SHA `3621fd7b…`) — same 1.91 line.
- **aquamarine 0.11.0 → 0.12.1** (`desktops/aquamarine.cyml`, SHA `80120257…`) — Hyprland backend lib, cmake build unchanged.

### Not bumped — flagged

- **`varna.cyml`** stays at **1.0.0**: 2.0.0 is the in-progress Cyrius port (local CHANGELOG dated 2026-06-16) and is **not yet tagged or released** on GitHub — only the 1.0.0 release exists and it ships no assets. Revisit once the 2.0.0 Cyrius-port release with a `source`-resolvable artifact is published.
- **`agnos-edge-agent.cyml`** stays at **2026.3.11** (empty SHA + TODO): upstream `agnosticos` is at 2026.3.31, but that release ships only OS images (`.iso`/`.img`) — no `agnos-edge-agent-*.tar.xz` asset — and the tag dropped its `v` prefix. Pending a published agent artifact, not a missed sync.
- **`network/libnl.cyml`** stays at **3.12.0** — tag-scan false positive: upstream's latest release tag `libnl3_12_0` *is* 3.12.0 (already in sync).
- **`vulkan-headers` / `vulkan-loader`** (1.4.352): tag-scan saw 1.4.354 but neither repo publishes a GitHub "latest" release (SDK-tagged). Needs a manual Vulkan-SDK-tag check — left for a per-SDK pass.

## [1.0.3] - 2026-06-15

A maintenance / drift-cleanup release, roughly three weeks after 1.0.2. Drift was re-detected across all 112 GitHub-sourced `MacCracken/*` recipes via `git ls-remote --tags`, then **confirmed against each repo's authoritative `releases/latest`** (tag-sorting alone was unreliable — several repos still carry stale CalVer tags that sort above their current semver). **35 recipes bumped**, each with its SHA256 verified against the upstream release asset (GitHub-published asset `digest:` cross-checked against the `.sha256` / `SHA256SUMS` companion). Dependency, license, and field audits run per recipe; the two major bumps (`mabda` 2→3, `szal` 1→2) cross-checked against upstream manifests — no new deps. Validator clean across all recipes.

### Cyrius toolchain bump — 6.0.3 → 6.2.11

- **`base/cyrius.cyml`** and **`marketplace/cyrius.cyml`** 6.0.3 → **6.2.11**. Tarball SHA256 `bed1a7e3…` verified two ways (GitHub asset digest + the upstream `cyrius-6.2.11-x86_64-linux.tar.gz.sha256` companion). Install steps unchanged — the 6.x binary set (`cycc`, `cyrius`, `ark`, `cybs`, `cyaudit`, `cyrius-lsp`, …) is stable. The v6.0.x `cc5`/`cyrc` back-compat symlinks are retained pending confirmation that upstream has retired the legacy consumers (the install creates them itself, so they are harmless; flagged for the next pass).

### base — version bumps (SHA verified)

- **`base/agnos-kernel.cyml`** + **`marketplace/agnos-kernel.cyml`** 1.35.3 → **1.45.10** (`agnos-1.45.10-src.tar.gz`, `d14af566…`).
- **`base/bazaar.cyml`** 1.0.1 → **1.0.2** (`bazaar-1.0.2-src.tar.gz`, `81c5a383…`). Tracks the zugot 1.0.3 tag.
- **`base/cyim.cyml`** 1.7.1 → **1.7.3** (`cyim-1.7.3-x86_64-linux.tar.gz`, `916e046e…`).
- **`base/kybernet.cyml`** + **`marketplace/kybernet.cyml`** 1.2.1 → **1.3.4** (`kybernet-1.3.4-src.tar.gz`, `a72ea8a8…`).
- **`base/owl.cyml`** 1.3.6 → **1.4.0** (`owl-1.4.0-x86_64-linux.tar.gz`, `3382b683…`).

### marketplace — version bumps (SHA verified)

- **`abaco.cyml`** 2.2.4 → **2.3.0** (`5951277c…`). **`aegis.cyml`** 1.0.0 → **1.0.1** (`450a424a…`). **`agnoshi.cyml`** 1.3.3 → **1.7.0** (`agnsh-1.7.0-x86_64-linux`, `9690f65e…`; stale ship-date narrative in the header trimmed). **`agnostik.cyml`** 1.2.2 → **1.3.1** (`0772c085…`). **`agnosys.cyml`** 1.2.7 → **1.4.3** (`578eddd3…`).
- **`ai-hwaccel.cyml`** 2.2.6 → **2.3.12** (`9c04f276…`). **`argonaut.cyml`** 1.7.0 → **1.8.3** (`140d3517…`). **`avatara.cyml`** 2.3.0 → **2.7.2** (`dc5b6307…`). **`bote.cyml`** 2.7.2 → **2.7.6** (`f4019947…`). **`daimon.cyml`** 1.2.3 → **1.2.9** (`b46a0775…`).
- **`itihas.cyml`** 2.2.0 → **2.3.4** (`a3f7d846…`). **`kavach.cyml`** 3.2.1 → **3.4.2** (`0df872cf…`). **`libro.cyml`** 2.6.3 → **2.7.4** (`ad1ebb07…`). **`majra.cyml`** 2.4.4 → **2.4.7** (`9169894d…`). **`patra.cyml`** 1.9.5 → **1.11.2** (`08bcfa8d…`).
- **`phylax.cyml`** 1.1.1 → **1.2.0** (`be856115…`). **`sigil.cyml`** 3.4.3 → **3.7.14** (`sigil-3.7.14.tar.gz`, `514640bd…`). **`t-ron.cyml`** 2.1.4 → **2.1.6** (`5785bced…`). **`vidya.cyml`** 2.7.1 → **2.7.3** (`471e7832…`). **`yukti.cyml`** 2.2.3 → **2.2.5** (`5ded3ea4…`).
- **`nous.cyml`** 1.2.5 → **1.2.6** (`dec324f0…`); hardcoded `release_asset` version advanced 1.2.5 → 1.2.6.

### marketplace — major bumps (deps cross-checked, SHA verified)

- **`mabda.cyml`** 2.5.0 → **3.2.2** (`mabda-3.2.2-src.tar.gz`, `91cf4e5f…`). Upstream `cyrius.cyml` declares no external runtime deps (vendored Cyrius modules) — recipe `runtime=[]` / `build=["cyrius"]` unchanged.
- **`szal.cyml`** 1.1.0 → **2.0.0** (`ec777223…`). `release_asset = "source"` resolves to the GitHub auto-generated source archive (`/archive/refs/tags/2.0.0.tar.gz`) — confirmed by matching the prior 1.1.0 SHA to that artifact, not the `-src.tar.gz` asset or the crates.io checksum. Upstream `Cargo.toml` has no dependencies — recipe unchanged.

### marketplace — asset-shape fixes (bare → versioned binary)

Upstream stopped shipping the bare `<name>` release asset; the latest releases publish only `<name>-<version>-x86_64-linux`. `release_asset` switched to the `<name>-*-x86_64-linux` glob and the install step rewritten to locate the binary by glob (`find … -name '<name>-*-x86_64-linux'`):

- **`hisab.cyml`** 2.2.0 → **2.6.6** (`32ba0fe4…`). **`hoosh.cyml`** 2.0.0 → **2.4.6** (`b0d9e6b5…`). **`nein.cyml`** 1.5.1 → **1.5.3** (`06d62880…`).
- **`shakti.cyml`** → **0.6.2** (`bff63c2f…`). Supersedes the staged 0.4.0 edit (which carried the stale 0.2.2 binary's hash and a `# TODO` blocking install). The bare `shakti` asset is gone; switched to the versioned glob with a verified SHA, so install is no longer blocked. Note: upstream 0.x tags are all flagged pre-release.

## [1.0.2] - 2026-05-27

A maintenance / drift-cleanup release. P(-1)-style version audit roughly a month after 1.0.1, focused on the fast-moving AGNOS-native (MacCracken/\*) ecosystem. Drift was detected for every GitHub-sourced recipe via `git ls-remote --tags` (no REST rate limit) and confirmed against each repo's authoritative `releases/latest`; SHA256 for every bump was verified against the release asset digest (GitHub-published `digest:` / `SHA256SUMS`). The Cyrius toolchain bumped 5.7.25 → 6.0.3 (binary renames). New `marketplace/patra` recipe. A second pass extended the audit to third-party GitHub recipes: 53 libraries bumped to current releases with download-verified SHAs (only `brave` left untouched, on a release-channel mismatch). `noted-issues-bazaar-finds.md` retired. Validator clean across all 563 recipes.

### Cyrius toolchain bump — 5.7.25 → 6.0.3 (2026-05-27)

- **`base/cyrius.cyml`** and **`marketplace/cyrius.cyml`** 5.7.25 → **6.0.3**. Tarball SHA256 verified (`8a49fb40…`) two ways: GitHub asset digest and the upstream `cyrius-6.0.3-x86_64-linux.tar.gz.sha256` companion file. **6.0.0 renamed the toolchain binaries** — install steps were rewritten to match (the old script referenced `bin/cc5`/`bin/cyrc` which no longer exist and would have failed):
  - `cc5` → **`cycc`** (main compiler); `cc5_aarch64` → **`cycc_aarch64`** (cross-compiler).
  - `cyrc` → **`cybs`** (build-script tool).
  - New tools installed: `cyaudit`, `cyrius-lsp` (guarded with `[ -f ]` so a future minor that renames/drops one fails soft; the core compiler/build/ark set stays unconditional).
  - Retired binaries no longer installed: `cyrc`, and the `cyrius-init/repl/port` shims are now installed only when present.
  - **v6.0.x back-compat symlinks** added (`cc5 → cycc`, `cyrc → cybs`), mirroring upstream's own installer; to be dropped at the 6.1 bump when upstream retires them.
  - Stdlib install made recursive (6.x nests subdirs, e.g. `lib/unicode/`); module count 65 → 88. `asm` seed install switched to `install -Dvm755` so its parent dir is created.
- **`base/kybernet.cyml`** header comment `cc5 toolchain` → `cycc toolchain`.

### base — version bumps (SHA verified)

- **`base/agnos-kernel.cyml`** 1.26.1 → **1.35.3** (`agnos-1.35.3-src.tar.gz`, `d7b95d2c…`).
- **`base/bazaar.cyml`** 1.0.0 → **1.0.1** (`bazaar-1.0.1-src.tar.gz`, `d755ce58…`).
- **`base/cyim.cyml`** 1.2.1 → **1.7.1** (`cyim-1.7.1-x86_64-linux.tar.gz`, `85a19aba…`).
- **`base/owl.cyml`** 1.1.9 → **1.3.6** (`owl-1.3.6-x86_64-linux.tar.gz`, `0212b066…`).
- **`base/kybernet.cyml`** 1.0.2 → **1.2.1** (`kybernet-1.2.1-src.tar.gz`, `96d3f18f…`).

### marketplace — version bumps (SHA verified)

- **`nous.cyml`** 1.1.1 → **1.2.5**. Asset shape changed: 1.2.x ships a bare prebuilt binary (`nous-1.2.5-x86_64-linux`), not a tarball. `release_asset` and install rewritten to glob the bare binary; stale `rust` tag → `cyrius`. SHA `3d3b61d6…`.
- **`agnos-kernel.cyml`** 1.26.1 → **1.35.3** (`d7b95d2c…`).
- **`abaco.cyml`** 2.2.0 → **2.2.4** (`d759f0d1…`).
- **`agnoshi.cyml`** 1.3.1 → **1.3.3** (`918659a2…`). Recipe was "staged" against a not-yet-cut release with a placeholder note pointing at the v1.0.0 hash; the v1.3.3 release is now live, so the SHA is real and the staging comments were removed.
- **`agnostik.cyml`** 1.0.0 → **1.2.2** (`fa572a58…`).
- **`agnosys.cyml`** 1.0.2 → **1.2.7** (`52b91f12…`).
- **`ai-hwaccel.cyml`** 2.0.0 → **2.2.6** (`71fff27e…`).
- **`argonaut.cyml`** 1.5.0 → **1.7.0** (`c5c1e733…`).
- **`bote.cyml`** 2.5.1 → **2.7.2** (`3ec38609…`).
- **`daimon.cyml`** 1.1.4 → **1.2.3** (`71aea9ea…`).
- **`kavach.cyml`** 3.0.0 → **3.2.1** (`0d0841e8…`).
- **`kybernet.cyml`** 1.0.2 → **1.2.1** (`96d3f18f…`).
- **`libro.cyml`** 2.0.5 → **2.6.3** (`34ac5044…`).
- **`majra.cyml`** 2.4.1 → **2.4.4** (`5e37340b…`).
- **`nein.cyml`** 1.0.0 → **1.5.1** (`b540b9be…`).
- **`phylax.cyml`** 1.0.0 → **1.1.1** (`fc694a51…`).
- **`sigil.cyml`** 2.9.4 → **3.4.3** (`13f39680…`).
- **`t-ron.cyml`** 2.0.0 → **2.1.4** (`3b9e5c1d…`).
- **`yukti.cyml`** 2.1.1 → **2.2.3** (`cd07fe59…`). (The `2.2.4` git tag is not a published release; tracked `releases/latest` = 2.2.3.)

**release_asset shape fix — bare → versioned binary:** `ai-hwaccel`, `bote`, `kavach`, `phylax`, `t-ron` upstream renamed their release binary from a bare `<name>` to `<name>-<version>-x86_64-linux`. `release_asset` changed to the `<name>-*-x86_64-linux` glob and the install line to `install -Dm755 <name>-*-x86_64-linux …`.

### SecureYeoman — CalVer → semver, build-from-source → prebuilt binary

The six SecureYeoman recipes were on the abandoned alpha CalVer scheme (`2026.3.x`, with the `version` field already drifted to `2026.3.28` while headers said `2026.3.18`), carried empty `# TODO` SHAs, and built from source (Bun/npm; Go for edge) in a flow that no longer matches upstream. Upstream dropped CalVer (it didn't match release frequency) and now publishes semver **0.5.0** as **prebuilt signed binaries** (per-platform, `.sig`/`.cert` + `SHA256SUMS`; backend rewritten to Rust, Cyrius port pending → v1). All six bumped to **0.5.0** and reworked to install the prebuilt binary directly (`pre_build`/`make`/`check` cleared, `build` deps emptied, real SHAs populated). The icon and `.env.example` install steps were dropped (those assets are not in the release); inline `.desktop` entries and systemd/init units are preserved. Binary mapping:

- **`secureyeoman.cyml`** (flagship) + **`secureyeoman-primary.cyml`** → `secureyeoman-0.5.0-linux-x64` (`2ecfcb60…`; primary sets `SY_ROLE=primary`).
- **`secureyeoman-agent.cyml`** + **`secureyeoman-lite.cyml`** → `secureyeoman-0.5.0-agent-linux-x64` (`9e306a41…`).
- **`secureyeoman-sqlite.cyml`** → `secureyeoman-0.5.0-sqlite-linux-x64` (`3c985759…`).
- **`edge/secureyeoman-edge.cyml`** → `secureyeoman-0.5.0-edge-linux-x64` (`ef5e2412…`); AGPL-3.0-only retained.

### Added

- **`marketplace/patra.cyml`** — patra **1.9.5**, "the sovereign database": embedded SQL/structured storage for Cyrius (B-tree, WAL, paged I/O, JSONL). GPL-3.0-only. Modeled on the agnosys/agnostik library template (ships the source tree to `/usr/lib/patra/`; downstream consumers use `[deps.patra]` git deps). Builds with `cyrius`; pulls the `sakshi` test lib as a build-time git dep. SHA verified against `patra-1.9.5-src.tar.gz` (`a0865463…`).

### Language updates — Rust → Cyrius port

- **`marketplace/aegis.cyml`** 0.1.0 → **1.0.0**. Upstream ported the security daemon from Rust to Cyrius and now ships a prebuilt static binary. Header `Lib: aegis = "0.1.0" in Cargo.toml` → Cyrius line; `groups`/`tags` `rust` → `cyrius`; `release_asset` `aegis-*-linux-amd64.tar.gz` (never matched) → `aegis-*-x86_64-linux`; build `cargo build`/`cargo test` → none (prebuilt); `build = ["rust"]` → `[]`; install switched from `target/release/aegis` to the prebuilt binary (systemd unit preserved). SHA populated — was an empty `# TODO` (`43bdf813…`).

### Placeholder SHA population (`sha256 = ""` backlog)

Swept the 76 recipes carrying an empty `sha256 = ""  # TODO`. **48 are now populated** with verified hashes:

- **46 `release_asset = "source"` recipes** got the sha256 of their pinned tag's GitHub source archive (tag located via `git ls-remote`, `archive/refs/tags/<tag>.tar.gz` downloaded + hashed). This also resolves the three source-only recipes whose versions were bumped earlier this release — `goonj` 1.1.1→1.4.3, `naad` 1.0.0→1.2.5, `mastishk` 1.0.0→1.1.0 — which now carry real SHAs rather than `# TODO`.
- **`vidya`** 2.7.1 — `vidya-2.7.1-src.tar.gz` (unambiguous `*-src.tar.gz` match).
- **`photisnadi`** — `release_asset` pinned to the exact `photisnadi-202603181-linux-x64.tar.gz` (the prior `*-linux-x64.tar.gz` glob also matched the `-server` build), SHA populated.

**28 remain empty — no verifiable artifact exists yet**, grouped by cause:
- *No published release/tag (unscaffolded):* `abacus`, `aethersafha`, `agnostic`, `mela`, `murti`, `salai`, `samay`, `seema`, `takumi`, `tanur`.
- *Release exists but ships no downloadable asset* (the recipe's `*-linux-amd64.tar.gz` glob matches nothing upstream): `aequi`, `agnosai`, `bullshift`, `delta`, `jalwa`, `kiran`, `mneme`, `nazar`, `rahd`, `selah`, `shruti`, `sutra`, `tarang`, `tazama`, `vidhana`.
- *Version/asset mismatch:* `rasa` (the 2026.3.23 release ships only `2026.3.18`-named assets), `stiva` (recipe `2.0.0` is ahead of upstream max `1.0.0`), `edge/agnos-edge-agent` (pinned `agnos-edge-agent-*.tar.xz` absent from the agnosticos release). These need an upstream fix or a recipe decision, not a hash.

### Removed

- **`noted-issues-bazaar-finds.md`** — the bazaar cross-reference audit doc. All issues it tracked are resolved: the two remaining unresolved deps (`pycups`, `pycurl`) now exist in `ai/`; the filename≠name cases were fixed (files renamed to `base/pip.cyml`, `base/npm.cyml`); validator is clean against bazaar. Its four references were redirected to CLAUDE.md §Naming Conventions (`CLAUDE.md`, `README.md`, `CONTRIBUTING.md`, `docs/adr/0003-naming-conventions.md`).

### Audit notes — flagged, no change

- **`marketplace/stiva.cyml`** — recipe declares `2.0.0` but upstream's max tag and `releases/latest` are both `1.0.0`. The recipe is *ahead* of upstream; left untouched (downgrading is riskier than the discrepancy) pending clarification of whether 2.0.0 was anticipated.
- **`edge/agnos-edge-agent.cyml`** — pins `agnosticos` asset `agnos-edge-agent-2026.3.11.tar.xz`, which does not exist in the current `2026.3.31` release (assets are full-OS images + `agnos-linux-*.tar.gz`). SHA was already an empty `# TODO`; recipe needs an upstream fix to identify the edge-agent asset.

### Third-party — version bumps (SHA verified by tarball download)

A `git ls-remote` sweep of the 156 non-MacCracken GitHub-sourced recipes, de-noised to genuine stable releases and confirmed against each repo's `releases/latest`, found the drift below. Each tarball was downloaded and SHA256 computed fresh (no GitHub digest exists for source archives); version, URL, and SHA were updated and re-verified (0 mismatches). All are point/minor releases whose recipes reference the version only in the `url` line (build steps use the build system's srcdir handling — no hardcoded version paths).

- **base/** (13): `bc` 7.0.3→7.1.0, `boost` 1.90.0→1.91.0, `dracut` 110→111, `expat` 2.7.5→2.8.1, `gyp` 0.22.0→0.22.2, `hyprwayland-scanner` 0.4.5→0.4.6, `iana-etc` 20260409→20260511, `intel-ucode` 20260227→20260512, `libnghttp2` 1.68.1→1.69.0, `llvm` 22.1.3→22.1.6, `meson` 1.11.0→1.11.1, `mimalloc` 3.3.0→3.3.2, `protobuf` 34.1→35.0.
- **ai/** (12): `containerd` 2.2.3→2.3.1, `crun` 1.27→1.28, `cython` 3.2.4→3.2.5, `huggingface-hub-cli` 1.11.0→1.16.4, `jupyter-server` 2.17.0→2.18.2, `nccl` 2.30.3→2.30.4, `openblas` 0.3.32→0.3.33, `pycurl` 7.45.7→7.46.0, `python-numpy` 2.4.4→2.4.6, `python-pandas` 3.0.2→3.0.3, `slirp4netns` 1.3.3→1.3.4, `vulkan-compute-tools` 1.4.341→1.4.352.
- **desktops/** (20): `aquamarine` 0.10.0→0.11.0, `cups` 2.4.16→2.4.19, `elogind` 255.22→255.25, `glslang` 16.2.0→16.3.0, `harfbuzz` 14.1.0→14.2.0, `hunspell` 1.7.2→1.7.3, `hwdata` 0.406→0.407, `kitty` 0.46.2→0.47.0, `libblockdev` 3.4.0→3.5.0, `libde265` 1.0.18→1.1.0, `libheif` 1.21.2→1.22.2, `libusb` 1.0.29→1.0.30, `libxmlb` 0.3.26→0.3.27, `minizip` 4.1.0→4.2.1, `pipewire` 1.6.3→1.6.6, `sdbus-cpp` 2.2.1→2.3.1, `tree-sitter` 0.26.8→0.26.9, `vulkan-headers` 1.4.349→1.4.352, `vulkan-loader` 1.4.349→1.4.352, `yazi` 26.1.22→26.5.6.
- **edge/ + network/** (2): `dhcpcd` 10.3.1→10.3.2 (both recipes).
- **browser/** (1): `midori` 11.6.5.1→11.8 (npm build; latest *release* — the `v12` git tag is unpublished). Its `agnos-defaults.patch` should be re-validated against 11.8 at build time.

`base/llvm` (22.1.x patch), `base/boost` (minor), and `desktops/elogind` were the three larger/corrected items pulled forward from the deferred set after confirming their build steps reference no hardcoded version paths; each SHA was verified against the full source tarball (llvm ≈159 MB). `elogind` was corrected to **255.25** — its `releases/latest` (the 257.x git tags are not published releases); the prior recipe also pointed at a non-existent `V255.22` tag, now a canonical `archive/refs/tags/v255.25` URL. `base/protobuf` 34.1→35.0 was likewise cleared from the deferred set after confirming it is safe: its three dependents (`agnosai`, `ifran`, `containerd`) use protobuf only as a build-time `protoc` (backward-compatible codegen — containerd is Go and vendors its own runtime, no libprotobuf ABI linkage), and the pinned `abseil-cpp` 20260107.1 satisfies protobuf 35's minimum (`-Dprotobuf_ABSL_PROVIDER=package`).

### Third-party — AI/ML stack

Bumped to current `releases/latest`, SHAs verified against the full source tarballs (pytorch ≈410 MB, onnxruntime ≈271 MB downloaded + hashed). These move together coherently (vllm depends on pytorch + transformers): `ai/python-transformers` 5.5.4→5.9.0 and `ai/vllm` 0.19.0→0.21.0 (pure `pip install .`), `ai/ollama` 0.20.7→0.24.0 (`go build`), `ai/python-pytorch` 2.11.0→2.12.0 and `ai/onnxruntime` 1.24.4→1.26.0 (generic `cmake … -DCMAKE_BUILD_TYPE=Release` / `make` — build flags unchanged across the minor bump; CI/takumi validates the actual compile).

### Third-party — not bumped (with rationale)

**`browser/brave` was not bumped — release-channel mismatch.** Brave's GitHub tags interleave channels: the latest *stable* (`releases/latest`) is **v1.90.124** (Chromium 148), which is *older* than the recipe's current **1.91.64** (itself a beta-channel tag), while the drift-detected **v1.93.1** is a **Nightly**. Bumping to 1.93.1 would ship a nightly; moving to current stable would be a downgrade. Left unchanged pending a decision on which Brave channel AGNOS tracks — and it needs a real Chromium-scale build to validate either way.

Two deliberate non-bumps: **`base/openssl` + `edge/openssl` stay on 3.5.6** — that is the latest 3.5.x patch (no 3.5.7 exists) and the only newer release is the **4.0.0 major**, which is the wrong track for a base distro pinned to the OpenSSL LTS line; a 4.0 migration is its own project. **`base/sysvinit` stays on 3.14** — the 3.15 git tag has no published release asset (404), so 3.14 remains the latest *released* version.

### Third-party — filtered as false positives (no change)

The raw max-tag sweep flagged these, but each recipe is already on the latest stable; the "newer" hit was a pre-release, an unrelated subproject/legacy tag, or a different release line: `redis7` (`twitter-20100825`), `desktops/opus` (`draft-15`), `desktops/icu` (`brs/…` branch), `desktops/libva` (`staging-…`), `desktops/libjpeg-turbo` (`jpeg-10` API tag), `desktops/msgpack-c` (recipe tracks the `c-` line, not `cpp-`), `desktops/wxwidgets` (`BKFILE_…`), `network/libnl` (already 3.12.0), `base/c-ares` (`curl-7_19_4`), `base/ninja` (`release-120715`), `base/shadow` (`20001016`), `base/squashfs-tools` (`CVE-…`), `base/bun` (canary date tag), `ai/rocm` (`therock-…` build-system tag).

## [1.0.1] - 2026-04-28

A maintenance / drift-cleanup release. No new categories, no semantic changes to the recipe schema. Driven by a P(-1)-style audit pass: the Cyrius toolchain bumped from 5.2 → 5.7.x; AGNOS-native packages that ported from Rust → Cyrius upstream had their recipes updated to match; static sweeps for header drift, naming convention, hardening, broken release_asset globs, and stale cc2 references; root-level `ifran.cyml` moved into `ai/`. Validator clean across all 562+ recipes.

### Cyrius toolchain bump (2026-04-28)

- **`base/cyrius.cyml`** 5.2.0 → **5.7.25**. Tarball SHA256 verified (`5d964a2e...`) against the live `cyrius-5.7.25-x86_64-linux.tar.gz` release. Install now ships two new binaries that landed during the 5.3–5.7 cycle: `cyriusly` (workspace runner) and `cyrld` (linker driver). Hardening flags populated (`pie`, `fullrelro`, `fortify`, `stackprotector`, `bindnow`) — previous recipe carried an empty `hardening = []` even though the upstream build links these by default.
- **`marketplace/cyrius.cyml`** rewritten on top of the bump. Header was stuck on the pre-self-hosting era ("v0.1.0 / cc2 / asm / cyrb / Assembly up. No Rust."); now reflects the 5.7.x toolchain. Install copies the full set (`cc5`, `cyrius`, `cyrc`, `cyrfmt`, `cyrlint`, `cyrdoc`, `cyriusly`, `cyrld`, `ark`, helper scripts, asm seed, stdlib). `release_asset` glob fixed (`*-x86_64-linux.tar.gz`, the actual upstream pattern; was the never-matching `*-linux-amd64.tar.gz`). Dropped the `rust` group tag (Cyrius is fully self-hosted — no Rust dep at any layer). Hardening populated. SHA256 verified (`5d964a2e...`).

### Language updates — Rust → Cyrius ports

Three marketplace recipes had stale `build = ["rust"]` deps and `groups = [..., "rust"]` tags from before the upstream Cyrius ports landed. Build commands updated to `cyrius build` / `cyrius test`, deps swapped to `cyrius`, group tag swapped to `cyrius`. Headers fixed (each was citing the last Rust version even though `version` had been bumped past the port).

- **`marketplace/kybernet.cyml`** 1.0.1 → **1.0.2**. Header `Lib: kybernet = "0.51.0" in Cargo.toml` replaced with the actual current language line. `release_asset` glob fixed to `*-src.tar.gz`. SHA256 verified (`8a9dc9a3...`). Build switched from `cargo build --release` / `cargo test --workspace` to `cyrius build` / `cyrius test src/test.cyr`.
- **`marketplace/daimon.cyml`** 1.1.1 → **1.1.4**. Upstream README documents the port: 9,724 LOC Rust → 4,141 LOC Cyrius, 181 KB binary. Recipe header reflects this. `release_asset` glob fixed to `*-src.tar.gz` (was the never-matching `*-linux-amd64.tar.gz`). Dropped `openssl` from runtime+build deps — Cyrius `sandhi` stdlib module handles TLS, no openssl link. SHA256 verified (`132d83a2...`).
- **`marketplace/vidya.cyml`** 2.1.0 → **2.3.0**. Header `Lib: vidya = "1.0.0" in Cargo.toml` replaced. Upstream `cyrius.cyml` builds `src/main.cyr` → `build/vidya`; recipe now installs that bin plus the read-only content corpus to `/usr/share/vidya/content`. `runtime` switched from `rust-crate` to `native-binary`. Two Landlock blocks added (`/usr/share/vidya` ro, `/tmp` rw) matching daimon's modern sandbox shape. `release_asset` glob fixed to `*-src.tar.gz` (was `"source"`). SHA256 verified (`3359cd66...`).

### base/kybernet build flow

- **`base/kybernet.cyml`** 1.0.1 → **1.0.2**. Build switched from the direct-pipe `cat src/main.cyr | cc5 > build/kybernet` to `cyrius build`. The 1.0.x source tree carries `cyrius.cyml` + `cyrius.lock` with stdlib/agnosys/sakshi/sigil deps that the bare `cc5` pipe cannot resolve; the modern build tool is required. SHA256 verified (`8a9dc9a3...`).

### Added — base OS items (cat / vi-vim counterparts)

Two AGNOS-native CLI tools promoted from "nice to have" to first-class base recipes, sitting alongside `coreutils`/`less` rather than in marketplace. Both ship as prebuilt x86_64 tarballs (same pattern as `base/cyrius`) so they have no build deps and are installable any time after glibc is up.

- **`base/owl.cyml`** — owl 1.1.9. `cat` replacement: pipe-friendly, line numbers, syntax highlighting (eleven starter grammars), git-aware decorations, hex/binary mode, auto-paging. Decorations switch off automatically when stdout is not a TTY. Installed bin to `/usr/bin/owl`, grammars to `/usr/share/owl/grammars/`. SHA256 verified (`b21a9f21...`).
- **`base/cyim.cyml`** — cyim 1.2.1. `vi`/`vim` replacement: modal editor in the vi → vim → nvim → cyim lineage, written in Cyrius — no Lua, no Vimscript, no plugin sandbox. Drives both interactive (`cyim <file>`) and non-interactive scripted edits (`--write`, `--replace`, `--replace-all`, `--batch`, `--grep`, `--expect`/`--expect-N`). Installed bin to `/usr/bin/cyim`, grammars to `/usr/share/cyim/grammars/`. SHA256 verified (`40f75f09...`).

Note: not added to `build-order.txt` — base/cyrius and base/kybernet aren't in build-order either; that file currently covers only the LFS bootstrap chain. Adding the Cyrius-language toolchain + downstream tools (cyrius, kybernet, owl, cyim) into a new tier 1f is tracked separately in roadmap.

### Removed

- **`marketplace/cyrius-seed.cyml`** — upstream `MacCracken/cyrius-seed` repo returns 404 (deleted upstream). The seed/asm bootstrap flow is now subsumed by the `asm` binary inside the cyrius release tarball (installed by `base/cyrius.cyml` to `/usr/lib/cyrius/asm`). References in `CHANGELOG.md` and `docs/development/roadmap.md` placeholder lists trimmed.

### Recipe sweep — Tier A (drift fixes, 2026-04-28)

Static audit pass across all 562 recipes. Findings categorised; mechanical, zero-risk fixes applied.

- **Header/version drift — 32 recipes.** Header comments cited a stale `vX.Y.Z` from before the last bump. Patched only the tightly-scoped idioms (`Status: Released — vX.Y.Z`, `Lib: name = "X.Y.Z" in Cargo.toml`, `Pre-release vX.Y.Z`, `Hardened — vX.Y.Z`) so prose mentions of unrelated semvers (e.g. `802.15.4` in `edge/esp32-agent.cyml`, `MQTT 3.1.1`, `0.8.5` referencing the old redhat libcap-ng mirror) were left alone. First pass over-matched and was reverted; second pass uses anchored patterns. Files: aethersafta, agnos-kernel, agnoshi, agnostik, agnosys, ai-hwaccel, argonaut, ark, avatara, bote, dhvani, hisab, hoosh, ifran, itihas, kiran, majra, nein, nous, phylax, ranga, sankhya, shabda, shabdakosh, sharira, shravan, sigil, svara, szal, t-ron, tarang, yukti.
- **`marketplace/agnos-kernel.cyml` — cc2 → cc5.** Install step `cat kernel/agnos.cyr | cc2 > build/agnos` retired the cc2 binary that was removed during the 5.x toolchain transition. Swapped to cc5 to match `base/cyrius`. Note: this recipe still has additional drift (version 1.22.0 vs upstream 1.26.1; `release_asset = "agnos-*-x86_64.tar.gz"` glob never matched — actual asset is `agnos-1.26.1-src.tar.gz` + bare `agnos-x86_64`); deferred to Tier B alongside the cargo→cyrius port sweep.

### Recipe sweep — Tier C (housekeeping, 2026-04-28)

- **`pip` stripped from build deps — 14 recipes.** Per CLAUDE.md naming conventions: `pip` ships with `python`; recipes should depend on `python` and invoke `python -m pip` in build scripts. Cleaned: `base/gyp.cyml`, `marketplace/agnostic.cyml`, and 12 `ai/*` recipes (cython, huggingface-hub-cli, jupyter-server, pycups, pycurl, python-numpy, python-pandas, python-pytorch, python-safetensors, python-scipy, python-transformers, vllm). The `base/pip.cyml` meta-package is preserved (allows bazaar recipes that list `pip` as a dep to resolve).
- **`pkg-config` → `pkgconf` in build deps — 14 recipes.** Canonical AGNOS dep name is `pkgconf` (which already installs `/usr/bin/pkg-config` as a compat symlink). Cleaned: 7 browser recipes (brave, chromium, falkon, firefox, librewolf, midori, zen), both database recipes (postgresql17, redis7), all four python recipes (3.12, 3.13, 3.13t, 3.14), and `ifran.cyml`. The `base/pkg-config.cyml` meta-package is preserved.
- **`npm` stripped from `browser/midori.cyml`.** Deps already listed `nodejs`; per convention `npm` ships with it.
- **Hardening flags filled — 2 base recipes.** `base/firecracker.cyml` and `base/gvisor.cyml` ship binaries but had `hardening = []`. Populated with the standard set (`pie`, `fullrelro`, `fortify`, `stackprotector`, `bindnow`). `base/agnos-kernel.cyml` was left as `hardening = []` — userspace hardening flags don't apply to a bare-metal kernel binary.

### Tier B — Rust→Cyrius port discovery (2026-04-28)

Probed 98 marketplace MacCracken/* recipes against upstream HEAD trees (`cyrius.cyml` / `cyrius.toml` / `Cargo.toml` presence). Classification, used to scope the port pass:

- **26 confirmed ported to Cyrius** — upstream has a Cyrius manifest at root, no `Cargo.toml`. 16 use the older `cyrius.cyml` naming, 10 use the newer `cyrius.toml`.
- **64 confirmed still Rust** — `Cargo.toml` only. Existing `cargo build` recipes are correct, no action.
- **8 ambiguous** — split into roadmapped placeholders (`abacus`, `mela`, `murti`, `samay`, `seema`, `tanur` — intentionally unscaffolded, not deletion candidates) and container-shaped repos (`bullshift`, `photisnadi`) that have neither `Cargo.toml` nor a Cyrius manifest at root, only a `Dockerfile`. The container set needs a separate "container-recipe shape" decision before any rewrite.

### Tier B — set 1 ports (16 cyrius.cyml recipes, 2026-04-28)

Recipes ported from `cargo build` / `build = ["rust"]` / `groups = [..., "rust"]` to the daimon/kybernet/vidya template: `cyrius build` / `build = ["cyrius"]` / `groups = [..., "cyrius"]`. `release_asset` globs corrected to actual upstream patterns. SHA256 verified against API-reported digests for every recipe (and against fresh tarball download for the 5 bare-binary ports). Marketplace metadata, sandbox config, and Landlock blocks preserved verbatim from prior recipe.

**Bare-binary installs (upstream ships a single `<name>` file):**
- `marketplace/agnova.cyml` 0.1.0 (rebuild — same version, now Cyrius). SHA `6fdbbf3a…`.
- `marketplace/ark.cyml` 0.8.0. SHA `863ff4b3…`.
- `marketplace/hisab.cyml` 2.2.0. SHA `9e9c598c…`.
- `marketplace/phylax.cyml` 1.0.0. SHA `de88bc11…`.
- `marketplace/shakti.cyml` 0.2.2. SHA `a062ad62…`.

**Source-tarball builds (`<name>-<version>-src.tar.gz`, build with `cyrius build`):**
- `marketplace/abaco.cyml` 2.1.0 → **2.2.0**. SHA `5a153ec1…`.
- `marketplace/agnostik.cyml` 0.96.0 → **1.0.0**. SHA `5c6b04ac…`. Library — install ships source tree to `/usr/lib/agnostik/` for inspection (real consumers use `[deps.agnostik]` git deps).
- `marketplace/agnosys.cyml` 0.97.2 → **1.0.2**. SHA `71ebd125…`. Library — same install pattern.
- `marketplace/argonaut.cyml` 1.2.0 → **1.5.0**. SHA `96447ebe…`. Used by kybernet for service management.
- `marketplace/libro.cyml` 0.92.0 → **2.0.5**. SHA `0f2226d5…`. Upstream output is `./libro` (not `build/libro`).
- `marketplace/mabda.cyml` 1.0.0 → **2.5.0**. SHA `bd4d05bf…`. Pure library — `cyrius build` only produces a smoke test (`build/mabda_smoke`); recipe ships source tree, not a binary.
- `marketplace/majra.cyml` 2.2.0 → **2.4.1**. SHA `9732fb92…`.
- `marketplace/yukti.cyml` 1.2.0 → **2.1.1**. SHA `a783b379…`.

**Plain tarball (no `-src` suffix):**
- `marketplace/sigil.cyml` 2.4.2 → **2.9.4**. SHA `b4d8d639…`. Upstream tarball is `sigil-2.9.4.tar.gz`.

**Binary tarball:**
- `marketplace/nous.cyml` 1.1.1 (rebuild — same version, now Cyrius). SHA `d7c2ab64…`. Upstream ships a prebuilt `nous-1.1.1-x86_64-linux.tar.gz`.

**Scaffold-state (no published release):**
- `marketplace/takumi.cyml` — kept at 0.1.0 with `# TODO` SHA. Upstream has a default-branch `cyrius.cyml` at 0.8.0 but no published release yet. Switched groups + build deps to Cyrius preemptively; release_asset glob set to anticipated `takumi-*-src.tar.gz` pattern.

### Tier B — what's left

### Root /ifran.cyml moved to ai/ (2026-04-28)

The system-package recipe for ifran was sitting at the repo root — illegal layout per the category-subdirectory convention; predated this audit cycle. Moved via `git mv ifran.cyml ai/ifran.cyml` (history preserved). The marketplace bundle variant `marketplace/ifran.cyml` is unchanged. Ifran upstream is still Rust (`Cargo.toml` at HEAD, no Cyrius manifest), so the recipe stays on `cargo build` for now — port lands when upstream cuts a Cyrius release.

### base/bazaar — Cyrius port (2026-04-28)

- **`base/bazaar.cyml`** 2026.3.18 → **1.0.0** (upstream's first stable release, versioned in lockstep with zugot tags). SHA `85e7c5d5…` verified against `bazaar-1.0.0-src.tar.gz`. Source switched from `local = true` to the upstream release tarball. Build switched from `cargo build --release --bin bazaar` to `cyrius build`. Output binary renamed from `bazaar` to `bazaar-validate` (matches upstream `cyrius.cyml` `output = "build/bazaar-validate"`); the now-meaningless `ark-bazaar` symlink dropped (user-facing commands ride on `ark bazaar <subcommand>` rather than a standalone binary). Default `/etc/agnos/bazaar/config.toml` heredoc preserved verbatim.

### agnos-kernel bump (2026-04-28)

- **`base/agnos-kernel.cyml`** 1.22.0 → **1.26.1**. SHA `c2b82039…` verified against `agnos-1.26.1-src.tar.gz`. Build switched from the bare `cat kernel/agnos.cyr | cc5 > build/agnos` pipe to `cyrius build` (upstream `cyrius.cyml` declares `entry = "kernel/agnos.cyr"`, `output = "build/agnos"`; no external deps so `cyrius deps` is a no-op). Comment added explaining `hardening = []` is intentional for a freestanding multiboot1 ELF.
- **`marketplace/agnos-kernel.cyml`** 1.22.0 → **1.26.1**. SHA `c2b82039…`. `release_asset` glob `agnos-*-x86_64.tar.gz` (never matched — upstream ships `*-src.tar.gz` + bare `agnos-x86_64`) corrected to `agnos-*-src.tar.gz`. Build step swapped from `cat | cc5` to `cyrius build`. Same `hardening = []` annotation.

### Tier A follow-up — Status header drift (2026-04-28)

The first Tier A pass (anchored on `Status: Released — vX.Y.Z[.]$`) missed Status lines that have prose appended after the version (`v0.29.4 on crates.io + GitHub.`, `v0.29.4 (linux amd64 + arm64).`, etc.). Caught in a second sweep:

- `marketplace/ranga.cyml`: `Status: Published — v0.29.4 on crates.io + GitHub` → `v1.0.0`
- `marketplace/selah.cyml`: `Status: Published — v0.29.4 (linux amd64 + arm64)` → `v2026.3.17`
- `marketplace/tarang.cyml`: `Status: Published — v0.21.3 on crates.io + GitHub` → `v2026.3.18`
- `marketplace/tazama.cyml`: prose cross-ref `tarang 0.20.3` → `tarang 2026.3.18` (tarang's bumped version, not tazama's own)

### Tier B — set 2 ports (10 cyrius.toml recipes, 2026-04-28)

Same daimon/kybernet/vidya template applied. Set 2 upstreams overwhelmingly publish a single bare-binary asset (`<name>` with no version/platform suffix), so 9 of 10 are bare-bin installs. Marketplace metadata, sandbox config, and Landlock blocks preserved verbatim from prior recipe; SHA256 verified against API digest and spot-checked against fresh downloads.

**Bare-binary installs:**
- `marketplace/agnoshi.cyml` 1.0.0 (rebuild — same version, now Cyrius). SHA `af7aae40…`. Bin renamed `agnsh` → `agnoshi` to match upstream asset name.
- `marketplace/ai-hwaccel.cyml` 2.0.0 (rebuild). SHA `121e90dd…`.
- `marketplace/avatara.cyml` 2.3.0 (rebuild). SHA `f2b2e085…`.
- `marketplace/bote.cyml` 2.5.1 (rebuild). SHA `2aa7359d…`.
- `marketplace/hoosh.cyml` 2.0.0 (rebuild). SHA `ba417a91…`. Dropped `openssl` runtime dep — upstream `cyrius.toml` confirms TLS via `sandhi` stdlib, no openssl link.
- `marketplace/itihas.cyml` 2.2.0 (rebuild). SHA `1501480a…`.
- `marketplace/kavach.cyml` 2.0.0 → **3.0.0**. SHA `7876b104…`.
- `marketplace/nein.cyml` 1.0.0 (rebuild). SHA `68b5d020…`.
- `marketplace/t-ron.cyml` 2.0.0 (rebuild). SHA `69e28fe9…`.

**Source-tarball build:**
- `marketplace/shravan.cyml` 2.3.2 (rebuild). SHA `c9e4d6ce…`. `cyrius build` → `build/shravan`.

This closes the rust→cyrius port pass for the 26 confirmed-ported recipes (16 cyml in set 1 + 10 toml in set 2).
- **Container-shaped (2)** — `bullshift`, `photisnadi`. Need a recipe-shape decision (do we install upstream's container, or run a build with the upstream Dockerfile, or something else?).
- **Roadmapped placeholders (6)** — `abacus`, `mela`, `murti`, `samay`, `seema`, `tanur`. Per the user, intentionally unscaffolded — leave the recipes as-is.

### Notes

- Cyrius 5.7.26 was tagged but swallowed by an in-flight 5.7.27; this bump targets 5.7.25 (latest published at audit time, 2026-04-28T19:12Z). Re-bump once 5.7.27 lands.

## [1.0.0] - 2026-04-17

First stable release. Zugot grew from ~426 recipes to **561** across a single
hardening + expansion pass; introduced the validator + CI; formalized naming
conventions; delivered a dated CVE audit; renamed the `desktop/` directory to
`desktops/` reflecting that Wayland won't be the only desktop AGNOS ships.

See `docs/adr/` for the architectural decisions that shaped this release.

### Security (audit 2026-04-17)

See `docs/audit/2026-04-17.md` for the full report.

- **`base/gnupg.cyml`** 2.4.9 → **2.5.18** (CVE-2026-24881, CVSS 9.8 CRITICAL — stack-based buffer overflow in gpg-agent CMS `PKDECRYPT` path, crafted S/MIME `EnvelopedData` → RCE/DoS). The 2.4.x stable branch is EOL 2026-06-30 and upstream did not backport; migration to 2.5.x was the only path. SHA256 verified from fresh download (`0dbd64e0...`).

### Security — monitor (no upstream fix yet)

Seven packages at the latest upstream but with known unpatched CVEs. Documented in `docs/development/roadmap.md` §P2 and `docs/audit/2026-04-17.md`:

- `base/sudo.cyml` 1.9.17p2 — CVE-2026-35535 (CVSS 7.4, local privesc)
- `base/glibc.cyml` 2.43 — CVE-2026-4046 (CVSS 7.5, iconv DoS)
- `desktops/libtiff.cyml` 4.7.1 — CVE-2025-61144/61143
- `base/binutils.cyml` 2.46.0 — CVE-2026-4647 + older (RHSA backports available)
- `desktops/gstreamer.cyml` + plugins 1.28.2 — CVE-2026-5056 (CVSS 7.8 local)
- `base/libarchive.cyml` 3.8.7 — CVE-2026-4111 (RAR5 DoS)
- `desktops/libxslt.cyml` 1.1.45 — CVE-2025-11731 + 3 older (project under-maintained)

Plus `base/nss.cyml` 3.122.1 — CVE-2026-2781/4727 status unclear until Mozilla release notes publish.

### Documentation

- New `docs/audit/2026-04-17.md` — first external-research CVE audit. Structure is reusable: one file per audit pass, dated. Next cycle ~2026-05-15.
- New `VERSION` file (`1.0.0`).
- New `docs/adr/` — Architecture Decision Records for the major design calls (CYML format, `desktops` pluralization, naming conventions, validator+CI, dated audit cadence).

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
abacus, aegis, aethersafha, agnova, jantu, jivanu, kavach, libro, mabda, mastishk, mela, mneme, muharrir, murti, nazar, salai, samay, seema, shakti, takumi, tanur

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
