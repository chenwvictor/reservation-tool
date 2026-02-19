# Data Model

## Restaurant
- `id` (int, PK)
- `name` (str, indexed)
- `city` (enum: NYC|PHL)
- `provider` (enum: resy|opentable|unknown)
- `provider_url` (nullable str)
- `popularity_score` (float)
- `tags` (JSON/text)
- `created_at`, `updated_at` (datetime)

## Evidence
- `id` (int, PK)
- `restaurant_id` (FK -> Restaurant)
- `source` (str, default `reddit`)
- `url` (str)
- `excerpt` (str)
- `posted_at` (datetime)

## DropRule
- `restaurant_id` (PK/FK -> Restaurant)
- `lead_time_days` (nullable int)
- `open_time_local` (nullable `HH:MM` str)
- `timezone` (str, default `America/New_York`)
- `rule_text` (nullable str)
- `confidence` (float)
- `updated_at` (datetime)

## BookingRequest
- `id` (int, PK)
- `restaurant_id` (FK -> Restaurant)
- `party_size` (int)
- `date_target` (date)
- `time_window_start` (`HH:MM`)
- `time_window_end` (`HH:MM`)
- `mode` (`deeplink`|`assist`)
- `dry_run` (bool)
- `created_at` (datetime)

## Job
- `id` (int, PK)
- `booking_request_id` (FK -> BookingRequest)
- `run_at` (datetime)
- `status` (`queued`|`running`|`success`|`failed`|`needs_user`)
- `last_error` (nullable str)
- `log_path` (nullable str)
- `created_at`, `updated_at` (datetime)

## Indexing notes
- Index restaurant `name`, `city`.
- Index evidence `restaurant_id`, `posted_at`.
- Index jobs `status`, `run_at`.
