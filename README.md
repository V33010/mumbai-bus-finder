# Mumbai Bus Finder

A Python project to discover optimal BEST bus routes in Mumbai using scraped
route data and graph-based routing algorithms.

## Features (WIP)
- Scrape BEST bus routes and stops
- Build a route graph from static data
- Find optimal bus paths between two locations

## Project Structure
- `src/` – application source code
- `data/raw/` – scraped, unprocessed data
- `data/processed/` – cleaned / normalized data
- `scripts/` – helper shell scripts

## Setup

```bash
uv sync
```

## Usage
Run the scraper:
```bash 
python src/mumbai_bus_finder/scraper/scrape_best_routes.py
```

Output will be saved to:
```bash 
data/raw/best_bus_routes.json
```

## License

MIT
