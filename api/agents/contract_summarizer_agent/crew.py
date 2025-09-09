from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task, before_kickoff, after_kickoff
from dotenv import load_dotenv
from PyPDF2 import PdfReader
import os

load_dotenv()

@CrewBase
class ContractSummarizer:
    """Contract Summarizer Agent"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @before_kickoff
    def preprocess_inputs(self, inputs):
        """
        Preprocess the uploaded contract and extract its content.
        """
        file_path = inputs['contract_file']
        if not file_path:
            raise ValueError("No contract file provided!")
        
        
        print(f"Processing file: {file_path}")

        # Extract text from the PDF
        try:
            reader = PdfReader(file_path)
            contract_text = "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])
            if not contract_text.strip():
                raise ValueError("The provided PDF file is empty or unreadable.")
            
            inputs["contract_text"] = contract_text
            print(f"Extracted Contract Text (First 500 chars):\n{contract_text[:500]}...")
        except Exception as e:
            print(f"Failed to process PDF: {e}")
            inputs["contract_text"] = "Error extracting text from PDF."

        return inputs

    # @after_kickoff
    # def log_results(self, output):
    #     """
    #     Log crew outputs.
    #     """
    #     print("Execution completed successfully!")
    #     print(f"Results: {output}")
    #     return output

    @agent
    def extractor(self) -> Agent:
        """
        Extractor Agent: Parses the document and identifies key sections.
        """
        return Agent(
            config=self.agents_config['extractor'],
            verbose=True
        )

    @agent
    def summarizer(self) -> Agent:
        """
        Summarizer Agent: Summarizes the extracted information into concise points.
        """
        return Agent(
            config=self.agents_config['summarizer'],
            verbose=True
        )

    @agent
    def structurer(self) -> Agent:
        """
        Structurer Agent: Formats the summarized content into a markdown report.
        """
        return Agent(
            config=self.agents_config['structurer'],
            verbose=True
        )

    @task
    def extract_info_task(self) -> Task:
        """
        Task to extract key sections from the document.
        """
        return Task(
            config=self.tasks_config['extract_task'],
            async_execution=True
        )

    @task
    def summarize_info_task(self) -> Task:
        """
        Task to summarize extracted key information.
        """
        return Task(
            config=self.tasks_config['summarize_task'],
        )

    @task
    def structure_report_task(self) -> Task:
        """
        Task to structure the summary into a markdown report.
        """
        return Task(
            config=self.tasks_config['structure_task'],
        )

    @crew
    def crew(self) -> Crew:
        """
        Create the Contract Summarizer crew.
        """
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
