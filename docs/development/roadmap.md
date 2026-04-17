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

## P2 · Recipes needing upstream transition handling

These work at the pinned version but upstream has changed something structural (naming scheme, source URL format, version scheme):

| recipe | current | upstream latest | issue |
|---|---|---|---|
| `base/libcap-ng.cyml` | 0.8.5 | 0.9.3 | Redhat mirror stops at 0.8.5; GitHub archive lacks pre-generated `configure` (need `autogen.sh` + autotools in build deps) |
| `desktop/nvidia-driver.cyml` | 570.133.07 | 595.58.03 (prod stable) | Proprietary binary; bumping requires deliberate branch/ML/beta channel choice |
| `desktop/zathura.cyml` | 0.5.14 | 2026.03.27 | Upstream switched from semver to date-based versioning; URL format rework needed |
| `desktop/girara.cyml` | 0.4.5 | 2026.02.04 | Same as zathura — date-based versioning switch |

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

### Validator — cross-check zugot against bazaar

`noted-issues-bazaar-finds.md` cites a Python cross-check script. Two follow-ups:

1. **Wire it into zugot CI** as a `validate_recipes` step that fails the PR if:
   - Any `[depends].runtime` or `[depends].build` entry references a package neither in zugot nor bazaar
   - Any `sha256` field is an unchanged placeholder (`""` without a `# TODO` comment, or `"VERIFY"`)
   - Any filename doesn't match its `[package].name`
2. **Wire it into bazaar CI** (upstream request) as `--check-against ../zugot` mode. The script already exists; it just needs a workflow file.

### TOML-compatible parsing

Cyrius's current CYML parser is lax enough to accept invalid TOML escape sequences (e.g. `\.` inside `"""..."""`). Strict consumers (Python `tomllib`, Rust `toml` crate) fail on these. We found and fixed 4 in pass 2. A lint step should scan for:
- Invalid backslash escapes inside basic strings (`"..."` / `"""..."""`)
- Recommendation: prefer literal strings (`'...'` / `'''...'''`) whenever a multi-line block contains shell or regex code with backslashes

### Roadmap maintenance

This file itself is new. Keep it updated as part of the work loop (CLAUDE.md §9: "update roadmap if applicable"). Close items inline with a `✅ Resolved` marker and a commit/PR link so the audit trail survives.

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
