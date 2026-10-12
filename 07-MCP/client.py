import asyncio
import os
import sys
from pathlib import Path

from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.agents import create_agent
from langchain_groq import ChatGroq
from dotenv import load_dotenv

# Get project directory and load environment variables
BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

# Define the asynchronous main function
async def main():
    # Check whether the Groq API key is available
    if not os.getenv("GROQ_API_KEY"):
        raise ValueError(
            "GROQ_API_KEY is missing. Add it to your .env file."
    )
    
    # Create an MCP client that connects to multiple MCP servers
    client=MultiServerMCPClient(
        {
            "math":{
                "command": sys.executable,
                "args": [str(BASE_DIR / "mathServer.py")],       # Ensure correct absolute path
                "transport":"stdio",
            },
            "weather":{
                "url":"http://localhost:8000/mcp",   # Ensure server is running here
                "transport":"streamable-http",
            }
        }
    )

    # Get tools from both MCP servers
    print("Connecting to MCP servers...")
    tools=await client.get_tools()
    print("Available tools:", [tool.name for tool in tools])

    # Initialize the Groq model and create the agent
    model=ChatGroq(model="openai/gpt-oss-120b")
    agent = create_agent(model, tools)

    # Ask a math question
    math_response=await agent.ainvoke(
        {"messages": [
            {
                "role":"user", 
                "content": "What is (45 +18) * 7? Use the math tools."
            }
        ]
        }
    )

    print("\nMath Response:")
    print(math_response["messages"][-1].content)

    # Ask a weather question
    weather_response = await agent.ainvoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": "What is the weather in California? Use the get_weather tool."
                }
            ]
        }
    )

    print("\nWeather Response:")
    print(weather_response["messages"][-1].content)


if __name__ == "__main__":
    asyncio.run(main())