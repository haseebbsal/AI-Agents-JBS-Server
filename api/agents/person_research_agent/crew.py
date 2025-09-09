from crewai import Agent, Task, Crew
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool, WebsiteSearchTool, ScrapeWebsiteTool
from dotenv import load_dotenv
import os

# Load environment variables
from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
import requests
from bs4 import BeautifulSoup
import json
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



@CrewBase
class PersonResearchAgent:
    """Configuration for the Person Research Agent."""
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @agent
    def research_agent(self) -> Agent:
        """Combined agent for search and report generation."""
        return Agent(
            config=self.agents_config['research_agent'],
            tools=[SerperDevTool(), WebsiteSearchTool(), ScrapeWebsiteTool()],
            verbose=True,
            memory=False
        )

    @task
    def person_research_task(self) -> Task:
        """Single task to consolidate search and report generation."""
        return Task(
            config=self.tasks_config['research_task'],
            agent=self.research_agent(),
            async_execution=True,
            description=(
                "Collect and synthesize comprehensive public information about the person. "
                "Search public sources such as Perplexity, ChatGPT Search, LinkedIn, and Facebook, "
                "validate the information, and compile it into a structured report."
            )
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Person Research Agent crew."""
        return Crew(
            agents=[self.research_agent()],
            tasks=[self.person_research_task()],
            process="sequential",
            verbose=True,
            memory=False,
            max_retry_limit=3
        )
