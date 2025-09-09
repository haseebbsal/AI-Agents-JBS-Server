from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import PDFSearchTool


@CrewBase
class ChatCrew:
    """ChatCrew handles a single RAG workflow for a merged PDF."""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    def __init__(self, pdf_paths):
        if len(pdf_paths) != 1:
            raise ValueError("Exactly one merged PDF file must be provided.")
        
        # Initialize the PDF search tool for the merged PDF
        self.pdf_search_tool = PDFSearchTool(
            pdf=pdf_paths[0],
            config=dict(
                llm=dict(provider="openai"),
                embedder=dict(
                    provider="openai",
                    config=dict(model="text-embedding-ada-002")
                )
            )
        )

    @agent
    def scraper(self) -> Agent:
        """
        Scraper agent for extracting content from the merged PDF.
        """
        return Agent(
            config=self.agents_config['scraper'],
            tools=[self.pdf_search_tool],
            verbose=True
        )

    @agent
    def query_resolver(self) -> Agent:
        """
        Query resolver agent to answer user queries.
        """
        return Agent(
            config=self.agents_config['query_resolver'],
            verbose=True,
            tools=[self.pdf_search_tool],

        )

    @task
    def scraping_task(self) -> Task:
        """
        Task for extracting relevant content from the merged PDF.
        """
        return Task(
            config=self.tasks_config['scraping_task'],
            agent=self.scraper(),
            async_execution=True
        )

    @task
    def query_resolver_task(self) -> Task:
        """
        Task for resolving queries using the extracted content.
        """
        return Task(
            config=self.tasks_config['query_resolver_task'],
            context=[self.scraping_task()],
            agent=self.query_resolver(),
            async_execution=True
        )

    @crew
    def crew(self) -> Crew:
        """
        Create the workflow for querying the merged PDF.
        """
        return Crew(
            agents=self.agents,
            tasks=[self.query_resolver_task()],
            process=Process.sequential,
            verbose=True
        )
