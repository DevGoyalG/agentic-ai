# Import FastMCP to create an MCP server
from mcp.server.fastmcp import FastMCP

# Create an MCP server named "Math"
mcp=FastMCP("Math")

# Register the add function as an MCP tool
@mcp.tool()
def add(a:int,b:int)->int:
    """
    Add two numbers
    """
    return a+b

# Register the subtract function as an MCP tool
@mcp.tool()
def subtract(a:int,b:int)->int:
    """    
    Subtract two numbers
    """
    return a-b

# Register the multiply function as an MCP tool
@mcp.tool()
def multiply(a:int,b:int)->int:
    """
    Multiply two numbers
    """
    return a*b

# The transport="stdio" argument tells the server to:
# Use standard input/output (stdin and stdout) to receive and respond to tool function calls.

if __name__ == "__main__":
    mcp.run(transport="stdio")