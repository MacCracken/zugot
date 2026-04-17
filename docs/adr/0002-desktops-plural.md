# ADR 0002 — Use plural `desktops` for group tag and directory

- **Status:** accepted
- **Date:** 2026-04-17
- **Deciders:** Robert MacCracken

## Context

The original recipe layout used `desktop/` as the directory for UI/graphics
packages, and `"desktop"` as the `groups` tag inside those recipes. This
assumed one desktop per AGNOS install (originally Wayland + GTK/foot/helix).

AGNOS's longer-term plan ships multiple desktop environments — a Hyprland-
based default, an XFCE profile, potentially others — each with overlapping
but distinct package graphs.

A singular tag conflates "this is for THE desktop" with "this is for A
desktop environment." Consumers that want to filter "show me everything for
XFCE" vs. "show me everything for Hyprland" both have to match `"desktop"`;
there's no distinguishing dimension.

## Decision

1. Rename the `groups` tag `"desktop"` → `"desktops"` (plural) in 130 recipes
2. Rename the filesystem directory `desktop/` → `desktops/` (176 recipes
   moved via `git mv`, history preserved)
3. Update `build-order.txt`, README, CLAUDE.md, roadmap references
4. Preserve non-group occurrences of `"desktop"`:
   - `seccomp_mode = "desktop"` (a named seccomp profile, not a group)
   - `tags = [..., "desktop", ...]` (human-facing search tag, not a group)
   - `boot_mode = ["desktop"]` (runtime boot-mode string, not a group)

## Consequences

**Positive:**
- Group tag reads as a namespace that holds multiple desktop environments,
  not as a singleton. Future DE-specific subgroups (`"desktops-hyprland"`,
  `"desktops-xfce"`) fit naturally.
- Directory name matches the plural convention used by `base/`,
  `marketplace/`, etc. (categories are always plural nouns)

**Negative:**
- One-time churn for 306 files (tag + file rename combined)
- Downstream consumers that hardcoded `"desktop"` must update
  (CHANGELOG calls this out explicitly)

## Alternatives considered

- **Keep singular `"desktop"`** — rejected: compounds the naming problem as
  DEs diverge; future subgroups would either shadow the singular or require
  an incompatible rename later
- **Two-level groups (`"desktop/wayland"`)** — rejected: the schema already
  uses flat string arrays; introducing path syntax would affect every
  consumer's query logic

## Related

- CHANGELOG.md [1.0.0] — "Group name: `desktop` → `desktops`" and
  "Directory rename: `desktop/` → `desktops/`"
- CLAUDE.md §Naming Conventions rule 6
