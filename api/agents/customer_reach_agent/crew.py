from typing import List
from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool,ScrapeWebsiteTool,WebsiteSearchTool
from dotenv import load_dotenv
import os

# Load environment variables
from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
import requests
from bs4 import BeautifulSoup
import json
import os
from dotenv import load_dotenv

load_dotenv()

class BrowserlessScraperInput(BaseModel):
    """
    Input schema for BrowserlessScraper tool.
    """
    url: str = Field(..., description="The URL of the website to scrape.")

class BrowserlessScraper(BaseTool):
    """
    A custom tool for scraping web pages using the Browserless.io service.
    """
    name: str = "Browserless Web Scraper"
    description: str = (
        "A tool for scraping websites using the Browserless.io service. "
        "Provide the URL of the target website and a valid Browserless API token."
    )
    args_schema: Type[BaseModel] = BrowserlessScraperInput

    def _run(self, url: str) -> str:
        """
        Scrape the text content of a webpage using Browserless.io and return the results.
        
        Args:
            url (str): The URL of the webpage to scrape.

        Returns:
            str: Extracted text content from the webpage or error message.
        """
        try:
            # Sending request to Browserless.io
            response = requests.post(
                "https://production-sfo.browserless.io/content",
                params={"token": os.getenv("BROWSERLESS_API_KEY")},
                json={
                    "waitForTimeout": 5000,
                    "url": url,
                },
                timeout=30  # Set a timeout for the request
            )
            response.raise_for_status()

            # Attempt to parse the response as JSON
            try:
                html_content = json.loads(response.text).get('content', '')
            except json.JSONDecodeError:
                return "Error: Unable to decode JSON response from Browserless.io."

            # Ensure content exists
            if not html_content:
                return "Error: No content returned from Browserless.io."

            # Parse the HTML content using BeautifulSoup
            soup = BeautifulSoup(html_content, 'html.parser')
            return soup.get_text(separator='\n', strip=True)

        except requests.exceptions.RequestException as e:
            return f"An error occurred while connecting to Browserless.io: {e}"
        except Exception as e:
            return f"An unexpected error occurred: {e}"


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
class CustomerResearchCrew:
    """CustomerResearchCrew configuration"""
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @agent
    def data_collection_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['data_collection_agent'],
            tools=[WebsiteSearchTool(), SerperDevTool()],
            verbose=True,
            llm=llm,
            memory=False
        )

    @agent
    def financial_analysis_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['financial_analysis_agent'],
            verbose=True,
            llm=llm,
        )

    @agent
    def market_intelligence_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['market_intelligence_agent'],
            verbose=True,
            llm=llm,
            memory=False
        )

    @agent
    def risk_assessment_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['risk_assessment_agent'],
            verbose=True,
            llm=llm,
            memory=False
        )

    @agent
    def report_generation_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['report_generation_agent'],
            verbose=True,
            llm=llm,
            memory=False
        )

    @task
    def data_collection_task(self) -> Task:
        return Task(
            config=self.tasks_config['data_collection_task'],
            agent=self.data_collection_agent(),
            async_execution=True
        )

    @task
    def financial_analysis_task(self) -> Task:
        return Task(
            config=self.tasks_config['financial_analysis_task'],
            agent=self.financial_analysis_agent(),
            context=[self.data_collection_task()]
        )

    @task
    def market_intelligence_task(self) -> Task:
        return Task(
            config=self.tasks_config['market_intelligence_task'],
            agent=self.market_intelligence_agent(),
            context=[self.data_collection_task()]
        )

    @task
    def risk_assessment_task(self) -> Task:
        return Task(
            config=self.tasks_config['risk_assessment_task'],
            agent=self.risk_assessment_agent(),
            context=[self.data_collection_task()]
        )

    @task
    def report_generation_task(self) -> Task:
        return Task(
            config=self.tasks_config['report_generation_task'],
            agent=self.report_generation_agent(),
            context=[
                self.financial_analysis_task(),
                self.market_intelligence_task(),
                self.risk_assessment_task()
            ]
        )

    @crew
    def crew(self) -> Crew:
        """Creates the CustomerResearchCrew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
            memory=False,
            max_retry_limit=3
        )
