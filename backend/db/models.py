"""
Pulse - Database Models

Defines the SQLite tables for storing historical metrics.
"""

SCHEMA = """
CREATE TABLE IF NOT EXISTS system_metrics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    cpu_percent REAL NOT NULL,
    memory_percent REAL NOT NULL,
    memory_used_gb REAL NOT NULL,
    memory_total_gb REAL NOT NULL,
    disk_percent REAL NOT NULL,
    disk_used_gb REAL NOT NULL,
    disk_total_gb REAL NOT NULL,
    cpu_temp REAL
);

CREATE TABLE IF NOT EXISTS container_metrics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    container_id TEXT NOT NULL,
    container_name TEXT NOT NULL,
    status TEXT NOT NULL,
    cpu_percent REAL,
    memory_usage_mb REAL,
    memory_limit_mb REAL,
    network_rx_mb REAL,
    network_tx_mb REAL
);

CREATE TABLE IF NOT EXISTS service_checks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    service_name TEXT NOT NULL,
    url TEXT NOT NULL,
    status TEXT NOT NULL,
    response_time_ms REAL,
    status_code INTEGER
);

CREATE TABLE IF NOT EXISTS services (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    url TEXT NOT NULL,
    check_type TEXT NOT NULL DEFAULT 'http',
    is_active INTEGER NOT NULL DEFAULT 1,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
"""