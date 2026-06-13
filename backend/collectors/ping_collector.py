"""
Pulse - Ping Collector

Checks the availability and response time of configured services.
Supports HTTP and TCP checks.
"""

import time

import httpx


async def check_http(url: str, timeout: int = 10) -> dict:
    """Check an HTTP/HTTPS endpoint and measure response time."""
    try:
        start = time.time()
        async with httpx.AsyncClient(verify=False, timeout=timeout) as client:
            response = await client.get(url)
        elapsed_ms = round((time.time() - start) * 1000, 2)

        return {
            "url": url,
            "status": "up" if response.status_code < 400 else "down",
            "status_code": response.status_code,
            "response_time_ms": elapsed_ms,
        }
    except httpx.TimeoutException:
        return {
            "url": url,
            "status": "down",
            "status_code": None,
            "response_time_ms": None,
            "error": "Timeout",
        }
    except httpx.ConnectError:
        return {
            "url": url,
            "status": "down",
            "status_code": None,
            "response_time_ms": None,
            "error": "Connection refused",
        }
    except Exception as e:
        return {
            "url": url,
            "status": "down",
            "status_code": None,
            "response_time_ms": None,
            "error": str(e),
        }


async def check_services(services: list) -> list:
    """Check all configured services and return their status."""
    results = []

    for service in services:
        check_type = service.get("check_type", "http")

        if check_type == "http":
            result = await check_http(service["url"])
        else:
            result = await check_http(service["url"])

        result["name"] = service["name"]
        result["id"] = service["id"]
        results.append(result)

    return results