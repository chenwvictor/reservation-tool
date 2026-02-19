# resy-sniper

MVP personal Reservation Drop Tracker + Assisted Booker for NYC/PHL.

## Quickstart

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
cp .env.example .env
```

Commands:
- `resy_sniper refresh`
- `resy_sniper infer`
- `resy_sniper browse --city NYC`
- `resy_sniper plan --restaurant 1 --party 2 --date 2026-03-10 --time-window 19:00-20:30`
- `resy_sniper book --request-id 1 --assist`
