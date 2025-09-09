import sys
from crew import MarketingPostsCrew
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Access environment variables
api_key = os.getenv("OPENAI_API_KEY")
model = os.getenv("MODEL")


def run():
    inputs = {
        'geographical_location': input("Enter Geographical Location (e.g., North America, Asia, etc.): "),
        'project_description': input("Enter Project Description: ")
    }

    
    try:
        crew_instance = MarketingPostsCrew().crew()
        
        if not crew_instance:
            raise ValueError("Failed to initialize the Crew instance.")
        
        result = crew_instance.kickoff(inputs=inputs)
        
        # Print and return the result
        print("Crew Output:", result)
        return result
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        'customer_domain': input("Enter Customer Domain (e.g., https://www.jubileelife.com/): "),
        'project_description': input("Enter Project Description: ")
    }
    
    try:
        n_iterations = int(input("Enter number of training iterations (default: 10): ") or 10)
        
        crew_instance = MarketingPostsCrew().crew()
        result = crew_instance.train(n_iterations=n_iterations, inputs=inputs)
        
        # Print and return the training result
        print("Training Completed:", result)
        return result
    except ValueError as ve:
        print(f"Input Error: {ve}")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred while training the crew: {e}")
        sys.exit(1)

if __name__ == "__main__":
    # Determine the mode (run or train) based on script arguments
    if len(sys.argv) > 1 and sys.argv[1] == 'train':
        train()
    else:
        run()
