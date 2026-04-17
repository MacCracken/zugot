# ADR 0005 — Dated CVE audit cadence + report format

- **Status:** accepted
- **Date:** 2026-04-17
- **Deciders:** Robert MacCracken

## Context

Zugot ships packages that are primary attack surface: openssl, openssh,
sudo, gnupg, browsers, the kernel, every image codec shipped to the desktop.
Package versions drift against the CVE landscape daily. Without a disciplined
review cadence, zugot accumulates known-vulnerable pins.

The first external CVE audit (2026-04-17) surfaced:
- 1 critical CVE requiring an immediate branch migration (gnupg 2.4 → 2.5)
- 7 CVEs where zugot is already at latest but upstream hasn't shipped a fix
- 1 uncertain case pending upstream release notes

## Decision

1. **One report file per audit pass**, named `docs/audit/YYYY-MM-DD.md`.
   Files are immutable (or append-only for corrections) so the audit trail
   survives as a historical record.

2. **Research method**: WebSearch + WebFetch against NVD, vendor security
   pages (openssl.org, openssh.org, gnupg.org/vulnerabilities,
   sudo.ws/security, mozilla.org/security, chromereleases.googleblog.com,
   postgresql.org/support/security, redis.io/blog, etc.). For each pinned
   version, cross-reference published CVEs with the fix version.

3. **Output classification**:
   - ⚠️ **Fix applied this pass** — a bump or patch landed in the same PR as
     the audit; link the CHANGELOG entry
   - 🟡 **Monitor (no upstream fix yet)** — zugot is at latest upstream but a
     CVE is open; add to `docs/development/roadmap.md` §P2 with the watch-
     list of upstream fix versions
   - 🟠 **Uncertain — verify next cycle** — CVE published but fix-status
     unclear (e.g. release notes not yet public)
   - ✅ **Clean at pinned version** — no action

4. **Cadence**: monthly, pegged to the Firefox/Chromium monthly release
   cycle (Chromium stable cuts roughly the first week of each month, and
   those cycles tend to bundle a high CVE count).

5. **Scope**: minimum of the ~49 packages in the first audit. Expand when a
   new security-sensitive package enters the tree.

## Consequences

**Positive:**
- The audit is an artifact, not a moment. Future reviewers can reconstruct
  what was known and patched at any past point.
- Separating "fixed", "monitor", and "clean" means the roadmap doesn't
  bloat with things that are actually resolved.
- Monthly cadence matches browser security-release rhythm, which is
  frequently the largest CVE bundle.

**Negative:**
- Each audit burns 30–60 minutes of web research + potentially hours of
  tarball re-downloads for bumps. Mitigation: most monthly audits will find
  ≤3 bumps; large-delta audits are the exception.

## Alternatives considered

- **Automated NVD feed subscription** — rejected for 1.0.0: setting up
  an NVD feed ingest that maps CPE strings to zugot recipe names is a
  separate tooling project. Noted as a future P3 item.
- **Continuous CVE-watching via Dependabot-equivalent** — rejected: zugot's
  recipes aren't a language-package-manager format Dependabot understands.
  Could be built as custom tooling (P3), but manual monthly audits are the
  pragmatic 1.0 answer.
- **Ad-hoc audits when a known CVE makes news** — rejected: that captures
  the high-profile CVEs but misses the steady stream of moderate-severity
  issues that accumulate without news attention.

## Related

- `docs/audit/2026-04-17.md` — first audit, establishes the format
- `docs/development/roadmap.md` §P2 — monitor list
- CLAUDE.md §CHANGELOG Format
