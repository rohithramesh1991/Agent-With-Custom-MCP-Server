import os
import httpx
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

load_dotenv()

mcp = FastMCP("weather")

@mcp.tool()
async def get_current_weather(latitude: float, longitude: float) -> str:
    """Get the current weather at given coordinates."""
    key = os.environ['WEATHERMAP_API_KEY']
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={key}&units=metric"
    async with httpx.AsyncClient() as client:
        response = await client.get(url, timeout=30.0)
        response.raise_for_status()
        return response.text

@mcp.tool()
async def get_forecast(city: str) -> str:
    """Get 5-day weather forecast for a city."""
    key = os.environ['WEATHERMAP_API_KEY']
    url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={key}&units=metric"
    async with httpx.AsyncClient() as client:
        response = await client.get(url, timeout=30.0)
        response.raise_for_status()
        return response.text