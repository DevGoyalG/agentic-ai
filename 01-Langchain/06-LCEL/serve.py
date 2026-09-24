# Import required libraries
from fastapi import FastAPI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq
from langserve import add_routes

# Import environment variables
import os
from dotenv import load_dotenv

# Load variables from .env file
load_dotenv()

# Get Groq API key from environment variables
groq_api_key = os.getenv("GROQ_API_KEY")

# Initialize the Groq chat model
model = ChatGroq(model="openai/gpt-oss-120b", groq_api_key=groq_api_key)


# Create prompt template
system_template = "Translate the following into {language}:"

# Define system and user messages for the prompt
prompt_template = ChatPromptTemplate.from_messages([
    ('system', system_template),
    ('user', '{text}')
])

# Create output parser to convert the model response into a string
parser = StrOutputParser()


# Create LCEL Chain
# Prompt → Model → Output Parser
chain = prompt_template|model|parser


# Create FastAPI application
app = FastAPI(title="Langchain Server",
              version="1.0",
              description="A simple API server using Langchain runnable interfaces"
)


# Add the LCEL chain as an API route
add_routes(
    app,
    chain,
    path="/chain"
)


# Run the FastAPI server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)


# Flow : 

# User Input
#     ↓
# Prompt Template
#     ↓
# Groq Chat Model
#     ↓
# StrOutputParser
#     ↓
# FastAPI /chain Endpoint


# After running it, open: http://localhost:8000/
# Go to: http://localhost:8000/docs
# Here, you can see several GET and POST API endpoints.