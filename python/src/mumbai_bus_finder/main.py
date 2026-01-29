import os
import sys

# Ensure we can find our own modules if running from root
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from mumbai_bus_finder.graph.builder import GraphBuilder


def main():
    # Adjust path relative to where you run this script
    # Assuming running from project root
    raw_data_path = "data/raw/best_bus_routes.json"

    builder = GraphBuilder(raw_data_path)
    builder.build()

    # Test Case
    start_node = "Hutatma Chowk"
    end_node = "Mantralaya"

    print(f"\n--- Finding path from {start_node} to {end_node} ---")
    path_steps = builder.find_shortest_path(start_node, end_node)

    if path_steps:
        print(f"Found path with {len(path_steps) - 1} stops:")
        print("-" * 60)
        print(f"{'STOP NAME':<40} | {'BUS TO TAKE'}")
        print("-" * 60)

        for step in path_steps:
            # Access the properties we defined in Rust struct
            print(f"{step.stop:<40} | {step.bus}")

        print("-" * 60)
    else:
        print("No path found.")


if __name__ == "__main__":
    main()
