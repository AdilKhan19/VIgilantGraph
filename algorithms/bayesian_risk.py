
from collections import deque
from math import isfinite

from algorithms.graph_engine import Graph


def topological_sort(graph: Graph) -> list[str]:
    """
    Sort graph nodes using Kahn's algorithm.

    Raises ValueError if the graph contains a cycle.
    """

    in_degree = {
        node_id: 0
        for node_id in graph.nodes
    }

    # Count incoming edges for every node.
    for source_id in graph.adjacency:
        for target_id in graph.get_neighbors(source_id):
            in_degree[target_id] += 1

    # Start with nodes that have no incoming edges.
    queue = deque(
        sorted(
            node_id
            for node_id, degree in in_degree.items()
            if degree == 0
        )
    )

    ordered_nodes = []

    while queue:
        current = queue.popleft()
        ordered_nodes.append(current)

        for neighbor in graph.get_neighbors(current):
            in_degree[neighbor] -= 1

            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    # If some nodes remain, the graph contains a cycle.
    if len(ordered_nodes) != len(graph.nodes):
        raise ValueError(
            "Risk propagation requires a directed acyclic graph. "
            "A cycle was detected."
        )

    return ordered_nodes


def propagate_risk(
    graph: Graph,
    baseline_priors: dict[str, float] | None = None,
) -> dict[str, float]:
    """
    Calculate compromise probabilities using a noisy-OR model.

    Assumptions:
    - The graph must be directed and acyclic.
    - Parent compromise events are treated as independent.
    - Propagation causes are treated as independent.
    """

    priors = baseline_priors or {}

    # Validate baseline probabilities.
    for node_id, probability in priors.items():

        if node_id not in graph.nodes:
            raise ValueError(
                f"Unknown node in baseline priors: {node_id}"
            )

        if (
            not isinstance(probability, (int, float))
            or not isfinite(probability)
            or not 0.0 <= probability <= 1.0
        ):
            raise ValueError(
                f"Invalid baseline probability for {node_id}"
            )

    # Calculate incoming edges for each node.
    incoming_edges = {
        node_id: []
        for node_id in graph.nodes
    }

    for source_id in graph.adjacency:
        for target_id in graph.get_neighbors(source_id):
            edge = graph.get_edge(source_id, target_id)
            incoming_edges[target_id].append(edge)

    # Process nodes in dependency order.
    ordered_nodes = topological_sort(graph)

    compromise_probability = {}

    for node_id in ordered_nodes:

        baseline = priors.get(node_id, 0.0)

        # Probability that no compromise cause succeeds.
        probability_of_no_compromise = 1.0 - baseline

        # Combine all incoming propagation causes.
        for edge in incoming_edges[node_id]:

            parent_probability = compromise_probability[
                edge.source
            ]

            propagation_probability = (
                parent_probability
                * edge.transition_probability
            )

            probability_of_no_compromise *= (
                1.0 - propagation_probability
            )

        # Convert probability of no compromise into
        # probability of compromise.
        compromise_probability[node_id] = (
            1.0 - probability_of_no_compromise
        )

    return compromise_probability


def calculate_expected_impact(
    graph: Graph,
    compromise_probabilities: dict[str, float],
) -> dict[str, float]:
    """
    Calculate expected impact using:

    Expected impact = compromise probability * asset criticality

    Criticality is expected to be a numeric node metadata value.
    """

    results = {}

    for node_id, probability in compromise_probabilities.items():

        if node_id not in graph.nodes:
            raise ValueError(
                f"Unknown node in compromise probabilities: {node_id}"
            )

        if (
            not isinstance(probability, (int, float))
            or not isfinite(probability)
            or not 0.0 <= probability <= 1.0
        ):
            raise ValueError(
                f"Invalid compromise probability for {node_id}"
            )

        criticality = graph.nodes[node_id].get(
            "criticality",
            1,
        )

        if (
            not isinstance(criticality, (int, float))
            or not isfinite(criticality)
            or criticality < 0
        ):
            raise ValueError(
                f"Invalid criticality value for {node_id}"
            )

        results[node_id] = probability * criticality

    return results