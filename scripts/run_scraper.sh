#!/usr/bin/env bash

set -e  # exit on error

# Move to the python subproject root
cd "$(dirname "$0")/../python"

# Run the scraper using uv
uv run python -m mumbai_bus_finder.scraper.scrape_best_routes
