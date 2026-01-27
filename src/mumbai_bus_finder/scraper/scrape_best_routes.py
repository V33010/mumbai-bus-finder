"""
Scraper for BEST Mumbai bus routes from thaneatoz.com

Outputs:
    data/raw/best_bus_routes.json
"""

import json
import time
from pathlib import Path

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://www.thaneatoz.com/BEST?page={}"
TOTAL_PAGES = 48
REQUEST_DELAY = 0.75  # seconds


def get_output_path() -> Path:
    """
    Returns the absolute path to data/raw/best_bus_routes.json
    regardless of where the script is run from.
    """
    # scrape_best_routes.py
    # └── scraper
    #     └── mumbai_bus_finder
    #         └── src
    #             └── mumbai-bus-finder  <-- PROJECT ROOT
    project_root = Path(__file__).resolve().parents[3]
    return project_root / "data" / "raw" / "best_bus_routes.json"


def scrape_best_bus_routes():
    output_path = get_output_path()
    output_path.parent.mkdir(parents=True, exist_ok=True)

    all_routes = []

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        )
    }

    for page in range(TOTAL_PAGES):
        print(f"[+] Scraping page {page}")

        try:
            response = requests.get(
                BASE_URL.format(page),
                headers=headers,
                timeout=10,
            )

            if response.status_code != 200:
                print(f"    [!] Failed page {page} (status {response.status_code})")
                continue

            soup = BeautifulSoup(response.text, "html.parser")

            table = soup.find("table", class_="views-table")
            if not table:
                print(f"    [!] No table found on page {page}")
                continue

            tbody = table.find("tbody")
            if not tbody:
                print(f"    [!] No tbody found on page {page}")
                continue

            for row in tbody.find_all("tr"):
                title_cell = row.find("td", class_="views-field-title")
                body_cell = row.find("td", class_="views-field-body")

                if not title_cell or not body_cell:
                    continue

                bus_field = title_cell.get_text(strip=True)

                route_text = body_cell.get_text(separator=",", strip=True)
                stops = [stop.strip() for stop in route_text.split(",") if stop.strip()]

                all_routes.append(
                    {
                        "bus": bus_field,
                        "stops": stops,
                    }
                )

            time.sleep(REQUEST_DELAY)

        except Exception as exc:
            print(f"    [!] Error on page {page}: {exc}")

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(all_routes, f, indent=2, ensure_ascii=False)

    print("\n✅ Scraping complete")
    print(f"Routes scraped : {len(all_routes)}")
    print(f"Saved to       : {output_path}")


if __name__ == "__main__":
    scrape_best_bus_routes()
