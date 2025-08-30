"""
FastMCP quickstart example.

cd to the `examples/snippets/clients` directory and run:
    uv run server fastmcp_quickstart stdio
"""

from mcp.server.fastmcp import FastMCP

from tools.meteo import get_city_coordinates, get_weather_forecast

# Create an MCP server
mcp = FastMCP(
    name="Weather MCP",
    instructions="This MCP provides weather information."
)

# Add a weather tool
@mcp.tool(
    title="Get Weather for a City",
    description="Get the weather information"
)
def get_weather(city: str) -> dict:
    """
    Get the weather information
    
    Args:
        city (str): The name of the city to get the weather for.

    Returns:
        dict: A dictionary containing the weather information.
    """
    coordinates = get_city_coordinates(city)
    if not coordinates:
        return {
            "error": "City not found"
        }
    lat, lon = coordinates
    forecast = get_weather_forecast(lat, lon)
    if not forecast:
        return {
            "error": "Weather forecast not available"
        }
    return {
        "city": city,
        "forecast": forecast,
        "latitude": lat,
        "longitude": lon,
    }

def main():
    """Run the MCP server."""
    print("Starting MCP server...")
    mcp.run()
