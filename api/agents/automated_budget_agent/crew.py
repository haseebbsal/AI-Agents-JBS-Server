from tabulate import tabulate
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task,tool
from crewai_tools import CSVSearchTool
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

@CrewBase
class AutomatedBudgetingAgent:
    """Automated Budgeting Agent crew"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    def create_csv_search_tool(self, file_path):
        csv_search_tool = CSVSearchTool(
            csv=file_path,
        )
        return csv_search_tool

    def __init__(self, inputs):
        self.csv_search_tool = self.create_csv_search_tool(inputs["file_path"])

    @agent
    def researcher(self) -> Agent:
        """
        Researcher agent responsible for identifying market trends.
        """
        return Agent(
            config=self.agents_config['researcher'],
            tools=[self.csv_search_tool],
            verbose=True
        )

    @agent
    def forecaster(self) -> Agent:
        """
        Forecaster agent responsible for generating 12-month forecasts.
        """
        return Agent(
            config=self.agents_config['forecaster'],
            verbose=True
        )

    

    @task
    def analyze_budget(self) -> Task:
        """
        Task to parse and analyze the uploaded budget file and extract lines of business.
        """
        return Task(
            config=self.tasks_config['analyze_budget_task'],
            async_execution=True,
            agent=self.researcher(),
            description="Analyze the uploaded budget file to extract lines of business, budget figures, and financial trends."
        )

    @task
    def research_market(self) -> Task:
        """
        Task to research market trends for each line of business in the specified region.
        """
        return Task(
            config=self.tasks_config['research_market_task'],
            agent=self.researcher(),
            context=[self.analyze_budget()],
            description="Perform market research for each extracted line of business and generate insights specific to the region."
        )

    @task
    def generate_forecast(self) -> Task:
        """
        Task to generate a 12-month forecast based on analyzed data and market research.
        """
        return Task(
            config=self.tasks_config['generate_forecast_task'],
            agent=self.forecaster(),
            context=[self.analyze_budget(), self.research_market()],
            description="Generate a 12-month forecast using extracted budget data, lines of business, and regional market trends."
        )

        

    @crew
    def crew(self) -> Crew:
        """
        Orchestrates the AutomatedBudgetingAgent workflow.
        """
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True
        )
