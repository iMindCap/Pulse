"""
Pulse - System Metrics Collector

Collects CPU, memory, disk, and temperature metrics from the host system.
"""

import psutil


async def get_system_metrics() -> dict:
    """Collect current system metrics."""
    # CPU
    cpu_percent = psutil.cpu_percent(interval=1)
    cpu_count = psutil.cpu_count()
    cpu_freq = psutil.cpu_freq()

    # Memory
    memory = psutil.virtual_memory()

    # Disk
    disk = psutil.disk_usage("/")

    # Temperature (not available on all systems)
    cpu_temp = None
    try:
        temps = psutil.sensors_temperatures()
        if temps:
            # Try common sensor names
            for name in ["coretemp", "cpu_thermal", "k10temp", "zenpower"]:
                if name in temps:
                    cpu_temp = temps[name][0].current
                    break
            # Fallback: use the first available sensor
            if cpu_temp is None:
                first_sensor = list(temps.values())[0]
                cpu_temp = first_sensor[0].current
    except (AttributeError, IndexError, KeyError):
        cpu_temp = None

    # Uptime
    boot_time = psutil.boot_time()

    return {
        "cpu": {
            "percent": cpu_percent,
            "cores": cpu_count,
            "freq_mhz": round(cpu_freq.current, 0) if cpu_freq else None,
        },
        "memory": {
            "percent": memory.percent,
            "used_gb": round(memory.used / (1024**3), 2),
            "total_gb": round(memory.total / (1024**3), 2),
            "available_gb": round(memory.available / (1024**3), 2),
        },
        "disk": {
            "percent": disk.percent,
            "used_gb": round(disk.used / (1024**3), 2),
            "total_gb": round(disk.total / (1024**3), 2),
            "free_gb": round(disk.free / (1024**3), 2),
        },
        "temperature": {
            "cpu_celsius": cpu_temp,
        },
        "boot_time": boot_time,
    }