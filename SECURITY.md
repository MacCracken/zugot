# Security Policy

## Reporting vulnerabilities

Zugot is a **recipe database**, not the software it builds. If you've found a
vulnerability in an upstream package (e.g. OpenSSL, curl, Firefox), report it
to that project directly — zugot just pins versions.

**Report to zugot directly only if:**

- A recipe ships a **known-vulnerable version** that has an upstream fix
  available (a new CVE landed between our audit cycles and zugot hasn't
  bumped yet)
- A recipe's **build or install logic** introduces a vulnerability (wrong
  `--sysconfdir`, weak sandbox flags, missing hardening stack)
- A **SHA256 mismatch** — the pinned hash doesn't match what upstream serves
  (indicates either a recipe bug or a supply-chain compromise; treat as
  critical)

## How to report

Email the maintainer privately or open a **private GitHub security
advisory** on the zugot repo. Do not open public issues for unpublished CVEs
affecting pinned versions.

## What we'll do

1. Acknowledge within 48 hours
2. For upstream-CVE-with-fix issues: prioritize the bump in the next audit
   cycle (or immediately if CVSS ≥ 9.0)
3. For recipe-logic issues: fix in a dedicated PR, credit the reporter in
   the CHANGELOG
4. For SHA mismatches: investigate supply-chain compromise immediately; may
   quarantine the recipe

## CVE audit cadence

Zugot runs a monthly CVE audit, pegged to the Firefox/Chromium monthly
cycle. Reports live in [`docs/audit/YYYY-MM-DD.md`](./docs/audit/).

Current open-but-upstream-unfixed items are tracked in
[`docs/development/roadmap.md`](./docs/development/roadmap.md) §P2.

## Supported versions

Zugot follows semantic versioning. Only the current major version receives
security bumps; older releases are archived.

| Version | Status | Security bumps |
|---|---|---|
| 1.0.0 | current | ✅ monthly cycle |
| 0.1.0 | archived | ❌ (initial migration from agnosticos/recipes/) |
