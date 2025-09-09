import os
from langchain_community.document_loaders import PyMuPDFLoader
from docx import Document
from crew import ContractOptimizationCrew

def load_document(file_path: str):
    """
    Dynamically load a document using the appropriate loader based on the file type.
    Handles PDFs, DOCX, and TXT files.
    """
    if file_path.endswith(".pdf"):
        # Use PyMuPDFLoader for PDFs
        loader = PyMuPDFLoader(file_path)
        try:
            docs = loader.load()
            return "\n\n".join([doc.page_content for doc in docs if doc.page_content])
        except Exception as e:
            raise ValueError(f"Failed to load PDF document: {e}")

    elif file_path.endswith(".docx"):
        # Use python-docx for DOCX files
        try:
            doc = Document(file_path)
            return "\n\n".join([paragraph.text for paragraph in doc.paragraphs if paragraph.text.strip()])
        except Exception as e:
            raise ValueError(f"Failed to load DOCX document: {e}")

    elif file_path.endswith(".txt"):
        # Handle TXT files directly
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except Exception as e:
            raise ValueError(f"Failed to load TXT document: {e}")

    else:
        raise ValueError("Unsupported file type. Please upload a PDF, DOCX, or TXT file.")

def run():
    """
    Entry point for the Contract Optimization Agent.
    """
    try:
        # Get file path from the user
        file_path = input("Enter the path to the contract file: ").strip()

        # Validate file path
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        # Load the document content
        contract_text = load_document(file_path)
        print("Document loaded successfully. Extracted content:")
        print(contract_text[:500])  

        # Initialize and run the agent
        inputs = {"contract_text": contract_text}
        output = ContractOptimizationCrew().crew().kickoff(inputs=inputs)

        # Display results
        print("\nContract Optimization Report:")
        print(output)

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    run()
