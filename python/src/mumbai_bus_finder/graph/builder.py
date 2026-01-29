import json
import re
from pathlib import Path
from typing import List, Optional

import mumbai_bus_rs


class GraphBuilder:
    def __init__(self, data_path: str):
        self.data_path = Path(data_path)
        self.graph = mumbai_bus_rs.BusGraph()

    def _clean_stop_name(self, name: str) -> str:
        """
        Normalizes stop names:
        - Removes trailing dots
        - Converts to uppercase
        - Strips whitespace
        Example: "Hutatma Chowk." -> "HUTATMA CHOWK"
        """
        if not name:
            return ""
        # Remove dots at the end, strip spaces, upper case
        clean = name.strip().rstrip(".").strip().upper()
        # Optional: specific fixes could go here
        return clean

    def build(self):
        """Loads data and populates the Rust graph."""
        if not self.data_path.exists():
            raise FileNotFoundError(f"Data file not found: {self.data_path}")

        with open(self.data_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        print(f"Loading {len(data)} routes into graph...")

        for entry in data:
            bus_no = entry.get("bus", "Unknown")
            raw_stops = entry.get("stops", [])

            # Clean all stops in the list
            clean_stops = [self._clean_stop_name(s) for s in raw_stops]

            # Filter out empty strings just in case
            clean_stops = [s for s in clean_stops if s]

            # Push to Rust
            self.graph.add_route(bus_no, clean_stops)

        print("Graph built successfully.")

    def find_shortest_path(self, start: str, end: str) -> Optional[List[str]]:
        """Wrapper for the Rust pathfinder."""
        c_start = self._clean_stop_name(start)
        c_end = self._clean_stop_name(end)
        return self.graph.find_path(c_start, c_end)
