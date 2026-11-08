
import platform
import socket
from datetime import UTC, datetime

import psutil


def collect_local_asset() -> dict:
    """
    Collect read-only inventory information from the
    machine running VigilantGraph.
    """

    hostname = socket.gethostname()

    # Collect network interfaces and their IP addresses.
    network_interfaces = []

    interface_addresses = psutil.net_if_addrs()
    interface_stats = psutil.net_if_stats()

    for interface_name, addresses in interface_addresses.items():

        interface_ips = []

        for address in addresses:

            if address.family == socket.AF_INET:
                ip_address = address.address

                if not ip_address.startswith("127."):
                    interface_ips.append(ip_address)

            elif address.family == socket.AF_INET6:
                ip_address = address.address.split("%")[0]

                if ip_address != "::1":
                    interface_ips.append(ip_address)

        if interface_ips:
            stats = interface_stats.get(interface_name)

            network_interfaces.append(
                {
                    "name": interface_name,
                    "ip_addresses": sorted(set(interface_ips)),
                    "is_up": stats.isup if stats else None,
                    "speed_mbps": (
                        stats.speed
                        if stats and stats.speed > 0
                        else None
                    ),
                }
            )

    # Collect disk information.
    disks = []

    for partition in psutil.disk_partitions(all=False):

        try:
            usage = psutil.disk_usage(partition.mountpoint)

            disks.append(
                {
                    "mountpoint": partition.mountpoint,
                    "filesystem": partition.fstype,
                    "total_bytes": usage.total,
                    "used_bytes": usage.used,
                    "free_bytes": usage.free,
                }
            )

        except (PermissionError, OSError):
            # Some mounted volumes may not be accessible.
            continue

    # Collect system information.
    memory = psutil.virtual_memory()

    asset = {
        "hostname": hostname,
        "operating_system": platform.system(),
        "os_release": platform.release(),
        "os_version": platform.version(),
        "architecture": platform.machine(),
        "processor": platform.processor(),
        "cpu_logical_cores": psutil.cpu_count(logical=True),
        "memory_total_bytes": memory.total,
        "memory_available_bytes": memory.available,
        "network_interfaces": network_interfaces,
        "disks": disks,
        "collection_timestamp": datetime.now(UTC).isoformat(),
    }

    return asset