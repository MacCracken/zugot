# Noted Issues — Bazaar Finds

> Cross-reference of bazaar (community recipes) deps against zugot (official recipes). Anything below is a dep that bazaar recipes reference but zugot does not provide — meaning the recipe will fail to resolve at install time.

**Generated:** 2026-04-16
**Bazaar commit:** `579ed38` (after the `python3 → python`, `*-dev → *` rename pass)
**Zugot commit:** `f2ee273` (`aaa8c42 more desktop`, 426 recipes)
**Method:** parse every `.cyml` in both trees, build the union of `[package].name`, then check every `[depends].runtime` and `[depends].build` entry in bazaar against that set.

After this pass: **91 unique deps, 135 references unresolved** (down from 100 unique / 178 references pre-rename).

## Already fixed in bazaar

These were naming bugs on bazaar's side (Debian-style `-dev` split + Python convention). Renamed in bazaar `579ed38`:

| was | is now | hits |
|---|---|---:|
| `python3` | `python` | 22 |
| `wayland-dev` | `wayland` | 14 |
| `ncurses-dev` | `ncurses` | 4 |
| `pipewire-dev` | `pipewire` | 1 |
| `openblas-dev` | `openblas` | 1 |
| `wlroots-dev` | `wlroots` | 1 |
| `qt6-base-dev` | `qt6-base` | 2 |
| `libevent-dev` | `libevent` | 1 |
| `libsodium-dev` | `libsodium` | 1 |

Zugot may want a contributor doc note: **packages do not split `-dev` headers**; the runtime package ships them.

## Suggested priorities for zugot

Ordered by blast radius (number of bazaar recipes blocked):

### 1. Build tools — likely belong in `base/`

These are not optional libraries; they're tools that build systems invoke. Without them, *any* recipe needing them fails its build phase regardless of category. Most distros ship them as build-essentials.

| dep | bazaar refs | recipes |
|---|---:|---|
| `pkg-config` | 4 | podman, libreoffice, ffmpeg, gimp |
| `intltool` | 6 | thunar, xfce-libs, xarchiver, evince, file-roller, system-config-printer |
| `itstool` | 4 | evince, file-roller, gparted, gnome-disk-utility |
| `desktop-file-utils` | 4 | file-roller, gnome-disk-utility, firewall-config, system-config-printer |
| `vala` | 3 | gimp, xfce-libs, libadwaita |
| `nasm` | 1 | ffmpeg |
| `swig` | 1 | obs-studio |
| `xmlto` | 1 | system-config-printer |
| `mm-common` | 1 | gtkmm3 |
| `gnome-doc-utils` | 1 | gparted |
| `hyprwayland-scanner` | 1 | hyprland |

### 2. Language runtimes & package managers

`python` exists; `pip` doesn't — pip ships *with* CPython, so this may just be a doc clarification (use `python` and invoke `python -m pip`). Same for `npm` (ships with `nodejs`).

| dep | refs | notes |
|---|---:|---|
| `pip` | 6 | likely just `python` (ships pip) — bazaar contributors shouldn't need to list separately |
| `git` | 4 | runtime dep for tools that shell out to git (lazygit, git-delta, pass, syncthing) |
| `nodejs` | 2 | needed by open-webui |
| `npm` | 1 | ships with nodejs |
| `cython` | 1 | blueman build dep |
| `pytorch` | — | (referenced by vllm, comfyui — but bazaar should probably define `pytorch` itself; left out of this count) |
| `protobuf` | 1 | onnxruntime runtime |
| `fuse` | 1 | lmstudio runtime (FUSE userspace lib) |

### 3. Qt 6

| dep | refs | notes |
|---|---:|---|
| `qt6-base` | 4 | obs-studio + keepassxc; both use it for runtime + build (it's not an `-dev` split) |

### 4. Desktop ecosystem

**GTK / GNOME** — `libhandy` (2), `libsecret` (2), `libnma`, `libpwquality`, `libportal`, `gtk-layer-shell`, `adwaita-icon-theme`, `appstream`, `iso-codes`, `gtkmm3` and its bindings: `glibmm`, `cairomm`, `pangomm`, `atkmm`, `sigc++`

**XFCE** — `exo`, `xfconf`, `libxfce4util`, `libxfce4ui`, `libice`, `libsm`, `startup-notification`

**Hyprland support libs** — `tomlplusplus` (2), `sdbus-cpp` (2), `xcb-util-wm` (2), `aquamarine`, `hyprcursor`, `libzip`

### 5. Audio / video / codecs

`libx264` (2), `libx265`, `libvpx`, `opus`, `lame` (2), `libwebp`, `giflib`, `pulseaudio`, `mbedtls`, `jansson`, `wxwidgets`, `portaudio`

### 6. C / C++ system libraries

`seatd` (4) — Wayland session management, blocks sway+wlroots+hyprland
`libevent` (2), `libsodium` (2), `iptables` (2), `pam` (2), `libxinerama` (2), `libxslt` (2)
`boost`, `nss`, `hunspell`, `oniguruma`, `libuv`, `tree-sitter`, `libluajit`, `msgpack-c`, `unibilium`, `containerd`, `fuse-overlayfs`, `libxt`, `libcurl`, `libdvdread`, `minizip`, `graphite2`, `hwdata`, `spdlog`, `fmt`

### 7. App-specific libs

`babl`, `gegl` (gimp); `gsl`, `gdl` (inkscape); `zip`, `unzip` (libreoffice build); `tree` (pass); `pycups`, `pycurl` (system-config-printer)

## How to regenerate this list

From the bazaar checkout:

```sh
./build/bazaar-validate    # confirms recipes parse + filenames match
# then run the python cross-check (see PR #N for the script)
```

Or run any TOML-parsing script that walks both repos and computes `bazaar_deps − (zugot_pkgs ∪ bazaar_pkgs)`.

Worth wiring this into bazaar's CI as a `--check-against ../zugot` mode of the validator so PRs surface gaps automatically.
