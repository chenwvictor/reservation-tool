#!/usr/bin/env bash
set -euo pipefail
rm -f resy_sniper.db
python -m resy_sniper.cli ingest-seeds
