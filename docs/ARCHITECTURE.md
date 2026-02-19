# Architecture

## Overview
A local-first Python CLI app with modular services:

- **CLI layer** (`cli.py`): Typer commands and user interaction.
- **Config layer** (`config.py`): Environment and defaults via Pydantic Settings.
- **Persistence layer** (`db.py`, `models.py`): SQLite + SQLModel entities.
- **Discovery layer** (`discovery.py`): Reddit fetch + extraction of candidate entities/evidence.
- **Inference layer** (`inference.py`): Heuristics to infer drop rules and confidence.
- **Planning layer** (`planner.py`): next-drop calculation and job creation.
- **Booking layer** (`providers.py`, `booking.py`): deep-link and optional assisted Playwright runner.
- **Scheduler** (`scheduler.py`): simple in-process loop to execute due jobs.

## Data flow
1. `refresh` fetches Reddit content and writes `Restaurant` + `Evidence`.
2. `infer` reads restaurant evidence, creates/updates `DropRule`.
3. `browse` reads joined data and presents terminal table.
4. `plan` creates `BookingRequest`, computes `run_at`, creates `Job`.
5. `book` executes job immediately or schedules.
6. `jobs` displays queue/history.

## External integrations
- **Reddit API (PRAW optional)**: used when credentials are available.
- **Fallback fetcher**: minimal static/mock retrieval when API unavailable.
- **Playwright (optional)**: assisted UI steps for providers.

## Compliance/safety design
- Never bypass anti-bot systems.
- If CAPTCHA/login/2FA is detected or suspected, stop and ask user to continue manually.
- Terminal confirmation required before final submit action.
- Redacted logs by default (email and phone masking regex).

## Deployment model
- Personal local execution only.
- SQLite file under configurable data directory.
- Single process scheduler started through CLI command.
