# Zugot Roadmap

> Consolidated list of open work items across zugot's recipe tree.
> Not a feature backlog — a snapshot of drift, TODOs, and process gaps surfaced during the current audit pass.
>
> **Last updated:** 2026-04-16

## Legend

- **Priority 1** — blocks downstream builds or has known incorrect state
- **Priority 2** — stale or out-of-convention, should update but won't break
- **Priority 3** — tooling/process work

---

## P1 · Broken / stale recipes needing coordinated work

### ✅ `base/cyrius.cyml` — resolved 2026-04-17

Rewritten: 0.9.0 → **5.2.0**, switched from `release_asset = "cc2"` pattern to direct `url` pointing at the pre-built `cyrius-5.2.0-x86_64-linux.tar.gz` release tarball, SHA256 populated. Install now copies the full toolchain (`cc5`, `cyrius`, `cyrc`, `cyrfmt`, `cyrlint`, `cyrdoc`, `ark`, helper scripts, stdlib) from the pre-built tarball — no bootstrap-from-source needed for distribution builds.

Downstream `make = "... | cc2 > ..."` references in `kybernet` and `agnos-kernel` updated to `cc5`.

### ✅ `base/kybernet.cyml` — resolved 2026-04-17

Bumped 0.9.0 → **1.0.1**. Switched from `release_asset = "kybernet-x86_64"` (pre-built binary) to building from the `kybernet-1.0.1-src.tar.gz` release tarball via `cc5`. SHA256 populated.

### ✅ `base/agnos-kernel.cyml` — resolved 2026-04-17

