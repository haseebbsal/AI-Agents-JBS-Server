#!/usr/bin/env python
import sys
import warnings
from dotenv import load_dotenv
from crew import OnboardingChatbot

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")
load_dotenv()


def run():
    """
    Run the crew.
    """
    inputs = {
        "query": "which cases are considered as grievances here?",
        "context":"user:What if I have a grievance with my manager, I want to know how to either resolve it or get it to the right person, assistant:If you have a grievance with your manager, start by discussing it with them directly to try and resolve it within 30 days. If that doesn't work or you feel uncomfortable, write to the HR Manager within 30 days. If still unresolved, escalate it in writing to Senior Managers or the CEO. For issues involving the CEO, contact the Board Chairman. Be sure to clearly state the policy violated and who is involved. The company will investigate and respond within 30 days, ensuring no retaliation for raising your concern.,user:which cases are considered as grievances here?",
        "pdf_path": "uploaded_files/HUMAN_RESOURCE_POLICIES_GESCI__June_2018.pdf"
    }
    OnboardingChatbot(inputs=inputs).crew().kickoff(inputs=inputs)


def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        "query": "<current user query>",
        "context":"<context or chat history>",
        "pdf_path": "<update path here>"
    }
    try:
        OnboardingChatbot(inputs=inputs).crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        OnboardingChatbot().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        "query": "current user query",
        "context":"context or chat history",
        "pdf_path": "update path here"
    }
    try:
        OnboardingChatbot(inputs=inputs).crew().test(n_iterations=int(sys.argv[1]), openai_model_name=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")


if __name__=="__main__":
    run()