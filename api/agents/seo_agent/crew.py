from crewai import Agent, Crew, Process, Task,LLM
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool, ScrapeWebsiteTool,WebsiteSearchTool
from dotenv import load_dotenv
import os


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
class SeoAgent():
    """SEO Agent with customer domain and geographical targeting."""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @agent
    def keyword_insights_agent(self) -> Agent:
        """Keyword Insights Agent"""
        return Agent(
            config=self.agents_config['keyword_insights_agent'],
            tools=[SerperDevTool()],
            llm=llm,
            verbose=True,
        )

    @agent
    def related_keywords_agent(self) -> Agent:
        """Related Keywords Agent"""
        return Agent(
            config=self.agents_config['related_keywords_agent'],
            tools=[SerperDevTool()],
            llm=llm,
            verbose=True,
        )

    @agent
    def seo_competitor_agent(self) -> Agent:
        """SEO Competitor Agent"""
        return Agent(
            config=self.agents_config['seo_competitor_agent'],
            tools=[ScrapeWebsiteTool(),SerperDevTool(),WebsiteSearchTool()],
            llm=llm,
            verbose=True,
        )

    @agent
    def seo_recommendation_agent(self) -> Agent:
        """SEO Recommendation Agent"""
        return Agent(
            config=self.agents_config['seo_recommendation_agent'],
            tools=[SerperDevTool()],
            llm=llm,
            verbose=True,
        )

    @task
    def keyword_insights_task(self) -> Task:
        """Keyword Insights Task"""
        return Task(
            config=self.tasks_config['keyword_insights_task'],
            agent=self.keyword_insights_agent(),
        )

    @task
    def related_keyword_task(self) -> Task:
        """Related Keywords Task"""
        return Task(
            config=self.tasks_config['related_keyword_task'],
            agent=self.related_keywords_agent(),
        )

    @task
    def seo_competitor_task(self) -> Task:
        """Competitor Analysis Task"""
        return Task(
            config=self.tasks_config['seo_competitor_task'],
            agent=self.seo_competitor_agent(),
            async_execution=True
        )

    @task
    def seo_recommendation_task(self) -> Task:
        """SEO Recommendations Task"""
        return Task(
            config=self.tasks_config['seo_recommendation_task'],
            agent=self.seo_recommendation_agent(),
        )

    @crew
    def crew(self) -> Crew:
        """Creates the SeoAgent crew for customer domain and geographical location."""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
            max_retry_limit=3
        )
