# PRD: Reservation Drop Tracker + Assisted Booker

## Goals
- Track likely reservation drop windows for high-demand restaurants in NYC/PHL.
- Combine seeds, Reddit evidence, and manual overrides for confidence-ranked rules.
- Provide assisted (not fully autonomous) booking workflows with user confirmation gates.

## Non-goals
- CAPTCHA bypassing, stealth botting, or anti-abuse evasion.
- Scraping paywalled NYT pages.
- Unattended final booking submit without explicit user approval.

## Core workflows
1. Ingest seeds (built-in + user CSV)
2. Discover mentions (Reddit + future sources)
3. Infer drop rules and confidence
4. Plan booking requests around inferred rules
5. Execute deep-link or assisted Playwright flows with pause/resume on challenges

## Guardrails
- No private/undocumented endpoint reverse engineering.
- No PII persistence in logs (redaction applied).
- Rate limiting + jitter + dry-run support everywhere.
- Explicit confirmation before final submit.
