"""
Pulse - Docker Collector

Collects status and resource usage from Docker containers.
Communicates with Docker via the unix socket.
"""

import docker
from docker.errors import DockerException


def get_docker_client():
    """Create a Docker client connection."""
    try:
        client = docker.from_env()
        client.ping()
        return client
    except DockerException:
        return None


async def get_docker_info() -> dict:
    """Get general Docker engine info."""
    client = get_docker_client()
    if not client:
        return {"available": False, "error": "Docker is not available"}

    try:
        info = client.info()
        return {
            "available": True,
            "containers_running": info.get("ContainersRunning", 0),
            "containers_stopped": info.get("ContainersStopped", 0),
            "containers_total": info.get("Containers", 0),
            "images": info.get("Images", 0),
            "docker_version": info.get("ServerVersion", "unknown"),
        }
    except DockerException as e:
        return {"available": False, "error": str(e)}
    finally:
        client.close()


async def get_containers() -> list:
    """Get status and stats for all containers."""
    client = get_docker_client()
    if not client:
        return []

    try:
        containers = client.containers.list(all=True)
        result = []

        for container in containers:
            container_data = {
                "id": container.short_id,
                "name": container.name,
                "image": container.image.tags[0] if container.image.tags else "unknown",
                "status": container.status,
                "state": container.attrs["State"]["Status"],
                "created": container.attrs["Created"],
                "ports": _parse_ports(container.ports),
            }

            # Only get stats for running containers
            if container.status == "running":
                try:
                    stats = container.stats(stream=False)
                    container_data["stats"] = _parse_stats(stats)
                except Exception:
                    container_data["stats"] = None
            else:
                container_data["stats"] = None

            result.append(container_data)

        return result
    except DockerException:
        return []
    finally:
        client.close()


def _parse_ports(ports: dict) -> list:
    """Parse Docker port mappings into a clean format."""
    parsed = []
    if not ports:
        return parsed

    for container_port, host_bindings in ports.items():
        if host_bindings:
            for binding in host_bindings:
                parsed.append({
                    "container": container_port,
                    "host": f"{binding['HostIp']}:{binding['HostPort']}",
                })
        else:
            parsed.append({
                "container": container_port,
                "host": None,
            })

    return parsed


def _parse_stats(stats: dict) -> dict:
    """Parse Docker container stats into readable metrics."""
    # CPU usage calculation
    cpu_percent = 0.0
    cpu_delta = (
        stats["cpu_stats"]["cpu_usage"]["total_usage"]
        - stats["precpu_stats"]["cpu_usage"]["total_usage"]
    )
    system_delta = (
        stats["cpu_stats"]["system_cpu_usage"]
        - stats["precpu_stats"]["system_cpu_usage"]
    )
    num_cpus = stats["cpu_stats"]["online_cpus"]

    if system_delta > 0 and cpu_delta > 0:
        cpu_percent = round((cpu_delta / system_delta) * num_cpus * 100, 2)

    # Memory usage
    memory_usage = stats["memory_stats"].get("usage", 0)
    memory_limit = stats["memory_stats"].get("limit", 0)
    memory_usage_mb = round(memory_usage / (1024**2), 2)
    memory_limit_mb = round(memory_limit / (1024**2), 2)

    # Network I/O
    network_rx = 0
    network_tx = 0
    networks = stats.get("networks", {})
    for iface in networks.values():
        network_rx += iface.get("rx_bytes", 0)
        network_tx += iface.get("tx_bytes", 0)

    return {
        "cpu_percent": cpu_percent,
        "memory_usage_mb": memory_usage_mb,
        "memory_limit_mb": memory_limit_mb,
        "memory_percent": round((memory_usage / memory_limit) * 100, 2) if memory_limit > 0 else 0,
        "network_rx_mb": round(network_rx / (1024**2), 2),
        "network_tx_mb": round(network_tx / (1024**2), 2),
    }