
from algorithms.bayesian_risk import calculate_expected_impact
from algorithms.graph_engine import Graph


def rank_assets_by_risk(
    graph: Graph,
    compromise_probabilities: dict[str, float],
) -> list[dict[str, float | str]]:
    """
    Rank assets from highest to lowest expected impact.

    Expected impact = compromise probability * criticality.
    """

    expected_impacts = calculate_expected_impact(
        graph,
        compromise_probabilities,
    )

    rankings = []

    for node_id, expected_impact in expected_impacts.items():
        criticality = graph.nodes[node_id].get(
            "criticality",
            1,
        )

        rankings.append(
            {
                "asset_id": node_id,
                "compromise_probability": (
                    compromise_probabilities[node_id]
                ),
                "criticality": criticality,
                "expected_impact": expected_impact,
            }
        )

    # Highest expected impact first.
    # Asset ID provides deterministic ordering for ties.
    rankings.sort(
        key=lambda item: (
            -item["expected_impact"],
            item["asset_id"],
        )
    )

    return rankings