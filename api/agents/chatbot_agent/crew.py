from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import PDFSearchTool


@CrewBase
class ChatCrew:
    """PolicyCrew handles PDF-based insurance policy queries and content summarization."""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    # Class-level variable to persist the PDF search tool across queries
    pdf_search_tool = None

    def __init__(self, pdf_path):
        """
        Initialize the crew and set up the PDF search tool.
        """
        if ChatCrew.pdf_search_tool is None or ChatCrew.pdf_search_tool.pdf_path != pdf_path:
            ChatCrew.pdf_search_tool = PDFSearchTool(
                pdf=pdf_path,
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
        Scraper agent to retrieve content from the PDF.
        """
        return Agent(
            config=self.agents_config['scraper'],
            tools=[ChatCrew.pdf_search_tool],
            verbose=True
        )

    @agent
    def query_resolver(self) -> Agent:
        """
        Query resolver agent to answer user queries by simplifying document content.
        """
        return Agent(
            config=self.agents_config['query_resolver'],
            verbose=True,
            tools=[ChatCrew.pdf_search_tool],

        )

    @task
    def scraping_task(self) -> Task:
        """
        Task for extracting relevant content from the PDF based on user query context.
        """
        return Task(
            config=self.tasks_config['scraping_task'],
            async_execution=True,
            agent=self.scraper(),
            logic="""
            Thought: I will extract all the document content first if section-specific queries fail.
            Action: Search a PDF's content
            Action Input: {"query": "all content"}
            Observation: If this fails, I will use fallback queries like 'Introduction' or 'Table of Contents.'
            """
        )

    @task
    def query_resolver_task(self) -> Task:
        """
        Task for resolving user queries and providing simplified, concise responses.
        """
        return Task(
            config=self.tasks_config['query_resolver_task'],
            agent=self.query_resolver(),
            context=self.scraping_task().context,
        )

    @crew
    def crew(self) -> Crew:
        """
        Create the PolicyCrew workflow.
        """
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
