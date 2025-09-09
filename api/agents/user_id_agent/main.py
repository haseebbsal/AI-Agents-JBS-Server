import sys
from crew import IDReaderCrew

def run(image_path):
    """
    Main function to initialize the IDReaderCrew and process the ID image.
    """
    id_reader_crew = IDReaderCrew(image_path=image_path)
    inputs = {
        "image_path": image_path,
    }
    response = id_reader_crew.crew().kickoff(inputs=inputs)
    print(response)

if __name__ == "__main__":
    # Dynamically use the uploaded file path
    uploaded_image_path = r"D:\AI_Backend\AI_Agents_20\id-card.png"  
    try:
        run(uploaded_image_path)
    except FileNotFoundError as e:
        print(f"File not found: {str(e)}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
