
import pytest

from algorithms.graph_engine import Graph
from datasets.lab_network import build_lab_network


def test_graph_node_count():
    graph = build_lab_network()

    assert graph.summary()["total_nodes"] == 5


def test_graph_edge_count():
    graph = build_lab_network()

    assert graph.summary()["total_edges"] == 5


def test_bfs_traversal():
    graph = build_lab_network()

    result = graph.bfs("WS-001")

    assert result == [
        "WS-001",
        "APP-001",
        "API-001",
        "DB-001",
        "BACKUP-001",
    ]


def test_dfs_traversal():
    graph = build_lab_network()

    result = graph.dfs("WS-001")

    assert result == [
        "WS-001",
        "APP-001",
        "API-001",
        "DB-001",
        "BACKUP-001",
    ]


def test_reachability():
    graph = build_lab_network()

    result = graph.reachable_nodes("APP-001")

    assert result == {
        "API-001",
        "DB-001",
        "BACKUP-001",
    }


def test_directionality():
    graph = build_lab_network()

    assert graph.get_neighbors("APP-001") == [
        "API-001",
        "DB-001",
    ]

    assert graph.get_neighbors("DB-001") == [
        "BACKUP-001",
    ]


def test_invalid_edge_weight():
    graph = Graph()

    graph.add_node("A")
    graph.add_node("B")

    with pytest.raises(ValueError):
        graph.add_edge(
            "A",
            "B",
            weight=-5,
            relationship="test",
        )


def test_invalid_probability():
    graph = Graph()

    graph.add_node("A")
    graph.add_node("B")

    with pytest.raises(ValueError):
        graph.add_edge(
            "A",
            "B",
            weight=1,
            relationship="test",
            transition_probability=1.5,
        )


def test_duplicate_node():
    graph = Graph()
    graph.add_node("A")

    with pytest.raises(ValueError):
        graph.add_node("A")