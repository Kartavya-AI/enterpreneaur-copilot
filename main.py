import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from src.crew.ene_crew import EntrepreneurshipCrew

load_dotenv()

app = FastAPI(title="Entrepreneurship Copilot API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=False,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Define the input schema
class CrewInput(BaseModel):
    startup_idea: str
    target_market: str
    team_composition: str

# Load crew on startup
crew_instance = EntrepreneurshipCrew()

@app.post("/run-crew/")
async def run_crew(input_data: CrewInput):
    try:
        print("🚀 Running Entrepreneurship Crew...")
        result = crew_instance.crew().kickoff(inputs=input_data.dict())
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error running crew: {str(e)}")
