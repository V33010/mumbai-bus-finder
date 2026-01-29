Mumbai Bus Finder 🚌
A high-performance hybrid application to discover optimal BEST bus routes in Mumbai. It combines Python for data orchestration/scraping and Rust for lightning-fast graph algorithms and pathfinding.

✨ Features
Hybrid Architecture: Python handles the web scraping and IO, while a compiled Rust extension handles the heavy graph computations.

Graph-Based Routing: Uses petgraph (Rust) to model the entire Mumbai bus network as a directed graph.

"Sticky Bus" Logic: The routing algorithm intelligently prefers staying on the current bus over unnecessary transfers when multiple buses serve the same route segment.

Data Scraping: Automated scraper to fetch the latest route details directly from BEST data sources.

📂 Project Structure
```
.
├── python/               # Python Source Code
│   ├── src/              # Scrapers, Graph Builder, and CLI tools
│   └── pyproject.toml    # Python dependencies (uv)
├── rust/                 # Rust Source Code
│   ├── src/              # Graph algorithms & Python bindings (PyO3)
│   └── Cargo.toml        # Rust dependencies
├── data/                 # Data Storage
│   └── raw/              # Scraped JSON data (best_bus_routes.json)
└── scripts/              # Helper shell scripts
```

🛠️ Prerequisites
Python 3.12+

Rust (latest stable toolchain)

uv (Python package manager)

🚀 Setup & Installation
Sync Python Dependencies

```bash
uv sync
```

Install Maturin (Bridge tool for Rust/Python)

```bash
uv pip install maturin
```

Compile the Rust Graph Engine This builds the Rust code and installs it as a Python module (mumbai_bus_rs) in your current environment.

```bash
maturin develop --manifest-path rust/Cargo.toml
```

🏃 Usage
1. Scrape Route Data
First, populate the dataset by running the scraper. This saves data to data/raw/best_bus_routes.json.

```bash
python python/src/mumbai_bus_finder/scraper/scrape_best_routes.py
```

2. Find a Route
Run the main application to load the graph and find the optimal path between two stops (e.g., Hutatma Chowk to Mantralaya).

```bash
python python/src/mumbai_bus_finder/main.py
```

Sample Output:

```
Loading 480 routes into graph...
Graph built successfully.

--- Finding path from Hutatma Chowk to Mantralaya ---
Found path with 3 stops:
------------------------------------------------------------
STOP NAME                                | BUS TO TAKE
------------------------------------------------------------
HUTATMA CHOWK                            | 137-NAVY NAGAR VIA NCPA AND NAVY NAGAR
DR.S.P.MUKHERJI CHOWK \ MUSEUM           | 137-NAVY NAGAR VIA NCPA AND NAVY NAGAR
Y.B.CHAVAN PRATISHTAN                    | AS-4 BEST BUS ROUTEBACKBAY DEPOT AND GOREGAON / OSHIWARA DEPOT
MANTRALAYA                               | Arrived
------------------------------------------------------------
```

## License
MIT
