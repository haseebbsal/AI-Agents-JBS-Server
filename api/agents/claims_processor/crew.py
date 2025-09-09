from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task, before_kickoff, after_kickoff
from dotenv import load_dotenv
from docx import Document  # For .docx files
from PyPDF2 import PdfReader  # For PDF files
import re
import os

load_dotenv()

@CrewBase
class ClaimsProcessor:
    """Claims Processing Agent"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @before_kickoff
    def preprocess_inputs(self, inputs):
        """
        Preprocess the uploaded documents: extract rules and claim text.
        """
        rules_path = inputs.get('rules_document')
        claims_path = inputs.get('claims_document')

        if not rules_path or not claims_path:
            raise ValueError("Both rules_document and claims_document paths must be provided!")

        print(f"Processing rules document: {rules_path}")
        print(f"Processing claims document: {claims_path}")

        try:
            # Extract rules from the predefined rules document
            rules_text = self._extract_text_from_file(rules_path)
            print("Extracted Rules:")
            print(rules_text[:500])

            # Extract claims content from the claims document
            claims_text = self._extract_text_from_file(claims_path)
            print("Extracted Claims Content:")
            print(claims_text[:500])

            # Clean extracted text
            inputs['rules_text'] = self._clean_text(rules_text)
            inputs['claims_text'] = self._clean_text(claims_text)
        except Exception as e:
            print(f"Error during preprocessing: {e}")
            raise ValueError("Failed to preprocess input documents.")

        return inputs

    def _extract_text_from_file(self, file_path):
        """
        Detect the file type by extension and extract text accordingly.
        """
        file_extension = os.path.splitext(file_path)[-1].lower()
        if file_extension == ".docx":
            return self._extract_text_from_docx(file_path)
        elif file_extension == ".pdf":
            return self._extract_text_from_pdf(file_path)
        elif file_extension == ".txt":
            return self._extract_text_from_txt(file_path)
        else:
            raise ValueError(f"Unsupported file format: {file_extension}")

    def _extract_text_from_docx(self, file_path):
        """Extract text from .docx files."""
        doc = Document(file_path)
        return "\n".join([para.text for para in doc.paragraphs if para.text.strip()])

    def _extract_text_from_pdf(self, file_path):
        """Extract text from PDF files."""
        reader = PdfReader(file_path)
        return "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])

    def _extract_text_from_txt(self, file_path):
        """Extract text from .txt files."""
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()

    def _clean_text(self, text):
        """
        Clean the text by removing unnecessary punctuation and fixing spaces.
        """
        text = re.sub(r"[^\S\r\n]+", " ", text)  # Replace multiple spaces with a single space
        text = re.sub(r"\s*\n\s*", "\n", text)  # Normalize newlines
        text = re.sub(r"[^\w\s.,;:'\"!?()-]", "", text)  # Remove unnecessary punctuation
        return text.strip()

    @after_kickoff
    def log_results(self, output):
        """
        Log crew outputs.
        """
        print("Execution completed successfully!")
        print(f"Final Output: {output}")
        return output

    @agent
    def analyzer(self) -> Agent:
        """
        Claims Analyzer Agent: Compares the claims document against predefined rules.
        """
        return Agent(
            config=self.agents_config['analyzer'],
            verbose=True
        )

    @agent
    def report_generator(self) -> Agent:
        """
        Compliance Report Generator Agent: Creates a markdown report of the analysis results.
        """
        return Agent(
            config=self.agents_config['report_generator'],
            verbose=True
        )

    @task
    def analyze_task(self) -> Task:
        """
        Task to analyze the claims content against predefined rules.
        """
        return Task(
            config=self.tasks_config['analyze_task'],
            inputs=lambda inputs: {
                "rules_text": inputs["rules_text"],
                "claims_text": inputs["claims_text"]
            },
            async_execution=True,
            callback=lambda output: print(f"Analysis Task Output: {output}")
        )

    @task
    def generate_report_task(self) -> Task:
        """
        Task to generate a structured markdown report of the analysis results.
        """
        return Task(
            config=self.tasks_config['generate_report_task'],
            inputs=lambda outputs: {"analysis_result": outputs["analyze_task"]},
            callback=lambda output: print(f"Report Task Output: {output}"),
        )

    @crew
    def crew(self) -> Crew:
        """
        Create the claims processing crew.
        """
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
