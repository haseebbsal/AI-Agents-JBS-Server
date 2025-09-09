#!/usr/bin/env python

import sys
import time
from crew import CustomerResearchCrew
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def run():
    """
    Entry point to run the Customer Research Agent.
    """
    try:
        # Record the start time
        start_time = time.time()

        # Collect company name from the user
        company_name = input("Enter the name of the company to research: ").strip()

        # Validate input
        if not company_name:
            raise ValueError("Company name cannot be empty. Please provide a valid company name.")

        # Run the Customer Research Agent
        inputs = {
            "company_name": company_name,
        }
        output = CustomerResearchCrew().crew().kickoff(inputs=inputs)

        # Record the end time
        end_time = time.time()

        # Calculate total execution time in minutes
        total_time_minutes = (end_time - start_time) / 60

        # Display results
        print("\nComprehensive Research Report:")
        print(output)

        # Display total execution time
        print(f"\nTotal Time Taken: {total_time_minutes:.2f} minutes")

    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    run()
