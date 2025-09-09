from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from dotenv import load_dotenv

load_dotenv()



from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type
from openai import OpenAI
from pathlib import Path
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class OpenAITranscriptionToolInput(BaseModel):
    """
    Input schema for OpenAITranscriptionTool.
    """
    audio_file_path: str = Field(..., description="Path to the audio file to transcribe.")

class OpenAITranscriptionTool(BaseTool):
    """
    A tool for transcribing audio using OpenAI's Whisper model.
    """
    name: str = "OpenAI Transcription Tool"
    description: str = (
        "Transcribes audio files into text using OpenAI's Whisper API. "
        "Provide the path to the audio file as input."
    )
    args_schema: Type[BaseModel] = OpenAITranscriptionToolInput

    def _run(self, audio_file_path: str) -> str:
        """
        Transcribes an audio file using OpenAI's Whisper API.

        Args:
            audio_file_path (str): Path to the audio file to transcribe.

        Returns:
            str: Transcribed text from the audio file.
        """
        try:
            # Validate file existence
            audio_path = Path(audio_file_path)
            print(audio_path)
            if not audio_path.exists():
                raise FileNotFoundError(f"Audio file not found at: {audio_file_path}")

            # Log transcription process
            print(f"Transcribing audio from: {audio_file_path}")

            # Transcribe audio
            with open(audio_file_path, "rb") as audio_file:
                response = client.audio.translations.create(
                    model="whisper-1",
                    file=audio_file
                )
                print(response.text)
                return response.text
        except FileNotFoundError as e:
            return f"File not found error: {e}"
        except Exception as e:
            return f"An error occurred during transcription: {e}"

    def _arun(self, *args, **kwargs):
        """
        This tool does not currently support asynchronous execution.
        """
        raise NotImplementedError("OpenAITranscriptionTool does not support async execution.")


@CrewBase
class UserStoryCrew:
    """UserStoryCrew generates Agile user stories based on audio responses."""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @agent
    def transcription_agent(self) -> Agent:
        """
        Agent to handle transcription of audio responses.
        """
        return Agent(
            config=self.agents_config['transcription_agent'],
            tools=[OpenAITranscriptionTool()],
            verbose=True
        )

    @agent
    def story_generator_agent(self) -> Agent:
        """
        Agent to generate user stories from transcriptions.
        """
        return Agent(
            config=self.agents_config['story_generator_agent'],
            verbose=True
        )

    @task
    def transcription_task(self) -> Task:
        """
        Task to transcribe audio responses.
        """
        return Task(
            config=self.tasks_config['transcription_task'],
            inputs={"audio_responses": "{audio_responses}"},
            agent=self.transcription_agent(),
            async_execution=True
        )

    @task
    def story_generation_task(self) -> Task:
        """
        Task to generate user stories based on transcriptions.
        """
        return Task(
            config=self.tasks_config['story_generation_task'],
            context=[self.transcription_task()],
            agent=self.story_generator_agent(),
			logic="""
			Thought: I will analyze the transcriptions to extract user roles, functionality, and benefits.
			Action: Extract key elements from transcriptions.
			Observation: Extracted components include roles, functionalities, and benefits.
			Thought: I now have all the necessary components to generate Agile user stories.
			Final Answer: Generated Agile user stories.
			"""
        )

    @crew
    def crew(self) -> Crew:
        """
        Create the UserStoryCrew workflow.
        """
        return Crew(
            agents=self.agents,
            tasks=[self.transcription_task(), self.story_generation_task()],
            process=Process.sequential,
            verbose=True
        )
