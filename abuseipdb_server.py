import os
import httpx
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

load_dotenv()

mcp = FastMCP("abuseipdb")

@mcp.tool()
async def check_ip_reputation(ip_address: str, max_age: int = 90) -> str:
    """Check the abuse reputation of a single IP address."""
    key = os.environ['ABUSEIPDB_API_KEY']
    url = "https://api.abuseipdb.com/api/v2/check"
    headers = {'Key': key, 'Accept': 'application/json'}
    params = {'ipAddress': ip_address, 'maxAgeInDays': max_age}
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params, timeout=30.0)
        response.raise_for_status()
        return response.text

@mcp.tool()
async def check_ip_block(block: str) -> str:
    """Check if any IPs in a block are abusive."""
    key = os.environ['ABUSEIPDB_API_KEY']
    url = "https://api.abuseipdb.com/api/v2/check-block"
    headers = {'Key': key, 'Accept': 'application/json'}
    params = {'network': block, 'maxAgeInDays': 90}
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params, timeout=30.0)
        response.raise_for_status()
        return response.text
