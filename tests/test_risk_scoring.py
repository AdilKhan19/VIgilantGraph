
import pytest

from algorithms.bayesian_risk import propagate_risk
from algorithms.graph_engine import Graph
from algorithms.risk_scoring import rank_assets_by_risk
from datasets.lab_network import build_lab_network


def test_assets_are_ranked_by_expected_impact():
    graph = build_lab_network()

    probabilities = propagate_risk(
        graph,
        {"WS-001": 0.60},
    )

    rankings = rank_assets_by_risk(
        graph,
        probabilities,
    )

    asset_order = [
        item["asset_id"]
        for item in rankings
    ]

    assert asset_order == [
        "APP-001",
        "DB-001",
        "WS-001",
        "BACKUP-001",
        "API-001",
    ]


def test_highest_risk_asset_is_first():
    graph = build_lab_network()

    probabilities = propagate_risk(
        graph,
        {"WS-001": 0.60},
    )

    rankings = rank_assets_by_risk(
        graph,
        probabilities,
    )

    assert rankings[0]["asset_id"] == "APP-001"
    assert rankings[0]["expected_impact"] == pytest.approx(2.64)


def test_ranking_is_descending():
    graph = build_lab_network()

    probabilities = propagate_risk(
        graph,
        {"WS-001": 0.60},
    )

    rankings = rank_assets_by_risk(
        graph,
        probabilities,
    )

    scores = [
        item["expected_impact"]
        for item in rankings
    ]

    assert scores == sorted(scores, reverse=True)


def test_equal_scores_use_asset_id_as_tiebreaker():
    graph = Graph()

    graph.add_node("B", criticality=5)
    graph.add_node("A", criticality=5)

    probabilities = {
        "B": 0.5,
        "A": 0.5,
    }

    rankings = rank_assets_by_risk(
        graph,
        probabilities,
    )

    assert [
        item["asset_id"]
        for item in rankings
    ] == ["A", "B"]