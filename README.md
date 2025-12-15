# Quantum-Traffic-Priority-Routing

A research-oriented prototype that demonstrates **priority-aware traffic routing** to reduce congestion and create **emergency corridors** using **quantum-inspired optimization techniques**.  
The system is implemented as an interactive **Streamlit dashboard** with **simulated traffic** and optional **SUMO integration** for realism.

---

##  Project Motivation

Urban traffic congestion delays emergency response vehicles such as ambulances and fire trucks.  
Most traffic optimization systems treat all vehicles equally, which is not suitable in emergency scenarios.

This project introduces a **Priority-Aware Traffic Optimization System** that:
- Simulates urban traffic on a real road network
- Assigns higher priority to emergency vehicles
- Optimizes routing using a **QUBO (Quadratic Unconstrained Binary Optimization)** model
- Visualizes congestion reduction and emergency corridors

This is a **guided demo**, not a deployed city system.

---

##  Objectives

- Simulate urban traffic using synthetic data (and optionally SUMO)
- Estimate congestion based on road usage
- Introduce priority-aware routing for emergency vehicles
- Optimize traffic using quantum-inspired solvers
- Visualize **before vs after** traffic conditions
- Demonstrate reduced emergency response time

---

##  Core Concepts Used

- Traffic Flow Optimization  
- Priority-Aware Routing  
- QUBO (Quadratic Unconstrained Binary Optimization)  
- Quantum-Inspired Optimization (Simulated Annealing)  
- Emergency Corridor Creation  
- Streamlit-based Visualization  

---
##  Technologies Used

### Programming & Frameworks
- **Python** – Core programming language
- **Streamlit** – Interactive web-based dashboard for visualization and user interaction

### Traffic & Graph Processing
- **OpenStreetMap (OSM)** – Real-world road network data
- **OSMnx** – Road network extraction and graph construction
- **NetworkX** – Graph modeling and shortest-path routing

### Optimization & Algorithms
- **dimod** – QUBO formulation and quantum-inspired solvers
- **Simulated Annealing** – Classical solver for QUBO optimization  
-  **D-Wave Ocean SDK** – Hybrid / quantum solver support

### Traffic Simulation 
- **SUMO (Simulation of Urban Mobility)** – Realistic traffic simulation
- **TraCI** – Python API for interacting with SUMO simulations

### Visualization & Analysis
- **Matplotlib** – Charts and plots
- **Streamlit Metrics & Charts** – Result comparison and performance display

### Collaboration & Development Tools
- **Git & GitHub** – Version control and team collaboration
- **Notion** – Documentation and report writing

---

##  Data Sources

- **Road Network:** OpenStreetMap (via OSMnx)
- **Traffic Data:** Synthetically generated
- **Emergency Vehicles:** Manually assigned with higher priority weights

> Real-time traffic data is not used. Simulation-based evaluation is standard practice in academic research.
---
##  How to Run

```bash
git clone https://github.com/Joann-jk/Quantum-Traffic-Priority-Routing.git
cd Quantum-Traffic-Priority-Routing
pip install -r requirements.txt
streamlit run app.py

