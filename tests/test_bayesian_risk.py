
import pytest

from algorithms.bayesian_risk import (
    calculate_expected_impact,
    propagate_risk,
    topological_sort,
)
from algorithms.graph_engine import Graph
from datasets.lab_network import build_lab_network


def test_topological_sort_respects_dependencies():
    graph = build_lab_network()

    ordered = topological_sort(graph)

    positions = {
        node_id: index
        for index, node_id in enumerate(ordered)
    }

    for source_id in graph.adjacency:
        for target_id in graph.get_neighbors(source_id):
            assert positions[source_id] < positions[target_id]


def test_risk_propagates_from_initial_compromise():
    graph = build_lab_network()

    results = propagate_risk(
        graph,
        {"WS-001": 0.60},
    )

    assert results["WS-001"] == pytest.approx(0.60)
    assert results["APP-001"] == pytest.approx(0.33)
    assert results["API-001"] == pytest.approx(0.2145)


def test_multiple_paths_are_combined():
    graph = build_lab_network()

    results = propagate_risk(
        graph,
        {"WS-001": 0.60},
    )

    assert results["DB-001"] == pytest.approx(0.2623302)


def test_backup_risk_propagates():
    graph = build_lab_network()

    results = propagate_risk(
        graph,
        {"WS-001": 0.60},
    )

    assert results["BACKUP-001"] == pytest.approx(
        0.15739812
    )


def test_uncompromised_isolated_nodes_have_zero_risk():
    graph = Graph()

    graph.add_node("A")
    graph.add_node("B")

    results = propagate_risk(graph)

    assert results == {
        "A": 0.0,
        "B": 0.0,
    }


def test_invalid_baseline_probability_rejected():
    graph = build_lab_network()

    with pytest.raises(ValueError):
        propagate_risk(
            graph,
            {"WS-001": 1.5},
        )


def test_unknown_baseline_node_rejected():
    graph = build_lab_network()

    with pytest.raises(ValueError):
        propagate_risk(
            graph,
            {"UNKNOWN": 0.5},
        )


def test_cycles_are_rejected():
    graph = Graph()

    graph.add_node("A")
    graph.add_node("B")

    graph.add_edge("A", "B", 1, "test", 0.5)
    graph.add_edge("B", "A", 1, "test", 0.5)

    with pytest.raises(ValueError, match="cycle"):
        topological_sort(graph)


def test_expected_impact_calculation():
    graph = build_lab_network()

    probabilities = {
        "WS-001": 0.60,
        "APP-001": 0.33,
    }

    results = calculate_expected_impact(
        graph,
        probabilities,
    )

    assert results["WS-001"] == pytest.approx(2.4)
    assert results["APP-001"] == pytest.approx(2.64)
