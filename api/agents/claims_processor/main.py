#!/usr/bin/env python
import warnings
from crew import ClaimsProcessor

warnings.filterwarnings("ignore", category=SyntaxWarning)

def run():
    """
    Run the crew with specified inputs.
    """
    inputs = {
        'rules_document': 'D:\AI_Backend\AI_Agents_20\claim_processing_agent\pdf_folder\Suggested rules on Police form.pdf',
        'claims_document': 'D:\AI_Backend\AI_Agents_20\claim_processing_agent\pdf_folder\ARC Accident 22172410011850.pdf'
        # 'claims_document': '../../pdf_folder/accidentReport1.pdf'
    }

    try:
        ClaimsProcessor().crew().kickoff(inputs=inputs)
    except Exception as e:
        print(f"An error occurred during execution: {e}")

if __name__ == "__main__":
    run()
