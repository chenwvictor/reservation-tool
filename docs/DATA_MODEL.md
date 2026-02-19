# Data Model

## Restaurant
- `id`, `name`, `normalized_name`, `city`, `provider`, `provider_url`, `source`, `popularity_score`

## DropRule
- `id`, `restaurant_id`, `days_ahead`, `drop_time`, `confidence`, `manual_override`, `notes`

## Evidence
- `id`, `restaurant_id`, `source_type`, `source_url`, `snippet`, `observed_at`, `weight`

## BookingRequest
- `id`, `restaurant_id`, `party_size`, `target_date`, `time_window`, `mode`, `status`, `dry_run`, `profile`

## Job
- `id`, `booking_request_id`, `run_at`, `status`, `result`
