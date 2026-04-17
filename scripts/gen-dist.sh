#!/bin/sh
# gen-dist.sh — regenerate dist/zugot.cyr from the current recipe set.
#
# Produces a Cyrius module that exposes `zugot_names(out_vec)` — a function
# that populates the given vec with every package name currently in zugot.
# Consumers (bazaar's validator, other downstream tools) declare zugot as
# a cyrius dep and use this to check unresolved references at build time.
#
# Run on release / when package set changes. Commit the output.

set -eu
cd "$(dirname "$0")/.."

OUT=dist/zugot.cyr
mkdir -p dist

NAMES=$(
    # Parse every .cyml; tolerate CYML files the strict TOML parser rejects
    # (same regex fallback the bazaar cross-check uses).
    python3 - <<'PY'
import pathlib, re, tomllib
names = set()
for f in pathlib.Path('.').rglob('*.cyml'):
    # Skip our own manifest and any dist/ output
    if 'dist' in f.parts: continue
    try:
        with f.open('rb') as fh: d = tomllib.load(fh)
        n = d.get('package', {}).get('name')
    except Exception:
        m = re.search(r'^name\s*=\s*"([^"]+)"', f.read_text(), re.M)
        n = m.group(1) if m else None
    if n: names.add(n)
for n in sorted(names): print(n)
PY
)

COUNT=$(printf '%s\n' "$NAMES" | grep -c . || echo 0)
UTC=$(date -u +%Y-%m-%dT%H:%M:%SZ)
SHA=$(git rev-parse --short=12 HEAD 2>/dev/null || echo "unknown")

{
    printf '# dist/zugot.cyr — auto-generated index of zugot package names.\n'
    printf '# Do not edit by hand. Regenerate with scripts/gen-dist.sh\n'
    printf '#\n'
    printf '# Source: %s packages at zugot %s (%s)\n' "$COUNT" "$SHA" "$UTC"
    printf '#\n'
    printf '# Consumers (e.g. bazaar) declare this repo as a cyrius dep and call\n'
    printf '# zugot_names(vec) to populate a vec with every package name in zugot.\n'
    printf '# Membership checks drive dependency-resolution validation without\n'
    printf '# any runtime clone of zugot.\n\n'
    printf 'fn zugot_names(out) {\n'
    printf '%s\n' "$NAMES" | while IFS= read -r name; do
        [ -n "$name" ] || continue
        printf '    vec_push(out, str_from("%s"));\n' "$name"
    done
    printf '    return %s;\n' "$COUNT"
    printf '}\n'
} > "$OUT"

printf 'wrote %s (%s names)\n' "$OUT" "$COUNT"
