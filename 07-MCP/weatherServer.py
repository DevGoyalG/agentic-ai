# Import FastMCP to create an MCP server
from mcp.server.fastmcp import FastMCP

# Create an MCP server named "Weather"
mcp=FastMCP("Weather")

# Register the get_weather function as an MCP tool
@mcp.tool()
async def get_weather(location:str)->str:
    """
    Get the weather for a given location
    """

    # Return a sample weather response.
    # This is hardcoded demo data, not real-time weather information.
    return "It's always raining in California"

if __name__ == "__main__":
    mcp.run(transport="streamable-http")