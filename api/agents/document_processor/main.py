#!/usr/bin/env python
import warnings
from crew import DocumentProcessor

warnings.filterwarnings("ignore", category=SyntaxWarning)

def run():
    """
    Run the crew with specified inputs.
    """
    inputs = {
        'document_file': 'D:\AI_Backend\AI_Agents_20\contract-summ.pdf'  # Replace with the path to your document
    }

    try:
        output = DocumentProcessor().crew().kickoff(inputs=inputs)
        print("=============================================")
        print("output:\n", output) # the output can be collected here, so you can remove the line in crew.py that makes output file 
    except Exception as e:
        print(f"An error occurred during execution: {e}")

if __name__ == "__main__":
    run()
