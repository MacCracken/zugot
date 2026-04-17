# Noted Issues — Bazaar Finds

> Cross-reference of bazaar (community recipes) deps against zugot (official recipes). Anything below is a dep that bazaar recipes reference but zugot does not provide — meaning the recipe will fail to resolve at install time.

## Status

| Pass | Date | Zugot HEAD | Bazaar HEAD | Unresolved unique | Unresolved refs |
|---|---|---|---|---:|---:|
| 1 | 2026-04-16 | `f2ee273` | `579ed38` | 91 | 135 |
| 2 | 2026-04-16 | `f2150bc` | `39019cc` | **5** | **13** |

Zugot absorbed 35/40 prioritized gaps in pass 1→2 (9 new packages in `base/`, several new `desktop/`, added `aquamarine`, `hyprcursor`, `hyprwayland-scanner`, `qt6-base`, `seatd`, `pulseaudio`, `libuv`, `tree-sitter`, `oniguruma`, and more). Great progress.

## Remaining unresolved — 5 deps, 13 references

### Needs zugot meta-packages (7 refs)

`pip` and `npm` ship bundled with their parent runtimes (`python`, `nodejs`), so bazaar contributors instinctively list them as deps. Rather than forcing contributors to drop them, **provide thin meta-packages** that depend on the runtime and install the right executable shim.

| dep | refs | recipes | suggested zugot recipe |
|---|---:|---|---|
| `pip` | 6 | yt-dlp, vllm, aider, open-webui, comfyui, pytorch | `python-pip.cyml` — depends only on `python`, installs `/usr/bin/pip` (symlink or shim to `python -m pip`) |
| `npm` | 1 | open-webui | `nodejs-npm.cyml` — depends only on `nodejs`, installs `/usr/bin/npm` (it's already in the tarball, just split into its own package for explicit dep) |

### Still genuinely missing (6 refs)

| dep | refs | recipes |
|---|---:|---|
| `pkg-config` | 4 | podman, libreoffice, ffmpeg, retroarch |
| `pycups` | 1 | system-config-printer |
| `pycurl` | 1 | system-config-printer |

`pkg-config` was on the previous priority list under "build tools" and is the highest-impact remaining gap — it's required at build time by anything using autotools or meson with C deps.

`pycups` and `pycurl` are Python bindings. Either add as `python-cups` / `python-pycurl`, or the bazaar `system-config-printer.cyml` can be changed to pull them via `pip` at install time once the `pip` meta-package lands.

## Also found — 4 TOML parse errors in zugot recipes

These files fail `python -m tomllib` parsing — unescaped backslashes in double-quoted strings (TOML requires `\\` for a literal backslash). My first cross-check silently skipped these recipes, which is why the pass-1 report wrongly listed some packages as missing when they existed.

| file | line | fix |
|---|---|---|
| `base/shadow.cyml` | 29 | escape `\` as `\\` (or use a literal `'...'` string) |
| `base/nss.cyml` | 50 | same |
| `desktop/noto-fonts.cyml` | 30 | same |
| `edge/kernel.cyml` | 75 | same |

These may parse fine in cyrius' current CYML parser (which is more lax) but will break any stricter TOML-compatible consumer. Worth fixing for portability.

## Already absorbed into bazaar (informational)

Naming bugs on bazaar's side — fixed in bazaar across two rename passes (`579ed38`, `39019cc`). Listed here so zugot doesn't need to provide the misspellings:

| was | is now | pass |
|---|---|---|
| `python3` → `python`  | 1 |
| `wayland-dev` → `wayland` | 1 |
| `ncurses-dev` → `ncurses` | 1 |
| `pipewire-dev` → `pipewire` | 1 |
| `openblas-dev` → `openblas` | 1 |
| `wlroots-dev` → `wlroots` | 1 |
| `qt6-base-dev` → `qt6-base` | 1 |
| `libevent-dev` → `libevent` | 1 |
| `libsodium-dev` → `libsodium` | 1 |
| `libx264` → `x264` | 2 |
| `libx265` → `x265` | 2 |
| `pam` → `linux-pam` | 2 |
| `libluajit` → `luajit` | 2 |
| `libcurl` → `curl` | 2 |
| `sigc++` → `libsigc++` | 2 |

**Suggested contributor doc note:** zugot package names use one convention consistently — runtime package ships headers (no `-dev` split), and `lib` prefix follows upstream project naming (so `curl` but `libsigc++`, `libuv` but `x264`). Contributors coming from Debian/Ubuntu backgrounds tend to reach for `-dev` and `lib-` variants by reflex.

## How to regenerate this list

From `~/Repos/bazaar`, against a local zugot checkout:

```python
import pathlib, tomllib, re

def extract_name(p):
    try:
        with p.open('rb') as fh: return tomllib.load(fh).get('package',{}).get('name')
    except:
        m = re.search(r'^name\s*=\s*"([^"]+)"', p.read_text(), re.M)
        return m.group(1) if m else None

def names(root):
    return {n for n in (extract_name(f) for f in pathlib.Path(root).rglob('*.cyml')) if n}

provided = names('/home/macro/Repos/zugot') | names('recipes')
gaps = {}
for f in pathlib.Path('recipes').rglob('*.cyml'):
    with f.open('rb') as fh: d = tomllib.load(fh)
    own = d.get('package',{}).get('name')
    for k in ('runtime','build'):
        for dep in d.get('depends',{}).get(k, []):
            if dep not in provided and dep != own:
                gaps.setdefault(dep, []).append(str(f))
```

Worth wiring this into bazaar's `validate_recipes` as a `--check-against` mode so PRs surface gaps automatically.
