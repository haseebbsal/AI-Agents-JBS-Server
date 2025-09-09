from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task, before_kickoff, after_kickoff
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from docx import Document  # Library to handle .docx files
import os

load_dotenv()

@CrewBase
class DocumentProcessor:
    """Document Processor for translation, content analysis, and categorization."""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @before_kickoff
    def preprocess_inputs(self, inputs):
        """
        Preprocess the uploaded document, extract its content, and detect the language.
        """
        file_path = inputs['document_file']
        if not file_path:
            raise ValueError("No document file provided!")
        
        print(f"Processing file: {file_path}")

        # Determine the file type and extract content accordingly
        file_extension = os.path.splitext(file_path)[1].lower()
        document_text = ""

        try:
            if file_extension == ".pdf":
                # Extract text from the PDF
                reader = PdfReader(file_path)
                document_text = "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])
            elif file_extension == ".docx":
                # Extract text from a Word document
                doc = Document(file_path)
                document_text = "\n".join([paragraph.text for paragraph in doc.paragraphs if paragraph.text.strip()])
            elif file_extension == ".txt":
                # Extract text from a plain text file
                with open(file_path, 'r', encoding='utf-8') as txt_file:
                    document_text = txt_file.read()
            else:
                raise ValueError(f"Unsupported file type: {file_extension}")

            if not document_text.strip():
                raise ValueError("The provided file is empty or unreadable.")
            
            inputs["document_text"] = document_text
            print(f"Extracted Document Text (First 500 chars):\n{document_text[:500]}...")
        except Exception as e:
            print(f"Failed to process {file_extension} file: {e}")
            inputs["document_text"] = "Error extracting text from the document."

        return inputs

    @after_kickoff
    def log_results(self, output):
        """
        Log the crew outputs.
        """
        print("Execution completed successfully!")
        print(f"Results: {output}")
        return output

    @agent
    def translator(self) -> Agent:
        """
        Translator Agent: Translates the document to English if needed.
        """
        return Agent(
            config=self.agents_config['translator'],
            verbose=True
        )

    @agent
    def analyzer(self) -> Agent:
        """
        Analyzer Agent: Extracts key information from the document.
        """
        return Agent(
            config=self.agents_config['analyzer'],
            verbose=True
        )

    @agent
    def formatter(self) -> Agent:
        """
        Formatter Agent: Formats the analysis into a structured document.
        """
        return Agent(
            config=self.agents_config['formatter'],
            verbose=True
        )

    @task
    def translate_task(self) -> Task:
        """
        Task to translate the document into English.
        """
        return Task(
            config=self.tasks_config['translate_task'],
            async_execution=True
        )

    @task
    def analyze_content_task(self) -> Task:
        """
        Task to analyze the translated document and extract key components.
        """
        return Task(
            config=self.tasks_config['analyze_task'],
        )

    @task
    def format_document_task(self) -> Task:
        """
        Task to format the extracted information into a structured document.
        """
        return Task(
            config=self.tasks_config['format_task'],
        )

    @crew
    def crew(self) -> Crew:
        """
        Create the Document Processor crew.
        """
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
