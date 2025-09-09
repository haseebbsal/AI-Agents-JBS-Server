#!/usr/bin/env python

import sys
from crew import PersonResearchAgent
from dotenv import load_dotenv
import time

# Load environment variables
load_dotenv()

def run():
    """
    Entry point to run the Person Research Agent.
    """
    try:
        # Record the start time
        start_time = time.time()

        # Collect input from the user
        person = input("Enter the name or social media link of the person to research: ")

        # Run the agent
        inputs = {"person": person}
        output = PersonResearchAgent().crew().kickoff(inputs=inputs)

        # Calculate execution time
        total_time = (time.time() - start_time) / 60

        # Display results
        print("\nComprehensive Research Report:")
        print(output)
        print(f"\nExecution Time: {total_time:.2f} minutes")

    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    run()
