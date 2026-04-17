# Noted Issues — Bazaar Finds

> Cross-reference of bazaar (community recipes) deps against zugot (official recipes). Anything below is a dep that bazaar recipes reference but zugot does not provide — meaning the recipe will fail to resolve at install time.

## Status

| Pass | Date | Zugot HEAD | Bazaar HEAD | Unresolved unique | Unresolved refs |
|---|---|---|---|---:|---:|
| 1 | 2026-04-16 | `f2ee273` | `579ed38` | 91 | 135 |
| 2 | 2026-04-16 | `f2150bc` | `39019cc` | 5 | 13 |
| 3 | 2026-04-16 | `efe0c7a` | `39019cc` | **2** | **2** |

Pass 2→3: zugot added `pip`, `npm`, `pkg-config`, and fixed all 4 TOML parse errors. Well done. Only 2 refs left, both in a single bazaar recipe.

## Remaining unresolved — 2 refs

Both are referenced only by `recipes/desktops/system-config-printer.cyml` in bazaar. They're Python bindings for system printing.

| dep | upstream | notes |
|---|---|---|
| `pycups` | [OpenPrinting/pycups](https://github.com/OpenPrinting/pycups) | Python CUPS API binding. Built via `python -m pip install` or setuptools. Depends on `python`, `cups`. |
| `pycurl` | [pycurl.io](http://pycurl.io/) | Python cURL binding. Built via setuptools. Depends on `python`, `curl`, `openssl`. |

Both are small C extensions — each is ~1-2 MB of source. Since zugot has `python` and `cups`/`curl` already, these slot in cleanly.

## Minor finding — filename ≠ package name in zugot

The bazaar validator enforces `filename_basename == [package].name`. Zugot appears to follow the same convention across its 528 recipes, except:

| file | declared `[package].name` |
|---|---|
| `base/python-pip.cyml` | `pip` |
| `base/nodejs-npm.cyml` | `npm` |

Not a blocker — the resolver indexes by `[package].name`, not filename — but inconsistent with the rest of the repo. Two easy fixes: rename files to `base/pip.cyml` / `base/npm.cyml`, or rename packages to `python-pip` / `nodejs-npm` (and update bazaar's refs to match).

## Already absorbed into bazaar (informational)

Naming bugs on bazaar's side — fixed across two rename passes. Listed here so zugot doesn't need to provide the misspellings:

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

**Suggested contributor doc note:** zugot package names follow one convention — runtime package ships headers (no `-dev` split), and `lib` prefix follows upstream project naming (so `curl` but `libsigc++`, `luajit` but `libuv`, `x264` but `libx265` — wait, zugot has both conventions for codecs actually). Worth documenting the canonical name for each commonly-referenced package so contributors don't guess. Contributors coming from Debian/Ubuntu backgrounds tend to reach for `-dev` and `lib-` variants by reflex.

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
