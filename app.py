"""
app.py
------
Streamlit demo for Priority-Aware Quantum Traffic Optimization
with Emergency Vehicle Green Corridors.

Author: Your Team
"""

import streamlit as st
import matplotlib.pyplot as plt
import networkx as nx

# Project modules
from network_builder import build_network_pipeline
from traffic_simulator import build_traffic_scenario
from qubo_builder import build_priority_aware_qubo
from solver import solve_traffic_qubo


# --------------------------------------------------
# STREAMLIT PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="Priority-Aware Quantum Traffic Optimization",
    layout="wide"
)

st.title("🚦 Priority-Aware Quantum Traffic Optimization")
st.subheader("Emergency Vehicle Green Corridor Demonstration")


# --------------------------------------------------
# SIDEBAR CONTROLS
# --------------------------------------------------

st.sidebar.header("Simulation Controls")

place = st.sidebar.text_input(
    "Enter City / Area",
    value="Kochi, India"
)

num_vehicles = st.sidebar.slider(
    "Number of Vehicles",
    min_value=3,
    max_value=15,
    value=6
)

emergency_ratio = st.sidebar.slider(
    "Emergency Vehicle Ratio",
    min_value=0.1,
    max_value=0.5,
    value=0.3
)

solve_button = st.sidebar.button("Run Optimization")


# --------------------------------------------------
# HELPER: DRAW GRAPH
# --------------------------------------------------

def draw_graph(G, routes=None, emergency_routes=None):
    pos = nx.spring_layout(G, seed=42)

    plt.figure(figsize=(10, 8))

    # Draw base graph
    nx.draw(
        G, pos,
        node_size=5,
        edge_color="lightgray",
        with_labels=False
    )

    # Draw regular routes
    if routes:
        for route in routes.values():
            edges = [(route[i], route[i + 1]) for i in range(len(route) - 1)]
            nx.draw_networkx_edges(
                G, pos,
                edgelist=edges,
                edge_color="blue",
                width=2,
                alpha=0.6
            )

    # Draw emergency routes
    if emergency_routes:
        for route in emergency_routes:
            edges = [(route[i], route[i + 1]) for i in range(len(route) - 1)]
            nx.draw_networkx_edges(
                G, pos,
                edgelist=edges,
                edge_color="green",
                width=3
            )

    st.pyplot(plt.gcf())
    plt.clf()


# --------------------------------------------------
# MAIN EXECUTION
# --------------------------------------------------

if solve_button:

    st.info("Building road network and simulating traffic...")

    # 1. Build network
    network_data = build_network_pipeline(
        place_name=place,
        num_vehicles=num_vehicles
    )

    # 2. Simulate traffic
    scenario = build_traffic_scenario(
        network_data,
        emergency_ratio=emergency_ratio
    )

    G = scenario["graph"]
    vehicles = scenario["vehicles"]

    # Identify emergency vehicles
    emergency_vehicles = [v for v in vehicles if v["type"] == "emergency"]

    st.success(f"Total Vehicles: {len(vehicles)}")
    st.success(f"Emergency Vehicles: {len(emergency_vehicles)}")

    # 3. Build QUBO
    st.info("Formulating Priority-Aware QUBO...")
    bqm, variable_map = build_priority_aware_qubo(vehicles)

    # 4. Solve QUBO
    st.info("Solving optimization problem...")
    selected_routes = solve_traffic_qubo(
        bqm,
        variable_map,
        vehicles,
        method="sa"  # simulated annealing
    )

    # Separate emergency routes
    emergency_routes = []
    regular_routes = {}

    for v in vehicles:
        vid = v["vehicle_id"]
        if vid in selected_routes:
            if v["type"] == "emergency":
                emergency_routes.append(selected_routes[vid])
            else:
                regular_routes[vid] = selected_routes[vid]

    # 5. Visualization
    st.subheader("🗺️ Optimized Traffic Flow")
    st.caption("Green = Emergency Corridor | Blue = Regular Traffic")

    draw_graph(
        G,
        routes=regular_routes,
        emergency_routes=emergency_routes
    )

    # 6. Results Summary
    st.subheader("📊 Optimization Summary")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Emergency Vehicles")
        for v in emergency_vehicles:
            st.write(f"Vehicle {v['vehicle_id']} → Priority Route Assigned")

    with col2:
        st.markdown("### Regular Vehicles")
        for vid in regular_routes.keys():
            st.write(f"Vehicle {vid} → Optimized Route Assigned")

else:
    st.info("Set parameters and click **Run Optimization** to start.")
