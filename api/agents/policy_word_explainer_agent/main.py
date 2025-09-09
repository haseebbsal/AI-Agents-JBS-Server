#!/usr/bin/env python
import sys
import warnings
from dotenv import load_dotenv
from crew import PolicyCrew

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")
load_dotenv()


def initialize_policy_crew(pdf_path):
    """
    Initialize the PolicyCrew with the given PDF file.
    """
    print(f"Initializing PolicyCrew with file: {pdf_path}")
    return PolicyCrew(pdf_path=pdf_path)


def send_query(policy_crew, query, context):
    """
    Send a query to the PolicyCrew.
    """
    inputs = {
        "query": query,
        "context": context,
    }
    print(f"Sending query: {query}")
    try:
        policy_crew.crew().kickoff(inputs=inputs)
    except Exception as e:
        print(f"An error occurred: {str(e)}")


if __name__ == "__main__":
    # Initialize the crew with the PDF file
    policy_pdf_path = r"D:\AI_Backend\AI_Agents_20\policy-pdf.pdf"
    policy_crew = initialize_policy_crew(policy_pdf_path)

    # Interactive loop to send queries
    context = "Initial context or chat history"
    while True:
        user_query = input("Enter your query (type 'exit' to quit): ")
        if user_query.lower() == 'exit':
            print("Exiting the chatbot.")
            break

        send_query(policy_crew, query=user_query, context=context)
        context = f"{context} | {user_query}"  # Update context with the new query
