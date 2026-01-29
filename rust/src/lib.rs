use petgraph::algo::astar;
use petgraph::graph::{Graph, NodeIndex};
use petgraph::Directed;
use pyo3::prelude::*;
use std::collections::HashMap;

/// A simple Python class to hold one step of the journey.
/// Example: "At HUTATMA CHOWK, take 10 LTD"
#[pyclass]
#[derive(Clone)]
struct RouteStep {
    #[pyo3(get)]
    stop: String,
    #[pyo3(get)]
    bus: String, // The bus to take to get to the NEXT stop (or "Arrived" for the last one)
}

#[pyclass]
struct BusGraph {
    // Nodes = Stop Names, Edges = Bus Numbers
    graph: Graph<String, String, Directed>,
    stop_indices: HashMap<String, NodeIndex>,
}

#[pymethods]
impl BusGraph {
    #[new]
    fn new() -> Self {
        BusGraph {
            graph: Graph::new(),
            stop_indices: HashMap::new(),
        }
    }

    fn add_route(&mut self, bus_number: String, stops: Vec<String>) {
        if stops.is_empty() {
            return;
        }

        let mut route_indices: Vec<NodeIndex> = Vec::new();
        // 1. Get or Create Nodes
        for stop in &stops {
            let index = *self
                .stop_indices
                .entry(stop.clone())
                .or_insert_with(|| self.graph.add_node(stop.clone()));
            route_indices.push(index);
        }

        // 2. Add Edges (Bus Connections)
        for i in 0..route_indices.len() - 1 {
            let from = route_indices[i];
            let to = route_indices[i + 1];
            // We allow multiple edges between nodes because different
            // buses might serve the same segment.
            self.graph.add_edge(from, to, bus_number.clone());
        }
    }

    /// Returns a list of RouteStep objects (Stop Name + Bus to take)
    fn find_path(&self, start_stop: String, end_stop: String) -> Option<Vec<RouteStep>> {
        let start_idx = self.stop_indices.get(&start_stop)?;
        let end_idx = self.stop_indices.get(&end_stop)?;

        // 1. Calculate the shortest path of Nodes (Stops)
        let path_result = astar(
            &self.graph,
            *start_idx,
            |finish| finish == *end_idx,
            |_| 1, // Cost is 1 hop
            |_| 0, // Heuristic
        );

        let (_cost, node_indices) = path_result?;

        // 2. Reconstruct the path with Bus Numbers
        // We need to look at each pair of stops and decide which bus to "take".
        let mut full_route: Vec<RouteStep> = Vec::new();
        let mut current_bus_preference: Option<String> = None;

        for i in 0..node_indices.len() {
            let current_node = node_indices[i];
            let stop_name = self.graph[current_node].clone();

            // If this is the last stop, we have arrived.
            if i == node_indices.len() - 1 {
                full_route.push(RouteStep {
                    stop: stop_name,
                    bus: "Arrived".to_string(),
                });
                break;
            }

            let next_node = node_indices[i + 1];

            // 3. Find the best bus to connect Current -> Next
            // There might be multiple buses connecting these two nodes.
            // We use "Sticky" logic: if we are already on a bus that goes to the next stop, stay on it.
            let mut best_bus = "Walk".to_string(); // Fallback
            let mut found_sticky = false;
            let mut any_bus: Option<String> = None;

            // Iterate over all edges connecting these two nodes
            let edges = self.graph.edges_connecting(current_node, next_node);

            for edge in edges {
                let bus_on_edge = edge.weight().clone();

                // If this bus matches the one we were just on, keep it (Minimize transfers)
                if let Some(ref pref) = current_bus_preference {
                    if *pref == bus_on_edge {
                        best_bus = bus_on_edge.clone();
                        found_sticky = true;
                        break;
                    }
                }
                // Keep track of at least one valid bus in case we don't find our preferred one
                if any_bus.is_none() {
                    any_bus = Some(bus_on_edge);
                }
            }

            if !found_sticky {
                // We were forced to transfer (or this is the start), pick the first available bus
                if let Some(b) = any_bus {
                    best_bus = b;
                }
            }

            // Update preference for the next hop
            current_bus_preference = Some(best_bus.clone());

            full_route.push(RouteStep {
                stop: stop_name,
                bus: best_bus,
            });
        }

        Some(full_route)
    }
}

#[pymodule]
fn mumbai_bus_rs(_py: Python, m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<BusGraph>()?;
    m.add_class::<RouteStep>()?;
    Ok(())
}
