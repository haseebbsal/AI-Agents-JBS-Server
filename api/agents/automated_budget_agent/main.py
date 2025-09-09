#!/usr/bin/env python
from crew import AutomatedBudgetingAgent
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()




def run():
    """
    Entry point for the Automated Budgeting Agent.
    """
    try:
        # Get file path from the user
        file_path = input("Enter the path to the 12-month budget file (.csv): ").strip()
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        # Specify region
        region = input("Enter the region or country: ").strip()

        # Prepare inputs
        inputs = {
            "file_path": file_path,
            "region": region,
        }

        # Initialize and run the agent
        output = AutomatedBudgetingAgent(inputs=inputs).crew().kickoff(inputs=inputs)

        print("\nGenerated Output:")
        print(output)
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    run()
