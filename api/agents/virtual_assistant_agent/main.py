#!/usr/bin/env python
import sys
import warnings
from dotenv import load_dotenv
from PyPDF2 import PdfMerger
from crew import ChatCrew

warnings.filterwarnings("ignore", category=SyntaxWarning)
load_dotenv()


def merge_pdfs(pdf_paths, output_path="merged.pdf"):
    """
    Merge multiple PDFs into one.
    
    Args:
        pdf_paths (list): List of paths to the PDF files.
        output_path (str): Path to save the merged PDF.
    
    Returns:
        str: Path to the merged PDF.
    """
    if len(pdf_paths) == 1:
        return pdf_paths[0]  # No merging needed if only one PDF is provided

    merger = PdfMerger()
    for pdf in pdf_paths:
        merger.append(pdf)
    merger.write(output_path)
    merger.close()
    return output_path


def initialize_virtual_assistant(pdf_paths):
    """
    Initialize the Virtual Assistant with the given PDF(s).
    If there are two PDFs, they are merged before initializing.
    """
    # Merge PDFs if more than one is provided
    merged_pdf_path = merge_pdfs(pdf_paths)
    print(f"Using merged PDF at: {merged_pdf_path}")
    return ChatCrew(pdf_paths=[merged_pdf_path])


def get_pdf_paths():
    """
    Prompt the user to provide up to two PDF paths.
    
    Returns:
        list: List of provided PDF file paths.
    """
    pdf_paths = []
    for i in range(2):  # Allow up to two PDFs
        pdf_path = input(f"Enter the path for PDF {i + 1} (leave blank if no more PDFs): ").strip()
        if pdf_path:
            pdf_paths.append(pdf_path)
        else:
            break
    return pdf_paths


if __name__ == "__main__":
    # Get PDF paths from the user
    pdf_paths = get_pdf_paths()

    if len(pdf_paths) == 0:
        print("No PDF files provided. Exiting.")
        sys.exit(1)

    try:
        # Initialize the assistant with the provided PDF(s)
        assistant_crew = initialize_virtual_assistant(pdf_paths)

        # Interactive loop to handle queries
        context = "Initial context or chat history"
        while True:
            query = input("Enter your query (type 'exit' to quit): ").strip()
            if query.lower() == 'exit':
                print("Exiting the chatbot.")
                break

            try:
                # Send the query to the assistant
                response = assistant_crew.crew().kickoff(inputs={"query": query, "context": context})
                print(f"Response:\n{response}")
                context += f" | {query}"  # Update context with the current query
            except Exception as e:
                print(f"An error occurred: {str(e)}")

    except Exception as e:
        print(f"Failed to initialize the Virtual Assistant: {str(e)}")
