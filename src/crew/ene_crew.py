#!/usr/bin/env python3
import os
import yaml
from crewai import Agent, Task, Crew, Process, LLM
from crewai.project import CrewBase, agent, crew, task
from dotenv import load_dotenv
from src.crew.tools.websearch import web_search_tool

# Load environment variables
load_dotenv()
os.getenv("GEMINI_API_KEY")

@CrewBase
class EntrepreneurshipCrew:
    """Entrepreneurship Copilot Crew for generating business plans, MVP plans, and GTM strategies."""
    
    def __init__(self):
        # Initialize Gemini LLM
        self.llm = LLM(
            model="gemini/gemini-2.0-flash",
        )
        
        # Load configuration files
        self.agents_config = self._load_config('config/agents.yaml')
        self.tasks_config = self._load_config('config/tasks.yaml')
    
    def _load_config(self, file_path):
        """Load YAML configuration file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return yaml.safe_load(file)
        except FileNotFoundError:
            print(f"Configuration file {file_path} not found.")
            return {}
        except yaml.YAMLError as e:
            print(f"Error parsing YAML file {file_path}: {e}")
            return {}
    
    @agent
    def business_strategy_agent(self) -> Agent:
        return Agent(
            config=self.agents_config.get('business_strategy_agent', {}),
            llm=self.llm,
            verbose=True,
            tools=[web_search_tool]
        )
    
    @agent
    def mvp_development_agent(self) -> Agent:
        return Agent(
            config=self.agents_config.get('mvp_development_agent', {}),
            llm=self.llm,
            verbose=True,
            tools=[web_search_tool]
        )
    
    @agent
    def gtm_strategy_agent(self) -> Agent:
        return Agent(
            config=self.agents_config.get('gtm_strategy_agent', {}),
            llm=self.llm,
            verbose=True,
            tools=[web_search_tool]
        )
    
    @task
    def business_plan_task(self) -> Task:
        return Task(
            config=self.tasks_config.get('business_plan_task', {}),
            agent=self.business_strategy_agent()
        )
    
    @task
    def mvp_plan_task(self) -> Task:
        return Task(
            config=self.tasks_config.get('mvp_plan_task', {}),
            agent=self.mvp_development_agent(),
            context=[self.business_plan_task()]
        )
    
    @task
    def gtm_strategy_task(self) -> Task:
        return Task(
            config=self.tasks_config.get('gtm_strategy_task', {}),
            agent=self.gtm_strategy_agent(),
            context=[self.business_plan_task(), self.mvp_plan_task()]
        )
    
    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True
        )