from crewai import Agent, Task, Crew
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool,WebsiteSearchTool
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

@CrewBase
class ContractOptimizationCrew:
    """Configuration for the Contract Optimization Crew."""
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @agent
    def document_analysis_agent(self) -> Agent:
        """
        This agent is responsible for analyzing the content of the uploaded contract.
        """
        return Agent(
            config=self.agents_config['document_analysis_agent'],
            tools=[SerperDevTool(),WebsiteSearchTool()],
            verbose=True,
            memory=False
        )

    @agent
    def suggestions_generation_agent(self) -> Agent:
        """
        This agent generates actionable suggestions for contract improvement.
        """
        return Agent(
            config=self.agents_config['suggestions_generation_agent'],
            verbose=True,
            memory=False
        )

    @task
    def analyze_document_task(self) -> Task:
        """
        Task to parse and analyze the uploaded document.
        """
        return Task(
            config=self.tasks_config['analyze_document_task'],
            agent=self.document_analysis_agent(),
            async_execution=True,
            description=(
                "Analyze the uploaded document to extract key terms and provisions, "
                "and check alignment with best practices."
            )
        )

    @task
    def generate_suggestions_task(self) -> Task:
        """
        Task to generate optimization suggestions for the contract.
        """
        return Task(
            config=self.tasks_config['generate_suggestions_task'],
            agent=self.suggestions_generation_agent(),
            context=[self.analyze_document_task()],
            description=(
                "Generate actionable suggestions for improving the contract "
                "based on extracted terms and best practices."
            )
        )

    @crew
    def crew(self) -> Crew:
        """
        Orchestrates the tasks and agents into a cohesive workflow.
        """
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process="sequential",
            verbose=True,
            memory=False,
            max_retry_limit=3
        )