Bumped 1.0.0 → **1.22.0**. Kept recipe name `agnos-kernel` (it's the kernel component of the broader AGNOS OS) but clarified in header comment that `MacCracken/agnos` is the upstream repo. Switched from `release_asset` → source tarball URL (`agnos-1.22.0-src.tar.gz`), SHA256 populated. Build uses `cc5` (was `cc2`).

### ✅ `base/gvisor.cyml` — resolved 2026-04-17

Pinned from `version = "latest"` to **20260413.0** (gVisor's weekly date-based release). URL now points at `/release/20260413/x86_64/runsc` instead of `/release/latest/...` — SHA256 will no longer drift silently. Bump deliberately; re-verify SHA when advancing to a newer date.

---

## P1 · Bazaar cross-ref — SHA population backlog

The following recipes build fine but have `sha256 = ""` with a `# TODO` comment — they need manual population before any release/distribution build:

### Base / desktop

| recipe | status | reason |
|---|---|---|
| `browser/chromium.cyml` | **still TODO** | tarball ~6GB, too large to auto-download; populate SHA from a dev machine before any release build |
| `base/boost.cyml` | ✅ resolved 2026-04-17 | 110MB tarball fetched, SHA256 populated |
| `desktop/luajit.cyml` | ✅ resolved 2026-04-17 | pinned to commit `18b087cd` (v2.1 branch snapshot 2026-04-17); version field updated to `2.1-18b087cd`; bump periodically |

### Marketplace

Most `marketplace/*.cyml` recipes have `sha256 = ""` with a `# TODO` comment. Convention is that SHAs are populated from the release asset at build time, but a periodic sweep to populate SHAs for all tagged releases would improve reproducibility. See `CHANGELOG.md` for the 39 marketplace recipes bumped in the current pass; SHAs for those are still TODO.

---

## P2 · Recipes needing upstream transition handling — ✅ resolved 2026-04-17

All four transitions applied:

| recipe | change | notes |
|---|---|---|
| `base/libcap-ng.cyml` | 0.8.5 → **0.9.3** | switched to GitHub archive URL (redhat mirror is stuck); added `autogen.sh` pre_build + `autoconf`/`automake`/`libtool` build deps. SHA256 verified. |
| `desktop/nvidia-driver.cyml` | 570.133.07 → **595.58.03** | production-stable channel chosen; SHA256 verified from download.nvidia.com |
| `desktop/zathura.cyml` | 0.5.14 → **2026.03.27** | upstream switched from semver to date-based versioning; version + URL + SHA updated |
| `desktop/girara.cyml` | 0.4.5 → **2026.02.04** | same date-based transition |

---

## P2 · Marketplace — recipes AHEAD of upstream (verify intent)

These have recipe versions newer than the current upstream tag. Likely pre-release staging, but worth confirming the version number isn't a typo:

- `marketplace/secureyeoman.cyml` — recipe `2026.3.28` vs upstream `2026.3.19`
- `marketplace/secureyeoman-agent.cyml` — same mismatch
- `marketplace/secureyeoman-lite.cyml` — same mismatch
- `marketplace/secureyeoman-primary.cyml` — same mismatch
- `marketplace/secureyeoman-sqlite.cyml` — same mismatch
- `marketplace/stiva.cyml` — recipe `2.0.0` vs upstream `1.0.0`

---

## P2 · Marketplace — no upstream tags yet (22 recipes)

These reference `MacCracken/*` repos that `git ls-remote` returns no tags for. Either the repo is new/empty or the project uses a branch-based release model. Current recipe versions are preserved until the upstream cuts a first tagged release:

`abacus`, `aegis`, `aethersafha`, `agnova`, `cyrius-seed`, `jantu`, `jivanu`, `kavach`, `libro`, `mabda`, `mastishk`, `mela`, `mneme`, `muharrir`, `murti`, `nazar`, `salai`, `samay`, `seema`, `shakti`, `takumi`, `tanur`

Revisit this list periodically and bump as releases land.

---

## P3 · Tooling / process

### ✅ Validator + CI — resolved 2026-04-17

Delivered as `scripts/validate_recipes.py` + `.github/workflows/validate-recipes.yml`. The script checks four classes of problem:
1. TOML/CYML parse errors (via stdlib `tomllib` — catches invalid backslash escapes like `\.` that the lax Cyrius parser accepts; **covers the "TOML-compatible parsing" item below too**)
2. Filename ≠ `[package].name` mismatches
3. Empty `sha256` without a `# TODO` comment
4. Unresolved deps in `[depends].runtime` / `[depends].build`

Usage:
```sh
scripts/validate_recipes.py                            # zugot-only
scripts/validate_recipes.py --check-against ../bazaar  # cross-check bazaar
```

First run against the current zugot tree surfaced **151 legitimate issues** — see "Follow-ups surfaced by the validator" below.

### Roadmap maintenance — ongoing

Keep this file updated as part of the work loop (CLAUDE.md §9: "update roadmap if applicable"). Close items inline with `✅ Resolved 2026-MM-DD` so the audit trail survives.

---

## Follow-ups surfaced by the validator (next roadmap sweep)

First run of `scripts/validate_recipes.py` flagged 151 issues. Grouped for the next pass:

### Naming conventions not yet applied to existing recipes
9 `ai/*.cyml` recipes still declare `python3` instead of `python` (CLAUDE.md rule 2):
`huggingface-hub-cli`, `jupyter-server`, `python-numpy`, `python-pandas`, `python-pytorch`, `python-safetensors`, `python-scipy`, `python-transformers`, `vllm`

Browser and some marketplace recipes still use `libpipewire` instead of `pipewire`.

### Genuinely missing recipes (new packages needed)
| dep | referenced by | scope |
|---|---|---|
| `gfortran` | lapack, openblas, python-scipy | new `base/` recipe (could be a meta-package pointing at `gcc` since gfortran ships as part of the GCC build) |
| `docbook-xsl` | xmlto | new `base/` recipe |
| `brotli` | nodejs | new `base/` recipe |
| `c-ares` | nodejs | new `base/` recipe |
| `gyp` | nss | new `base/` recipe (Chromium's build-config generator) |
| `libseat` | aquamarine | alias/meta-package — `seatd` provides `libseat` (same pattern as pkgconf→pkg-config) |

### Filename/package-name mismatches
To be enumerated from validator output during the next sweep.

---

## Resolved this pass (2026-04-16)

Summary of what the current audit pass closed; kept here so the next roadmap refresh starts from accurate state:

- ✅ **CYML format conversion** — all 426 recipes renamed `.toml` → `.cyml`
- ✅ **Group rename** — `"desktop"` → `"desktops"` across 130 recipes
- ✅ **Bazaar cross-ref** — 91 → 0 unresolved deps across three passes; added 100+ new recipes (Qt 6 stack, GTK/GNOME ecosystem, XFCE, Hyprland, A/V codecs, C/C++ system libs, app-specific, meta-packages)
- ✅ **4 TOML parse errors** fixed (shadow, nss, noto-fonts, kernel)
- ✅ **Naming conventions** codified in CLAUDE.md (9 rules)
- ✅ **5 latent bugs** caught during base audit (fontconfig URL 404, zlib wrong SHA, binutils URL+SHA, pkgconf phantom version 3.0.0, util-linux wrong SHA)
- ✅ **Full recipe audit** across all 10+ categories (database, python, network, browser, ai, edge, sandbox, base, desktop, marketplace)
