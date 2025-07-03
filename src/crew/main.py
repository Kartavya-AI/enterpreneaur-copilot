import os
from dotenv import load_dotenv
from ene_crew import EntrepreneurshipCrew

def main():
    """Main function for testing the crew."""
    print("🚀 Entrepreneurship Copilot Crew")
    print("=" * 50)
    
    # Create crew instance
    crew_instance = EntrepreneurshipCrew()
    
    # Example inputs
    inputs = {
        'startup_idea': """
        A mobile app that uses AI to help people meal plan based on their dietary preferences, 
        budget constraints, and local grocery store inventory. The app would generate personalized 
        meal plans, shopping lists, and even suggest recipes based on what's on sale.
        """,
        'target_market': """
        Primary: Health-conscious millennials and Gen Z (ages 25-40) with disposable income 
        of $50,000+ who are tech-savvy and interested in convenience and health optimization.
        Secondary: Busy professionals and families looking to save time and money on grocery shopping.
        Market size: ~50 million people in the US.
        """,
        'team_composition': """
        - CEO/Co-founder: Business background, 5 years experience in food tech
        - CTO/Co-founder: Software engineer, 8 years experience in mobile app development
        - AI/ML Engineer: PhD in Computer Science, specializing in recommendation systems
        - UX/UI Designer: 4 years experience in consumer app design
        - Marketing Manager: 6 years experience in digital marketing for consumer apps
        """
    }
    
    try:
        print("Starting crew execution...")
        # Run the crew with inputs
        result = crew_instance.crew().kickoff(inputs=inputs)
        
        print("\n" + "=" * 50)
        print("📋 RESULTS")
        print("=" * 50)
        print(result)
        
    except Exception as e:
        print(f"❌ Error running crew: {str(e)}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())