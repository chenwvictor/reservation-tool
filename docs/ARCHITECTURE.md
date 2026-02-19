# Architecture

## Modules
- `config.py`: env/config loading, weight/rate settings.
- `models.py`: SQLModel entities (`Restaurant`, `DropRule`, `Evidence`, `BookingRequest`, `Job`).
- `db.py`: engine/session/init helpers.
- `seeds.py` + `ingest_seeds.py`: curated seeds and CSV ingestion.
- `discovery.py`: seed+reddit discovery and merge dedupe.
- `inference.py`: regex extraction + confidence scoring.
- `planner.py`: computes next drop datetime.
- `providers.py`: official API adapters + deep-link fallback builder.
- `booking.py`: booking flow, assisted Playwright mode, confirmation gate.
- `cli.py`: orchestration commands.

## Data flow
1. `ingest-seeds` / `ingest-csv` populate restaurants + provenance.
2. `refresh` collects external mentions and merges into restaurants/evidence.
3. `infer` converts evidence into drop rules with confidence + snippets.
4. `plan` creates booking requests scheduled at computed drop datetime.
5. `book` executes dry-run or assisted booking with explicit confirmation.
