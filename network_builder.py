"""
network_builder.py
------------------
Builds and prepares a real-world road network for
Priority-Aware Quantum Traffic Optimization.

Author: Your Team
"""

import osmnx as ox
import networkx as nx
import random


# --------------------------------------------------
# 1. BUILD ROAD NETWORK FROM OPENSTREETMAP
# --------------------------------------------------

def build_road_network(place_name: str):
    """
    Download and create a road network graph from OpenStreetMap.

    Args:
        place_name (str): Name of the city or area

    Returns:
        G (networkx.Graph): Road network graph
    """
    G = ox.graph_from_place(place_name, network_type="drive")



# Convert DiGraph → Graph (simple graph)
    G = nx.Graph(G)

    return G


# --------------------------------------------------
# 2. ADD EDGE ATTRIBUTES (SPEED, LENGTH)
# --------------------------------------------------

def add_edge_attributes(G):
    """
    Ensure each road segment has speed and length.

    Args:
        G (networkx.Graph)

    Returns:
        G (networkx.Graph)
    """
    for u, v, data in G.edges(data=True):

        # Length (meters)
        length = data.get("length", random.randint(50, 300))
        data["length"] = length

        # Speed (km/h)
        speed = data.get("speed_kph", random.choice([30, 40, 50, 60]))
        if isinstance(speed, list):
            speed = speed[0]
        data["speed"] = speed

    return G


# --------------------------------------------------
# 3. SIMULATE CONGESTION ON ROADS
# --------------------------------------------------

def add_congestion(G, min_level=1, max_level=10):
    """
    Add simulated congestion level to each road.

    Args:
        G (networkx.Graph)
        min_level (int)
        max_level (int)

    Returns:
        G (networkx.Graph)
    """
    for u, v, data in G.edges(data=True):
        data["congestion"] = random.randint(min_level, max_level)

    return G


# --------------------------------------------------
# 4. COMPUTE TRAVEL TIME
# --------------------------------------------------

def compute_travel_time(G):
    """
    Compute travel time (minutes) for each road.

    Formula:
        time = (length / speed) * congestion_factor

    Args:
        G (networkx.Graph)

    Returns:
        G (networkx.Graph)
    """
    for u, v, data in G.edges(data=True):
        length_km = data["length"] / 1000
        speed_kmph = max(data["speed"], 1)
        congestion = data["congestion"]

        base_time = (length_km / speed_kmph) * 60
        data["travel_time"] = base_time * congestion

    return G


# --------------------------------------------------
# 5. SELECT RANDOM ORIGIN–DESTINATION PAIRS
# --------------------------------------------------

def generate_od_pairs(G, num_pairs=5):
    """
    Generate random origin-destination node pairs.

    Args:
        G (networkx.Graph)
        num_pairs (int)

    Returns:
        List of (origin, destination)
    """
    nodes = list(G.nodes)
    od_pairs = []

    for _ in range(num_pairs):
        origin, destination = random.sample(nodes, 2)
        od_pairs.append((origin, destination))

    return od_pairs


# --------------------------------------------------
# 6. FIND CANDIDATE ROUTES
# --------------------------------------------------

def find_candidate_routes(G, origin, destination, k=3):
    """
    Find up to k shortest routes between origin and destination.

    Args:
        G (networkx.Graph)
        origin (int)
        destination (int)
        k (int)

    Returns:
        List of routes (each route is a list of nodes)
    """
    routes = []
    try:
        paths = nx.shortest_simple_paths(
            G,
            source=origin,
            target=destination,
            weight="travel_time"
        )

        for path in paths:
            routes.append(path)
            if len(routes) == k:
                break

    except nx.NetworkXNoPath:
        pass

    return routes


# --------------------------------------------------
# 7. CONVERT ROUTES TO EDGE LISTS
# --------------------------------------------------

def routes_to_edges(routes):
    """
    Convert node paths into edge paths.

    Args:
        routes (list)

    Returns:
        List of edge lists
    """
    all_edges = []

    for path in routes:
        edges = [(path[i], path[i + 1]) for i in range(len(path) - 1)]
        all_edges.append(edges)

    return all_edges


# --------------------------------------------------
# 8. COMPLETE PIPELINE (FOR STREAMLIT)
# --------------------------------------------------

def build_network_pipeline(place_name, num_vehicles=5):
    """
    Full pipeline to prepare network for optimization.

    Returns:
        dict with graph, OD pairs, and routes
    """
    G = build_road_network(place_name)
    G = add_edge_attributes(G)
    G = add_congestion(G)
    G = compute_travel_time(G)

    od_pairs = generate_od_pairs(G, num_vehicles)

    routes = {}
    for (o, d) in od_pairs:
        routes[(o, d)] = find_candidate_routes(G, o, d)

    return {
        "graph": G,
        "od_pairs": od_pairs,
        "routes": routes
    }
