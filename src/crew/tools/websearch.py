from crewai_tools import SerperDevTool
from dotenv import load_dotenv
import os
# Load environment variables
load_dotenv()
# Ensure the GEMINI_API_KEY is set
if not os.getenv("GEMINI_API_KEY"):
    raise ValueError("GEMINI_API_KEY is not set. Please set your Google API key in the .env file.")
# Initialize the web search tool
# This tool uses Serper to perform web searches, which is useful for gathering real-time information

web_search_tool = SerperDevTool()