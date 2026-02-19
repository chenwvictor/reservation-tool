# Resy Sniper

Reservation Drop Tracker + Assisted Booker (NYC + PHL) with explicit safety guardrails.

## Safety guardrails
- Never bypass CAPTCHA, 2FA, or anti-bot systems.
- Use official APIs when credentials are available; otherwise use deep links and user-assisted flows.
- Require explicit user confirmation before final booking submit.
- Redact PII from logs and persisted audit fields.

## Setup
```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
cp .env.example .env
# Fill provider/reddit keys as needed
playwright install
```

## Run commands
```bash
# module mode
python -m resy_sniper.cli --help
python -m resy_sniper --help

# installed console script mode
resy-sniper --help
```

## Typical flow
```bash
resy-sniper ingest-csv nyt_top100.csv
resy-sniper ingest-seeds
resy-sniper refresh
resy-sniper infer
resy-sniper browse --city NYC
resy-sniper plan --restaurant 12 --party 2 --date 2026-03-10 --time-window 19:00-20:30 --mode deeplink --dry-run
resy-sniper book --request-id 7 --assist --dry-run
resy-sniper jobs
```

## Tests
```bash
pytest
```

## Notes on providers
OpenTable and Resy official APIs are typically partner/onboarding-only. This tool includes adapter stubs with TODOs and deep-link fallback behavior when authorized API access is unavailable.

## CSV schema
`ingest-csv` expects columns:
- `name`
- `city`
- `source_url`
