
"""
VigilantGraph - Risk-Aware Pathfinding Engine

Custom implementations of:
1. Dijkstra's shortest-path algorithm
2. A* heuristic search

The algorithms operate on our custom Graph data structure.
"""

from dataclasses import dataclass
from heapq import heappop, heappush
from itertools import count
from math import isfinite

from algorithms.graph_engine import Graph


@dataclass(frozen=True)
class PathResult:
    """Result returned by a pathfinding algorithm."""

    path: tuple[str, ...]
    total_cost: float
    explored_nodes: int


def _validate_endpoints(
    graph: Graph,
    start: str,
    goal: str,
) -> None:
    """Validate source and destination assets."""

    if start not in graph.nodes:
        raise ValueError(f"Unknown start node: {start}")

    if goal not in graph.nodes:
        raise ValueError(f"Unknown goal node: {goal}")


def _reconstruct_path(
    parents: dict[str, str],
    start: str,
    goal: str,
) -> tuple[str, ...]:
    """Reconstruct a path by following predecessor links."""

    path = [goal]
    current = goal

    while current != start:
        current = parents[current]
        path.append(current)

    path.reverse()

    return tuple(path)


def dijkstra(
    graph: Graph,
    start: str,
    goal: str,
) -> PathResult | None:
    """
    Calculate the minimum-cost path using Dijkstra.

    Returns None when no path exists.

    Complexity:
        O((V + E) log V) using a binary heap.
    """

    _validate_endpoints(graph, start, goal)

    distances = {
        node: float("inf")
        for node in graph.nodes
    }

    distances[start] = 0.0

    parents: dict[str, str] = {}

    sequence = count()

    priority_queue = [
        (0.0, next(sequence), start)
    ]

    explored = set()

    while priority_queue:
        current_distance, _, current = heappop(
            priority_queue
        )

        # Ignore outdated queue entries.
        if current_distance != distances[current]:
            continue

        if current in explored:
            continue

        explored.add(current)

        if current == goal:
            return PathResult(
                path=_reconstruct_path(
                    parents,
                    start,
                    goal,
                ),
                total_cost=current_distance,
                explored_nodes=len(explored),
            )

        for neighbor in graph.get_neighbors(current):

            edge = graph.get_edge(current, neighbor)

            candidate_distance = (
                current_distance + edge.weight
            )

            if candidate_distance < distances[neighbor]:

                distances[neighbor] = candidate_distance

                parents[neighbor] = current

                heappush(
                    priority_queue,
                    (
                        candidate_distance,
                        next(sequence),
                        neighbor,
                    ),
                )

    return None


def astar(
    graph: Graph,
    start: str,
    goal: str,
    heuristic: dict[str, float] | None = None,
) -> PathResult | None:
    """
    Calculate a minimum-cost path using A*.

    The supplied heuristic must be admissible for an
    optimality guarantee.

    Missing heuristic values are treated as zero.

    Complexity:
        Worst-case exponential with a general heuristic.
        With h(n)=0, behavior reduces to Dijkstra.
    """

    _validate_endpoints(graph, start, goal)

    heuristic = heuristic or {}

    for node, estimate in heuristic.items():

        if node not in graph.nodes:
            raise ValueError(
                f"Heuristic references unknown node: {node}"
            )

        if not isfinite(estimate) or estimate < 0:
            raise ValueError(
                "Heuristic values must be finite and non-negative."
            )

    def estimate(node: str) -> float:
        return heuristic.get(node, 0.0)

    g_score = {
        node: float("inf")
        for node in graph.nodes
    }

    g_score[start] = 0.0

    parents: dict[str, str] = {}

    sequence = count()

    priority_queue = [
        (
            estimate(start),
            0.0,
            next(sequence),
            start,
        )
    ]

    explored = set()

    while priority_queue:

        _, current_cost, _, current = heappop(
            priority_queue
        )

        # Ignore outdated queue entries.
        if current_cost != g_score[current]:
            continue

        explored.add(current)

        if current == goal:
            return PathResult(
                path=_reconstruct_path(
                    parents,
                    start,
                    goal,
                ),
                total_cost=current_cost,
                explored_nodes=len(explored),
            )

        for neighbor in graph.get_neighbors(current):

            edge = graph.get_edge(current, neighbor)

            tentative_cost = current_cost + edge.weight

            if tentative_cost < g_score[neighbor]:

                g_score[neighbor] = tentative_cost

                parents[neighbor] = current

                estimated_total = (
                    tentative_cost + estimate(neighbor)
                )

                heappush(
                    priority_queue,
                    (
                        estimated_total,
                        tentative_cost,
                        next(sequence),
                        neighbor,
                    ),
                )

    return None