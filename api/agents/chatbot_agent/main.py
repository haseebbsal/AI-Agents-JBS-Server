#!/usr/bin/env python
import sys
import warnings
import time
from dotenv import load_dotenv
from crew import ChatCrew

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")
load_dotenv()


def initialize_policy_crew(pdf_path):
    """
    Initialize the PolicyCrew with the given PDF file.
    """
    print(f"Initializing PolicyCrew with file: {pdf_path}")
    return ChatCrew(pdf_path=pdf_path)


def send_query(policy_crew, query, context):
    """
    Send a query to the PolicyCrew and handle errors or empty responses.
    """
    inputs = {
        "query": query,
        "context": context,
    }
    print(f"Sending query: {query}")
    try:
        start_time = time.time()  # Start timing
        response = policy_crew.crew().kickoff(inputs=inputs)
        end_time = time.time()  # End timing

        execution_time = end_time - start_time  # Calculate execution time
        print(f"Execution Time: {execution_time:.2f} seconds")
        print(f"Response: {response}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")


if __name__ == "__main__":
    # Initialize the crew with the PDF file
    policy_pdf_path = r"D:\AI_Backend\AI_Agents_20\customer-support-2.pdf"
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
