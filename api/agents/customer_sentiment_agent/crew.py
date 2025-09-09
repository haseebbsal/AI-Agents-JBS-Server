from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool, ScrapeWebsiteTool
from pydantic import BaseModel, Field
from collections import Counter
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize LLM with environment variables
llm = LLM(
    model=os.getenv("MODEL"),
    temperature=0.7,
    top_p=0.9,
    frequency_penalty=0,
    presence_penalty=0.1,
    stop=["END"],
    seed=42,
    base_url="https://api.openai.com/v1",
    api_key=os.getenv("OPENAI_API_KEY"),
)


class SentimentReport(BaseModel):
    positive_feedback: list = Field(default_factory=list, description="Positive feedback")
    neutral_feedback: list = Field(default_factory=list, description="Neutral feedback")
    negative_feedback: list = Field(default_factory=list, description="Negative feedback")
    sentiment_distribution: dict = Field(default_factory=dict, description="Sentiment breakdown")
    key_themes: dict = Field(default_factory=dict, description="Key recurring themes")
    actionable_insights: str = Field(default="", description="Actionable insights summary")


@CrewBase
class CustomerSentimentCrew:
    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def search_agent(self) -> Agent:
        return Agent(config=self.agents_config["search_agent"], tools=[SerperDevTool()], llm=llm)

    @agent
    def scraping_agent(self) -> Agent:
        return Agent(config=self.agents_config["scraping_agent"], tools=[ScrapeWebsiteTool()], llm=llm)

    @agent
    def sentiment_analysis_agent(self) -> Agent:
        return Agent(config=self.agents_config["sentiment_analysis_agent"], llm=llm)

    @agent
    def report_generation_agent(self) -> Agent:
        return Agent(config=self.agents_config["report_generation_agent"], llm=llm)

    def extract_key_themes(self, feedback):
        themes = Counter(word.lower() for f in feedback for word in f.split() if word)
        return themes.most_common(5)

    def generate_actionable_insights(self, themes, geographical_location):
        insights = []
        if "claims" in [t[0] for t in themes.get("negative", [])]:
            insights.append(f"Improve claims processing in {geographical_location}.")
        if "pricing" in [t[0] for t in themes.get("neutral", [])]:
            insights.append(f"Adjust pricing strategies for {geographical_location}.")
        return " ".join(insights)

    @task
    def search_task(self) -> Task:
        return Task(
            config=self.tasks_config["search_task"],
            agent=self.search_agent(),
        )

    @task
    def scraping_task(self) -> Task:
        return Task(
            config=self.tasks_config["scraping_task"],
            agent=self.scraping_agent(),
            context=[self.search_task()],
            async_execution=True
        )

    @task
    def sentiment_analysis_task(self) -> Task:
        return Task(
            config=self.tasks_config["sentiment_analysis_task"],
            agent=self.sentiment_analysis_agent(),
            context=[self.scraping_task()],
        )

    @task
    def generate_report_task(self) -> Task:
        def generate_report(context):
            sentiment_data = context.get("sentiment_analysis_task_output", {})
            geographical_location = context.get("inputs", {}).get("geographical_location", "the specified region")
            themes = {
                "positive": self.extract_key_themes(sentiment_data.get("positive", [])),
                "neutral": self.extract_key_themes(sentiment_data.get("neutral", [])),
                "negative": self.extract_key_themes(sentiment_data.get("negative", [])),
            }
            insights = self.generate_actionable_insights(themes, geographical_location)
            return SentimentReport(
                positive_feedback=sentiment_data.get("positive", []),
                neutral_feedback=sentiment_data.get("neutral", []),
                negative_feedback=sentiment_data.get("negative", []),
                sentiment_distribution={
                    "positive": len(sentiment_data.get("positive", [])),
                    "neutral": len(sentiment_data.get("neutral", [])),
                    "negative": len(sentiment_data.get("negative", [])),
                },
                key_themes=themes,
                actionable_insights=insights,
            )

        return Task(
            config=self.tasks_config["generate_report_task"],
            agent=self.report_generation_agent(),
            context=[self.sentiment_analysis_task()],
            output_function=generate_report,
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
