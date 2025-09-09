from crew import PersonalizedRecommendationCrew


def ask_questions():
    # Step 1: Basic Details
    name = input("What is your name? ")
    age_group = input("Which age group do you belong to (e.g., 20-30, 30-40)? ")
    segment = input("Are you an Individual, a Business, or a Specialized Entity? ")

    # Step 2: Specific Questions Based on Segment
    characteristics = {}
    if segment.lower() == "individual":
        type_of_customer = input("Are you a Homeowner, Renter, Vehicle Owner, or Other? ")
        interest = input("What type of insurance are you looking for (e.g., Property, Life, Health)? ")
        characteristics = {"type": type_of_customer, "interest": interest}

    elif segment.lower() == "business":
        industry = input("What industry is your business in (e.g., Technology, Manufacturing)? ")
        risk_concern = input("What is the primary risk your business wants to mitigate (e.g., cyber threats, liability)? ")
        characteristics = {"industry": industry, "risk_concern": risk_concern}

    elif segment.lower() == "specialized entity":
        type_of_entity = input(
            "What type of specialized entity are you? (e.g., Airlines, Non-Profit Organization, Educational Institution)? "
        )
        specific_needs = input(
            "What is the primary insurance need for your entity (e.g., Aviation Insurance, Liability, Health)? "
        )
        characteristics = {"type_of_entity": type_of_entity, "specific_needs": specific_needs}

    # Create structured input
    inputs = {
        "customer_name": name,
        "age_group": age_group,
        "customer_segment": segment,
        "characteristics": characteristics,
    }
    return inputs


def run():
    # Collect user responses interactively
    user_inputs = ask_questions()

    # Initialize the recommendation system
    recommendation_crew = PersonalizedRecommendationCrew().crew()

    # Generate recommendations
    output = recommendation_crew.kickoff(inputs=user_inputs)

    # Ensure the output is of the correct type
    try:
        print(output)
    except Exception as e:
        print(f"Error in processing the output: {str(e)}")


if __name__ == "__main__":
    run()
