#!/usr/bin/env python
from crew import CustomerSentimentCrew
import time

def run():
   
    # Input parameters
    inputs = {
        'company_name': 'jubileelife',
        'company_variations': ['Life Insurance Corporation of India', 'Jubilee Life Insurance Company Limite'],
        'geographical_location': 'Asia',
    }

    print("Starting Customer Sentiment Analysis...")
     # Start tracking time
    start_time = time.time()
    sentiment_crew = CustomerSentimentCrew().crew()

    # Perform the analysis
    output = sentiment_crew.kickoff(inputs=inputs)
    
    # Calculate execution time
    end_time = time.time()
    execution_time = end_time - start_time
    
    print("\nExecution Time: {:.2f} seconds".format(execution_time))
    print("\nCustomer Sentiment Analysis Output:")
    print(output)

if __name__ == "__main__":
    run()
