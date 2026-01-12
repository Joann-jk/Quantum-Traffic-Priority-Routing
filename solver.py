"""
solver.py
---------
Solves the Priority-Aware QUBO using classical or hybrid solvers.
Designed to be compatible with D-Wave quantum solvers.

Author: Your Team
"""

import dimod


# --------------------------------------------------
# 1. SOLVE USING SIMULATED ANNEALING (LOCAL)
# --------------------------------------------------

def solve_with_simulated_annealing(bqm, num_reads=100):
    """
    Solve the QUBO using classical Simulated Annealing.

    Args:
        bqm (BinaryQuadraticModel)
        num_reads (int)

    Returns:
        best_sample (dict)
    """
    sampler = dimod.SimulatedAnnealingSampler()
    sampleset = sampler.sample(bqm, num_reads=num_reads)

    best_sample = sampleset.first.sample
    return best_sample


# --------------------------------------------------
# 2. SOLVE USING EXACT SOLVER (SMALL PROBLEMS ONLY)
# --------------------------------------------------

def solve_exact(bqm):
    """
    Solve QUBO exactly (only for very small problems).

    Args:
        bqm (BinaryQuadraticModel)

    Returns:
        best_sample (dict)
    """
    sampler = dimod.ExactSolver()
    sampleset = sampler.sample(bqm)

    best_sample = sampleset.first.sample
    return best_sample


# --------------------------------------------------
# 3. OPTIONAL: D-WAVE HYBRID SOLVER (CLOUD)
# --------------------------------------------------

def solve_with_dwave_hybrid(bqm):
    """
    Solve QUBO using D-Wave Hybrid Solver (cloud-based).

    NOTE:
    Requires D-Wave credentials and Ocean SDK.

    Returns:
        best_sample (dict)
    """
    from dwave.system import LeapHybridSampler

    sampler = LeapHybridSampler()
    sampleset = sampler.sample(bqm)

    best_sample = sampleset.first.sample
    return best_sample


# --------------------------------------------------
# 4. DECODE SOLUTION INTO ROUTE SELECTION
# --------------------------------------------------

def decode_solution(sample, variable_map, vehicles):
    """
    Decode solver output into selected routes.

    Args:
        sample (dict): Binary solution
        variable_map (dict)
        vehicles (list)

    Returns:
        selected_routes (dict)
    """
    selected_routes = {}

    for (vid, r_idx), var_name in variable_map.items():
        if sample.get(var_name, 0) == 1:
            selected_routes[vid] = vehicles[vid]["candidate_routes"][r_idx]

    return selected_routes


# --------------------------------------------------
# 5. COMPLETE SOLVER PIPELINE
# --------------------------------------------------

def solve_traffic_qubo(bqm, variable_map, vehicles, method="sa"):
    """
    Full solver pipeline.

    Args:
        method (str): "sa", "exact", or "dwave"

    Returns:
        selected_routes (dict)
    """
    if method == "exact":
        sample = solve_exact(bqm)
    elif method == "dwave":
        sample = solve_with_dwave_hybrid(bqm)
    else:
        sample = solve_with_simulated_annealing(bqm)

    selected_routes = decode_solution(sample, variable_map, vehicles)
    return selected_routes
