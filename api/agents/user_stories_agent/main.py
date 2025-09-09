#!/usr/bin/env python
import sys
import warnings
from dotenv import load_dotenv
from pathlib import Path
from crew import UserStoryCrew

warnings.filterwarnings("ignore", category=SyntaxWarning)
load_dotenv()


def play_audio(file_path):
    """
    Play a pre-recorded WAV audio file.
    
    Args:
        file_path (str): Path to the WAV audio file.
    """
    try:
        import simpleaudio as sa

        if file_path and Path(file_path).exists():
            print(f"Playing audio: {file_path}")
            wave_obj = sa.WaveObject.from_wave_file(file_path)
            play_obj = wave_obj.play()
            play_obj.wait_done()
        else:
            print(f"Audio file {file_path} does not exist.")
    except ImportError:
        print("Please install simpleaudio to enable audio playback.")
    except Exception as e:
        print(f"An error occurred while playing audio: {e}")


def initialize_user_story_agent():
    """
    Initialize the User Story Agent.
    """
    return UserStoryCrew()


if __name__ == "__main__":
    # Initialize the agent
    user_story_crew = initialize_user_story_agent()

    # Pre-recorded question audio files (in .wav format)
    question_audio_files = [
        "audio_questions/question_1.wav",
        "audio_questions/question_2.wav",
        "audio_questions/question_3.wav",
        "audio_questions/question_4.wav",
        "audio_questions/question_5.wav"
    ]

    print("Welcome to the User Story Agent!")
    
    # Ask how many functionalities the user wants to define
    while True:
        try:
            num_functions = int(input("How many functionalities would you like to define (1-3)? ").strip())
            if 1 <= num_functions <= 3:
                break
            else:
                print("Please enter a number between 1 and 3.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

    functionalities = []
    for i in range(num_functions):  
        print(f"\nFunctionality {i + 1}:")
        audio_responses = []
        for idx, question_audio in enumerate(question_audio_files):
            # Play the question audio
            play_audio(question_audio)

            # Assume the user's response is already recorded and saved at a specific path
            response_audio_path = input(f"Enter the path for response {idx + 1} for Functionality {i + 1}: ").strip()
            if not response_audio_path or not Path(response_audio_path).exists():
                print("Invalid path or no response provided. Skipping this functionality.")
                break

            audio_responses.append(response_audio_path)

        # If all 5 responses are recorded, add them to functionalities
        if len(audio_responses) == len(question_audio_files):
            functionalities.append(audio_responses)
        else:
            print(f"Incomplete responses for Functionality {i + 1}. Skipping this functionality.")
            continue
    
    if not functionalities:
        print("No valid functionalities defined. Exiting.")
        sys.exit(1)

    print("Functionalities Completed:", functionalities)

    # Pass audio paths to the crew
    print("\nProcessing user stories...")
    try:
        response = user_story_crew.crew().kickoff(inputs={"audio_responses": functionalities})
        print("\nGenerated User Stories:")
        print(response)
    except Exception as e:
        print(f"An error occurred: {str(e)}")
