#!/usr/bin/env python
import sys
import warnings
from crew import EmergingRiskAgent

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

def run():
    """
    Run the crew.
    """
    inputs = {
        'area': input("Enter Geographical Location (e.g., North America, Asia, etc.): "),
        'product_lines': input("Relevant insurance product lines for emerging risk analysis separated by comma (Can be multiple)")
    }

    
    try:
        crew_instance = EmergingRiskAgent().crew()
        
        if not crew_instance:
            raise ValueError("Failed to initialize the Crew instance.")
        
        result = crew_instance.kickoff(inputs=inputs)
        
        # Print and return the result
        print("Crew Output:", result)
        return result
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)


def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        'area': 'North America',
        'product_lines': ['Property Insurance', 'Cyber Insurance']
    }
    try:
        EmergingRiskAgent().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")


def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        EmergingRiskAgent().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")


def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        'area': 'North America',
        'product_lines': ['Property Insurance', 'Cyber Insurance']
    }
    try:
        EmergingRiskAgent().crew().test(n_iterations=int(sys.argv[1]), openai_model_name=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")


if __name__ == '__main__':
    run()
