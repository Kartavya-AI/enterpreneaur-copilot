from crewai_tools import SerperDevTool
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize the web search tool
# This tool uses Serper to perform web searches, which is useful for gathering real-time information
# Note: SerperDevTool requires SERPER_API_KEY to be set in environment variables

try:
    web_search_tool = SerperDevTool()
except Exception as e:
    # If SerperDevTool fails to initialize, create a fallback
    print(f"Warning: Could not initialize SerperDevTool: {e}")
    web_search_tool = None