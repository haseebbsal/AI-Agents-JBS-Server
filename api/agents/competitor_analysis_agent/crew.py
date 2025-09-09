import os
from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool, ScrapeWebsiteTool,WebsiteSearchTool
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize LLM with environment variables
llm = LLM(
    model=os.getenv("MODEL"), 
    temperature=0.8,
    top_p=0.9,
    frequency_penalty=0.1,
    presence_penalty=0.1,
    stop=["END"],
    seed=42,
    base_url="https://api.openai.com/v1",
    api_key=os.getenv("OPENAI_API_KEY")
)


@CrewBase
class CompetitorAnalysisAgent():
    """Competitor Analysis Agent for the insurance industry"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @agent
    def competitor_data_agent(self) -> Agent:
        """Competitor Data Retrieval Agent"""
        return Agent(
            config=self.agents_config['competitor_data_agent'],
            tools=[SerperDevTool(),WebsiteSearchTool()],
            verbose=True,
        )

    @agent
    def market_positioning_agent(self) -> Agent:
        """Market Positioning Agent"""
        return Agent(
            config=self.agents_config['market_positioning_agent'],
            tools=[SerperDevTool()],
            verbose=True,
        )

    @agent
    def performance_metrics_agent(self) -> Agent:
        """Performance Metrics Analysis Agent"""
        return Agent(
            config=self.agents_config['performance_metrics_agent'],
            verbose=True,
        )

    @agent
    def competitor_comparison_agent(self) -> Agent:
        """Competitor Comparison Agent"""
        return Agent(
            config=self.agents_config['competitor_comparison_agent'],
            tools=[SerperDevTool()],
            verbose=True,
            llm=llm  
        )

    @task
    def competitor_data_task(self) -> Task:
        """Competitor Data Retrieval Task"""
        return Task(
            config=self.tasks_config['competitor_data_task'],
            agent=self.competitor_data_agent(),
            async_execution=True
        )

    @task
    def market_positioning_task(self) -> Task:
        """Market Positioning Task"""
        return Task(
            config=self.tasks_config['market_positioning_task'],
            agent=self.market_positioning_agent(),
        )

    @task
    def performance_metrics_task(self) -> Task:
        """Performance Metrics Analysis Task"""
        return Task(
            config=self.tasks_config['performance_metrics_task'],
            agent=self.performance_metrics_agent(),
        )

    @task
    def competitor_comparison_task(self) -> Task:
        """Competitor Comparison Task"""
        return Task(
            config=self.tasks_config['competitor_comparison_task'],
            agent=self.competitor_comparison_agent(),
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Competitor Analysis Agent crew for the insurance industry"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,  
            verbose=True,
        )
