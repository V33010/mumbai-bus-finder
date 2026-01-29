#!/usr/bin/env bash
set -e

# Move to project root
cd "$(dirname "$0")/.."

# Run scraper with correct PYTHONPATH
PYTHONPATH=python/src uv run python -m mumbai_bus_finder.scraper.scrape_best_routes

