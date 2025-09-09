from crewai import Agent, Crew, Process, Task,LLM
from crewai.project import CrewBase, agent, crew, task
from pydantic import BaseModel, Field
from typing import List, Dict
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize LLM with environment variables
llm = LLM(
    model=os.getenv("MODEL"), 
    temperature=0.8,
    top_p=0.9,
    frequency_penalty=0.1,
    presence_penalty=0.1,
    stop=["END"],
    seed=42,
    base_url="https://api.openai.com/v1",
    api_key=os.getenv("OPENAI_API_KEY")
)




# Predefined recommendation matrix
RECOMMENDATION_MATRIX = {
    "Individuals": {
        "Homeowners and Renters": ["Renter's Insurance", "Health Insurance", "Personal Liability Insurance", "Umbrella Insurance Policy"],
        "Vehicle Owners": ["Motor Insurance", "Health Insurance"],
        "High Net Worth Individuals": ["Kidnap and Ransom Insurance", "Property Insurance"],
        "Young Professionals": ["Health Insurance", "Life Insurance", "Professional Development Coverage"],
        "Families": ["Health Insurance", "Life Insurance", "Property Insurance"],
        "Seniors": ["Health Insurance", "Life Insurance", "Annuity Plans"]
    },
    "Businesses": {
        "SMEs": ["Commercial Insurance", "Cyber Insurance", "Directors and Officers (D&O) Insurance"],
        "Large Corporations": ["Commercial Insurance", "Environmental Liability Insurance", "D&O Insurance"],
        "Start-ups": ["Cyber Insurance", "Professional Liability Insurance"],
        "Technology Companies": ["Cyber Insurance", "Professional Liability Insurance", "Technology Insurance"],
        "Healthcare Providers": ["Cyber Insurance", "Professional Liability Insurance"],
        "Manufacturers": ["Product Liability Insurance", "Cargo Insurance", "Environmental Liability Insurance"],
        "Retailers": ["Product Liability Insurance", "Cargo Insurance", "Cyber Insurance"],
        "Agricultural Businesses": ["Agricultural Insurance", "Environmental Liability Insurance"],
        "Hospitality and Tourism Businesses": ["Commercial Insurance", "Health Insurance"]
    },
    "Specialized Entities": {
        "Airlines": ["Aviation Insurance", "Hull Insurance"],
        "Shipping and Maritime Companies": ["Marine Insurance", "Hull Insurance", "Cargo Insurance"],
        "Drone Operators": ["Aviation Insurance", "Professional Liability Insurance"],
        "Non-Profit Organizations": ["D&O Insurance", "Employment Practices Liability Insurance"],
        "Government Agencies": ["Environmental Liability Insurance", "Marine Insurance"],
        "Educational Institutions": ["Health Insurance", "D&O Insurance", "Professional Liability Insurance"]
    }
}


class Characteristics(BaseModel):
    """Nested model for customer characteristics"""
    type: str
    interest: str


class RecommendationInput(BaseModel):
    """Input model for customer characteristics"""
    customer_name: str = Field(..., description="Name of the customer")
    age_group: str = Field(..., description="Age group of the customer")
    customer_segment: str = Field(..., description="Customer segment (e.g., Individuals, Businesses, Specialized Entities)")
    characteristics: Characteristics = Field(..., description="Specific characteristics such as profession, assets owned, or needs")


class RecommendationOutput(BaseModel):
    """Output model for personalized recommendations"""
    recommended_products: List[str] = Field(..., description="List of recommended insurance products")
    explanation: str = Field(..., description="Detailed explanations for each recommended product")
    actionable_insights: str = Field(..., description="Insights or next steps for the sales representative")


@CrewBase
class PersonalizedRecommendationCrew:
    """Personalized Recommendation Crew"""
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @agent
    def input_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['input_agent'],
            verbose=True,
            llm=llm 
        )

    @agent
    def recommendation_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['recommendation_agent'],
            verbose=True,
            llm=llm
        )

    @task
    def gather_customer_input_task(self) -> Task:
        return Task(
            config=self.tasks_config['gather_customer_input_task'],
            agent=self.input_agent(),
            output_json=RecommendationInput,
        )

    @task
    def generate_recommendations_task(self) -> Task:
        def generate_recommendations(context):
            # Extract input from gather_customer_input_task
            customer_input_data = context.get("gather_customer_input_task_output", {})
            try:
                customer_input = RecommendationInput(**customer_input_data)
            except Exception as e:
                return RecommendationOutput(
                    recommended_products=[],
                    explanation=f"Error: {str(e)}",
                    actionable_insights="Failed to process customer input due to validation error."
                )

            # Match segment and characteristics to recommendations
            segment = customer_input.customer_segment
            characteristics = customer_input.characteristics
            recommended_products = RECOMMENDATION_MATRIX.get(segment, {}).get(characteristics.type, [])

            # Generate detailed explanations
            explanation_details = []
            for product in recommended_products:
                if product == "Renter's Insurance":
                    explanation_details.append(
                        f"**Renter's Insurance**:\n"
                        f"- **Why It’s Essential:** Protects personal property from theft or damage, a common concern in rental units.\n"
                        f"- **Scenario:** Covers damages like water leaks harming personal electronics, preventing financial burden.\n"
                    )
                elif product == "Health Insurance":
                    explanation_details.append(
                        f"**Health Insurance**:\n"
                        f"- **Why It’s Essential:** Provides comprehensive coverage for preventive care and chronic conditions.\n"
                        f"- **Scenario:** Supports active lifestyles with benefits like gym memberships or mental health counseling.\n"
                    )
                elif product == "Personal Liability Insurance":
                    explanation_details.append(
                        f"**Personal Liability Insurance**:\n"
                        f"- **Why It’s Essential:** Covers unexpected incidents like guest injuries on your property.\n"
                        f"- **Scenario:** Protects against legal fees if a visiting friend is injured in your apartment.\n"
                    )
                elif product == "Umbrella Insurance Policy":
                    explanation_details.append(
                        f"**Umbrella Insurance Policy**:\n"
                        f"- **Why It’s Essential:** Extends coverage limits, protecting future acquisitions like cars or property.\n"
                        f"- **Scenario:** Ensures protection against large liability claims, providing long-term peace of mind.\n"
                    )

            # Generate actionable insights
            actionable_insights = (
                f"- **Key Selling Points:**\n"
                f"  - Emphasize comprehensive protection and cost efficiency through bundling options.\n"
                f"  - Highlight long-term savings by mitigating risks early.\n"
                f"- **Cross-Selling Opportunities:**\n"
                f"  - Pair Health Insurance with wellness programs.\n"
                f"  - Bundle Renter’s Insurance and Personal Liability Insurance for holistic coverage.\n"
            )

            return RecommendationOutput(
                recommended_products=recommended_products,
                explanation="\n".join(explanation_details),
                actionable_insights=actionable_insights,
            )

        return Task(
            config=self.tasks_config['generate_recommendations_task'],
            agent=self.recommendation_agent(),
            context=[self.gather_customer_input_task()],
            output_function=generate_recommendations,
            async_execution=True
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
