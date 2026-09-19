# MCP Weather Server

A simple Model Context Protocol (MCP) server built with Python that retrieves real-time weather data using the Open-Meteo API.

Instead of requiring users to enter latitude and longitude manually, this project accepts a city and province, converts them into coordinates using the Open-Meteo Geocoding API, and then retrieves current weather data.

## What is MCP?

MCP stands for Model Context Protocol.

It provides a standard way for AI applications to connect to external tools, APIs, files, and services.

In this project, the MCP server exposes a weather tool that an MCP client can discover and call.

## Project Flow

User enters city + province
        ↓
MCP Tool
        ↓
Open-Meteo Geocoding API
        ↓
Latitude + Longitude
        ↓
Open-Meteo Weather API
        ↓
Current weather data
        ↓
Returned to MCP client

## Features

- Accepts city and province as input
- Converts location names into latitude and longitude
- Retrieves current weather data
- Returns structured JSON output
- Exposes weather functionality as an MCP tool
- Can be tested using MCP Inspector

## Weather Data Returned

- Temperature
- Apparent temperature
- Relative humidity
- Precipitation
- Rain
- Showers
- Snowfall
- Cloud cover
- Wind speed

## Technologies Used

- Python
- Model Context Protocol (MCP)
- MCP Python SDK
- httpx
- Open-Meteo Weather API
- Open-Meteo Geocoding API
- uv
- MCP Inspector

## Project Structure

mcp-server-weather/
├── server.py
├── pyproject.toml
├── uv.lock
├── README.md
├── .gitignore
├── .python-version
├── src/
└── .venv/

The .venv folder is excluded from Git using .gitignore.

## Installation

Clone the repository:

git clone https://github.com/risacarvalho14/mcp-server-weather.git

Navigate into the project:

cd mcp-server-weather

Create a virtual environment:

uv venv

Activate it on Windows:

.venv\Scripts\activate

Install the required dependencies:

uv add "mcp[cli]" httpx

## Run the MCP Server

Start the server in development mode:

mcp dev server.py

This launches MCP Inspector.

If uv or npx is not recognized, make sure they are available in your system PATH.

## Test with MCP Inspector

1. Connect to the server
2. Open the Tools tab
3. Select get_current_weather
4. Enter a city and province
5. Run the tool

Example:

city: Toronto
province: Ontario

The server will:

Toronto, Ontario
→ geocoding API
→ latitude / longitude
→ weather API
→ structured weather response

## MCP Tool

The main MCP tool is:

@mcp.tool()
async def get_current_weather(city: str, province: str):

This tool accepts:
- city
- province

and returns the current weather for that location.

## Example Output

{
  "city": "Toronto",
  "province": "Ontario",
  "latitude": 43.646603,
  "longitude": -79.38272,
  "weather": {
    "current": {
      "temperature_2m": 16.8,
      "apparent_temperature": 15.5,
      "relative_humidity_2m": 68,
      "precipitation": 0,
      "cloud_cover": 100,
      "wind_speed_10m": 16.3
    }
  }
}

## What I Learned

Through this project, I learned how to:

- Understand the MCP client-server architecture
- Build an MCP server using Python
- Expose Python functions as MCP tools
- Work with async API requests
- Use external APIs inside an MCP server
- Convert city names into geographic coordinates
- Return structured data to MCP clients
- Test MCP tools using MCP Inspector
- Manage Python environments using uv
- Version and publish an MCP project using Git and GitHub

## Future Improvements

- Add multi-day weather forecasts
- Make province optional
- Add country support
- Add location suggestions
- Improve error handling
- Return cleaner human-readable weather summaries
- Connect the MCP server directly to Claude Desktop

## Author

Risa Carvalho
GitHub: https://github.com/risacarvalho14

