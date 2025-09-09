#!/usr/bin/env python
import warnings
import time
from crew import DigitalTwinAgent

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")


def run():
    """
    Run the digital twin agent for an input describing a product or marketing idea.
    """
    # Single input field for product or marketing idea
    product_marketing_idea = input("Enter a description of the product or marketing idea: ").strip()
    area = input("Enter Geographical Location (e.g., North America, Asia, etc.): ").strip()

    # Validate input
    if not product_marketing_idea:
        raise ValueError("Description cannot be empty. Please provide a valid input.")

    inputs = {
        'product_marketing_idea': product_marketing_idea,
        'area': area
    }

    try:
        print("Processing...")
        start_time = time.time()  # Start timing
        output = DigitalTwinAgent().crew().kickoff(inputs=inputs)
        end_time = time.time()  # End timing

        execution_time = end_time - start_time  # Calculate execution time
        print(f"Execution Time: {execution_time:.2f} seconds")

        print("Results:")
        print(output)
    except Exception as e:
        print(f"An error occurred: {str(e)}")


if __name__ == "__main__":
    run()
