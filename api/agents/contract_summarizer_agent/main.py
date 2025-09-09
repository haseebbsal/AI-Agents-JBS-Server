#!/usr/bin/env python
import warnings
from crew import ContractSummarizer

warnings.filterwarnings("ignore", category=SyntaxWarning)

def run():
    """
    Run the crew with specified inputs.
    """
    # Provide the relative path to the PDF file
    inputs = {
        'contract_file': 'D:\AI_Backend\AI_Agents_20\contract-summ.pdf'  # Use the absolute path here
    }

    try:
        response=ContractSummarizer().crew().kickoff(inputs=inputs)
        print(response)
    except Exception as e:
        print(f"An error occurred during execution: {e}")

if __name__ == "__main__":
    run()
