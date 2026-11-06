
"""
VigilantGraph - Corporate Network Graph Engine

Implements a directed, weighted graph using an adjacency list.

Core capabilities:
- Asset/node management
- Directed relationship management
- Breadth First Search (BFS)
- Depth First Search (DFS)
- Reachability analysis
"""

from collections import deque
from dataclasses import dataclass, field
from math import isfinite
from typing import Any


@dataclass(frozen=True)
class Edge:
    """Represents a directed relationship between two assets."""

    source: str
    target: str
    weight: float
    relationship: str
    transition_probability: float


@dataclass
class Graph:
    """
    Directed weighted graph for corporate network modeling.

    adjacency:
        Maps each node to its outgoing edges.

    nodes:
        Stores metadata associated with each asset.
    """

    nodes: dict[str, dict[str, Any]] = field(default_factory=dict)

    adjacency: dict[str, dict[str, Edge]] = field(
        default_factory=dict
    )

    def add_node(
        self,
        node_id: str,
        **metadata: Any
    ) -> None:
        """Add a network asset to the graph."""

        if not node_id or not node_id.strip():
            raise ValueError("Node ID cannot be empty.")

        if node_id in self.nodes:
            raise ValueError(f"Node already exists: {node_id}")

        self.nodes[node_id] = metadata
        self.adjacency[node_id] = {}

    def add_edge(
        self,
        source: str,
        target: str,
        weight: float,
        relationship: str,
        transition_probability: float = 0.0,
    ) -> None:
        """Create a directed relationship between two assets."""

        if source not in self.nodes:
            raise ValueError(f"Unknown source node: {source}")

        if target not in self.nodes:
            raise ValueError(f"Unknown target node: {target}")

        if not isfinite(weight) or weight < 0:
            raise ValueError("Weight must be finite and non-negative.")

        if (
            not isfinite(transition_probability)
            or not 0 <= transition_probability <= 1
        ):
            raise ValueError(
                "Transition probability must be between 0 and 1."
            )

        edge = Edge(
            source=source,
            target=target,
            weight=weight,
            relationship=relationship,
            transition_probability=transition_probability,
        )

        self.adjacency[source][target] = edge

    def get_neighbors(self, node_id: str) -> list[str]:
        """Return outgoing neighbors of a node."""

        if node_id not in self.nodes:
            raise ValueError(f"Unknown node: {node_id}")

        return sorted(self.adjacency[node_id])

    def bfs(self, start: str) -> list[str]:
        """
        Breadth First Search.

        Explores the graph level by level.
        """

        if start not in self.nodes:
            raise ValueError(f"Unknown start node: {start}")

        visited = {start}
        queue = deque([start])
        traversal_order = []

        while queue:
            current = queue.popleft()
            traversal_order.append(current)

            for neighbor in self.get_neighbors(current):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)

        return traversal_order

    def dfs(self, start: str) -> list[str]:
        """
        Iterative Depth First Search.

        Explores one branch before returning.
        """

        if start not in self.nodes:
            raise ValueError(f"Unknown start node: {start}")

        visited = set()
        stack = [start]
        traversal_order = []

        while stack:
            current = stack.pop()

            if current in visited:
                continue

            visited.add(current)
            traversal_order.append(current)

            neighbors = self.get_neighbors(current)

            for neighbor in reversed(neighbors):
                if neighbor not in visited:
                    stack.append(neighbor)

        return traversal_order

    def reachable_nodes(self, start: str) -> set[str]:
        """
        Return every node reachable from the starting asset.

        The starting asset itself is excluded.
        """

        return set(self.bfs(start)) - {start}

    def get_edge(self, source: str, target: str) -> Edge | None:
        """Return a specific directed edge, if it exists."""

        if source not in self.nodes:
            raise ValueError(f"Unknown source node: {source}")

        if target not in self.nodes:
            raise ValueError(f"Unknown target node: {target}")

        return self.adjacency[source].get(target)

    def summary(self) -> dict[str, int]:
        """Return basic graph statistics."""

        edge_count = sum(
            len(neighbors)
            for neighbors in self.adjacency.values()
        )

        return {
            "total_nodes": len(self.nodes),
            "total_edges": edge_count,
        }