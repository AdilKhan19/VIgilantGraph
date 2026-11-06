
"""
VigilantGraph - Initial simulated corporate network.

All assets and relationships in this dataset are synthetic.
"""

from algorithms.graph_engine import Graph


def build_lab_network() -> Graph:
    graph = Graph()

    # Corporate assets
    graph.add_node(
        "WS-001",
        hostname="EMPLOYEE-WS-01",
        asset_type="workstation",
        criticality=4,
    )

    graph.add_node(
        "APP-001",
        hostname="APP-SERVER-01",
        asset_type="application_server",
        criticality=8,
    )

    graph.add_node(
        "API-001",
        hostname="INTERNAL-API-01",
        asset_type="api_server",
        criticality=6,
    )

    graph.add_node(
        "DB-001",
        hostname="DB-SERVER-01",
        asset_type="database_server",
        criticality=10,
    )

    graph.add_node(
        "BACKUP-001",
        hostname="BACKUP-SERVER-01",
        asset_type="backup_server",
        criticality=9,
    )

    # Directed relationships
    graph.add_edge(
        "WS-001",
        "APP-001",
        weight=2,
        relationship="authorized_application_access",
        transition_probability=0.55,
    )

    graph.add_edge(
        "APP-001",
        "API-001",
        weight=3,
        relationship="authorized_api_access",
        transition_probability=0.65,
    )

    graph.add_edge(
        "APP-001",
        "DB-001",
        weight=5,
        relationship="authorized_database_access",
        transition_probability=0.40,
    )

    graph.add_edge(
        "API-001",
        "DB-001",
        weight=2,
        relationship="authorized_database_access",
        transition_probability=0.70,
    )

    graph.add_edge(
        "DB-001",
        "BACKUP-001",
        weight=3,
        relationship="authorized_backup_access",
        transition_probability=0.60,
    )

    return graph