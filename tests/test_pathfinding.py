
import pytest

from algorithms.graph_engine import Graph
from algorithms.pathfinding import astar, dijkstra
from datasets.lab_network import build_lab_network


def test_dijkstra_finds_shortest_path():
    graph = build_lab_network()

    result = dijkstra(graph, "WS-001", "DB-001")

    assert result is not None
    assert result.total_cost == 7
    assert result.path[0] == "WS-001"
    assert result.path[-1] == "DB-001"


def test_dijkstra_finds_backup_path():
    graph = build_lab_network()

    result = dijkstra(graph, "WS-001", "BACKUP-001")

    assert result is not None
    assert result.total_cost == 10
    assert result.path == (
        "WS-001",
        "APP-001",
        "DB-001",
        "BACKUP-001",
    )


def test_astar_finds_optimal_path():
    graph = build_lab_network()

    # Admissible heuristic for the BACKUP-001 destination.
    heuristic = {
        "WS-001": 10,
        "APP-001": 8,
        "API-001": 5,
        "DB-001": 3,
        "BACKUP-001": 0,
    }

    result = astar(
        graph,
        "WS-001",
        "BACKUP-001",
        heuristic,
    )

    assert result is not None
    assert result.total_cost == 10
    assert result.path[0] == "WS-001"
    assert result.path[-1] == "BACKUP-001"


def test_astar_zero_heuristic_matches_dijkstra():
    graph = build_lab_network()

    dijkstra_result = dijkstra(
        graph,
        "WS-001",
        "BACKUP-001",
    )

    astar_result = astar(
        graph,
        "WS-001",
        "BACKUP-001",
        {},
    )

    assert astar_result is not None
    assert dijkstra_result is not None

    assert astar_result.total_cost == dijkstra_result.total_cost


def test_unreachable_destination():
    graph = Graph()

    graph.add_node("A")
    graph.add_node("B")

    result = dijkstra(graph, "A", "B")

    assert result is None


def test_unknown_start_node():
    graph = build_lab_network()

    with pytest.raises(ValueError):
        dijkstra(graph, "UNKNOWN", "DB-001")


def test_negative_heuristic_rejected():
    graph = build_lab_network()

    with pytest.raises(ValueError):
        astar(
            graph,
            "WS-001",
            "DB-001",
            {"WS-001": -1},
        )
