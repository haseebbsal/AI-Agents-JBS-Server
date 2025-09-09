from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import PDFSearchTool





@CrewBase
class OnboardingChatbot():
	"""OnboardingChatbot crew"""

	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	def create_pdf_search_tool(self, pdf_path):
		pdf_search_tool = PDFSearchTool(
			pdf=pdf_path,
		)
		return pdf_search_tool
	
	def __init__(self, inputs):
		self.pdf_search_tool = self.create_pdf_search_tool(inputs["pdf_path"])
		
		

	
	@agent
	def scraper(self) -> Agent:
		return Agent(config=self.agents_config['scraper'], tools=[self.pdf_search_tool], verbose=True)

	@agent
	def query_resolver(self) -> Agent:
		return Agent(config=self.agents_config['query_resolver'], verbose=True)

	@task
	def scraping_task(self) -> Task:
		return Task(config=self.tasks_config['scraping_task'],async_execution=True)

	@task
	def query_resolver_task(self) -> Task:
		return Task(config=self.tasks_config['query_resolver_task'])

	@crew
	def crew(self) -> Crew:
		"""Creates the PolicyAgenticRAG Crew"""
		return Crew(
			agents=self.agents,
			tasks=self.tasks,
			process=Process.sequential,
			verbose=True,
		)
