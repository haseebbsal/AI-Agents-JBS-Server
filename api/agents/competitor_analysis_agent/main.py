# main.py

#!/usr/bin/env python
import sys
import warnings
from crew import CompetitorAnalysisAgent
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Access environment variables
api_key = os.getenv("OPENAI_API_KEY")
model = os.getenv("MODEL")

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

def run():
    """
    Run the Competitor Analysis Agent crew.
    """
    competitor1 = input("Enter the name of the first insurance company: ")
    competitor2 = input("Enter the name of the second insurance company (optional): ")
    area=input("Enter the area of insurance: ")
    
    inputs = {
        'competitor1': competitor1,
        'competitor2': competitor2 if competitor2 else None,
        'area':area
    }
    try:
        result = CompetitorAnalysisAgent().crew().kickoff(inputs=inputs)
        print(result)
    except Exception as e:
        print(f"An error occurred while running the crew: {e}")

if __name__ == "__main__":
    run()
