from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from langchain_openai import ChatOpenAI
import os


@CrewBase
class DigitalTwinAgent:
    """DigitalTwinAgent crew"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"



    @agent
    def jordan_miller(self) -> Agent:
        """Persona agent for Jordan Miller."""
        return Agent(
            config=self.agents_config["jordan_miller"],
            verbose=True,
        )

    @agent
    def emily_and_michael_thompson(self) -> Agent:
        """Persona agent for Emily and Michael Thompson."""
        return Agent(
            config=self.agents_config["emily_and_michael_thompson"],
            verbose=True,
        )

    @agent
    def linda_and_robert_johnson(self) -> Agent:
        """Persona agent for Linda and Robert Johnson."""
        return Agent(
            config=self.agents_config["linda_and_robert_johnson"],
            verbose=True,
        )

    @agent
    def sarah_martinez(self) -> Agent:
        """Persona agent for Sarah Martinez."""
        return Agent(
            config=self.agents_config["sarah_martinez"],
            verbose=True,
        )

    @agent
    def alex_and_taylor_morgan(self) -> Agent:
        """Persona agent for Alex and Taylor Morgan."""
        return Agent(
            config=self.agents_config["alex_and_taylor_morgan"],
            verbose=True,
        )

    @agent
    def mia_chen(self) -> Agent:
        """Persona agent for Mia Chen."""
        return Agent(
            config=self.agents_config["mia_chen"],
            verbose=True,
        )

    @agent
    def daniel_nguyen(self) -> Agent:
        """Persona agent for Daniel Nguyen."""
        return Agent(
            config=self.agents_config["daniel_nguyen"],
            verbose=True,
        )

    @agent
    def alex_rodriguez(self) -> Agent:
        """Persona agent for Alex Rodriguez."""
        return Agent(
            config=self.agents_config["alex_rodriguez"],
            verbose=True,
        )

    @task
    def research_task(self) -> Task:
        try:
            return Task(
                config=self.tasks_config["research_task"],
                agents=[
                    self.jordan_miller(),
                    self.emily_and_michael_thompson(),
                    self.linda_and_robert_johnson(),
                    self.sarah_martinez(),
                    self.alex_and_taylor_morgan(),
                    self.mia_chen(),
                    self.daniel_nguyen(),
                    self.alex_rodriguez(),
                ],
                async_execution=True
            )
        except KeyError as e:
            raise Exception(f"Agent or config missing: {e}")

    @crew
    def crew(self) -> Crew:
        """Creates the DigitalTwinAgent crew."""
        return Crew(
            agents=self.agents,  
            tasks=self.tasks,  
            process=Process.hierarchical,  
            manager_llm=ChatOpenAI(model=os.getenv("MODEL")),  
            verbose=True,
        )
