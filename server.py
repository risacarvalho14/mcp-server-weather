from typing import Any
import httpx
from mcp.server import MCPServer

mcp = MCPServer("weather")

OPENMETEO_API_BASE = "https://api.open-meteo.com/v1"
GEOCODING_API_BASE = "https://geocoding-api.open-meteo.com/v1"
USER_AGENT = "weather-app/1.0"


async def make_openmeteo_request(
    url: str,
    params: dict[str, Any] | None = None
) -> dict[str, Any] | None:
    """Call an Open-Meteo API endpoint and return JSON data."""

    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/json",
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                url,
                params=params,
                headers=headers,
                timeout=30.0
            )
            response.raise_for_status()
            return response.json()

        except Exception:
            return None


async def get_coordinates(
    city: str,
    province: str
) -> tuple[float, float] | None:
    """Convert a city and province into latitude and longitude."""

    params = {
        "name": city,
        "count": 10,
        "language": "en",
        "format": "json",
    }

    data = await make_openmeteo_request(
        f"{GEOCODING_API_BASE}/search",
        params=params
    )

    if not data or "results" not in data:
        return None

    for result in data["results"]:
        admin1 = result.get("admin1", "")

        if province.lower() in admin1.lower():
            return result["latitude"], result["longitude"]

    return None


@mcp.tool()
async def get_current_weather(
    city: str,
    province: str
) -> dict[str, Any] | str:
    """Get current weather for a city and province."""

    coordinates = await get_coordinates(city, province)

    if not coordinates:
        return f"Could not find coordinates for {city}, {province}."

    latitude, longitude = coordinates

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": (
            "temperature_2m,"
            "apparent_temperature,"
            "relative_humidity_2m,"
            "precipitation,"
            "rain,"
            "showers,"
            "snowfall,"
            "cloud_cover,"
            "wind_speed_10m"
        ),
    }

    data = await make_openmeteo_request(
        f"{OPENMETEO_API_BASE}/forecast",
        params=params
    )

    if not data:
        return f"Unable to fetch weather data for {city}, {province}."

    return {
        "city": city,
        "province": province,
        "latitude": latitude,
        "longitude": longitude,
        "weather": data,
    }


if __name__ == "__main__":
    mcp.run(transport="stdio")