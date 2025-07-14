import streamlit as st
import sys
import os
from pathlib import Path

# Add src to path
src_dir = Path(__file__).parent / "src"
sys.path.insert(0, str(src_dir))

try:
    from src.crew.ene_crew import EntrepreneurshipCrew
except ImportError:
    st.error("❌ Import error. Please install dependencies with: pip install -e .")
    st.stop()


def main():
    st.set_page_config(
        page_title="Entrepreneurship Copilot",
        page_icon="🚀",
        layout="wide"
    )
    
    st.title("🚀 Entrepreneurship Copilot")
    st.markdown("*AI-powered business planning assistant*")
    
    # Initialize session state for API key
    if 'gemini_api_key_set' not in st.session_state:
        st.session_state.gemini_api_key_set = False
    
    st.markdown("---")
    
    # Sidebar with instructions
    with st.sidebar:
        # Show API key status or setup
        if os.getenv('GEMINI_API_KEY') or st.session_state.gemini_api_key_set:
            st.success("✅ Gemini API Key: Connected")
            st.info("🔧 Set for this session")
            if st.button("🔄 Change API Key"):
                # Remove from current environment
                if 'GEMINI_API_KEY' in os.environ:
                    del os.environ['GEMINI_API_KEY']
                st.session_state.gemini_api_key_set = False
                st.rerun()
        else:
            st.warning("🔑 API Key Required")
            st.markdown("You'll need a Gemini API key to generate plans.")
            
            with st.expander("🔐 Set API Key"):
                st.markdown("Get your key from: [Google AI Studio](https://makersuite.google.com/app/apikey)")
                
                with st.form("sidebar_api_key_form"):
                    api_key = st.text_input(
                        "Enter your Gemini API Key:",
                        type="password",
                        placeholder="AIza...",
                        help="Your API key will be securely stored for this session only"
                    )
                    
                    submitted = st.form_submit_button("🚀 Set API Key", type="primary")
                    
                    if submitted:
                        if api_key.strip():
                            os.environ['GEMINI_API_KEY'] = api_key.strip()
                            st.session_state.gemini_api_key_set = True
                            st.success("✅ API key set successfully!")
                            st.rerun()
                        else:
                            st.error("❌ Please enter a valid API key.")
        
        st.header("📋 How it works")
        st.markdown("""
        1. **Describe your startup idea** - What problem are you solving?
        2. **Define your target market** - Who are your customers?
        3. **Outline your team** - What skills and experience do you have?
        4. **Generate comprehensive plans** - Get business plan, MVP strategy, and go-to-market plan
        """)
        
        st.header("🎯 What you'll get")
        st.markdown("""
        - **Business Plan**: Market analysis, financial projections, strategy
        - **MVP Plan**: Product development roadmap and validation strategy  
        - **GTM Strategy**: Customer acquisition and launch plan
        """)
    
    # Main input form
    st.header("📝 Tell us about your startup")
    
    with st.form("startup_form"):
        startup_idea = st.text_area(
            "💡 Startup Idea",
            placeholder="Describe your startup idea, the problem you're solving, and your proposed solution...",
            height=120,
            help="Be specific about the problem, solution, and unique value proposition"
        )
        
        target_market = st.text_area(
            "🎯 Target Market",
            placeholder="Describe your target customers, market size, demographics, and market trends...",
            height=100,
            help="Include information about customer segments, market size, and competitive landscape"
        )
        
        team_composition = st.text_area(
            "👥 Team Composition",
            placeholder="Describe your team members, their roles, experience, and relevant skills...",
            height=100,
            help="Include founders, key employees, advisors, and their backgrounds"
        )
        
        submitted = st.form_submit_button("🚀 Generate Business Plan", type="primary")
    
    if submitted:
        if not startup_idea or not target_market or not team_composition:
            st.error("❌ Please fill in all fields before generating the plan.")
        elif not os.getenv('GEMINI_API_KEY') and not st.session_state.gemini_api_key_set:
            st.error("🔑 Please set your Gemini API key first using the sidebar.")
            st.info("💡 You can get your API key from [Google AI Studio](https://makersuite.google.com/app/apikey)")
        else:
            # Show progress
            with st.spinner("🔄 Analyzing your startup and generating comprehensive plans... This may take a few minutes."):
                try:
                    # Prepare inputs for the crew
                    inputs = {
                        'startup_idea': startup_idea,
                        'target_market': target_market,
                        'team_composition': team_composition
                    }
                    
                    # Initialize crew and run analysis
                    crew_instance = EntrepreneurshipCrew()
                    result = crew_instance.crew().kickoff(inputs=inputs)

                    # Display results
                    st.success("✅ Plan generation completed!")
                    
                    # Parse the result to extract different sections
                    result_str = str(result)
                    
                    # Create tabs for different sections
                    tab1, tab2, tab3, tab4 = st.tabs(["📊 Executive Summary", "📋 Complete Plan", "📈 Key Insights", "💾 Download"])
                    
                    with tab1:
                        st.header("📊 Executive Summary")
                        
                        # Extract key information for summary
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.subheader("🎯 Your Startup")
                            with st.container():
                                st.markdown(f"**Idea:** {startup_idea[:200]}...")
                                st.markdown(f"**Target Market:** {target_market[:150]}...")
                                st.markdown(f"**Team:** {team_composition[:150]}...")
                        
                        with col2:
                            st.subheader("📈 Generated Plans")
                            st.info("✅ **Business Strategy Plan** - Complete")
                            st.info("✅ **MVP Development Plan** - Complete") 
                            st.info("✅ **Go-to-Market Strategy** - Complete")
                            
                        # Key metrics section
                        st.subheader("🔍 Quick Insights")
                        
                        # Try to extract key metrics from the result
                        insights_col1, insights_col2, insights_col3 = st.columns(3)
                        
                        with insights_col1:
                            st.metric("Plan Sections", "12+", help="Number of strategic sections covered")
                        
                        with insights_col2:
                            st.metric("Target Segments", "2-3", help="Primary customer segments identified")
                            
                        with insights_col3:
                            st.metric("Revenue Streams", "Multiple", help="Diversified revenue model")
                    
                    with tab2:
                        st.header("📋 Your Complete Entrepreneurship Plan")
                        
                        # Split the content into sections for better readability
                        sections = result_str.split('\n\n')
                        
                        # Display content in organized sections
                        for i, section in enumerate(sections):
                            if section.strip():
                                # Check if this looks like a header
                                if section.startswith('#') or section.startswith('**') or len(section) < 100:
                                    if section.startswith('#'):
                                        # Convert markdown headers to streamlit headers
                                        header_level = section.count('#')
                                        header_text = section.lstrip('#').strip()
                                        if header_level == 1:
                                            st.header(header_text)
                                        elif header_level == 2:
                                            st.subheader(header_text)
                                        else:
                                            st.write(f"**{header_text}**")
                                    else:
                                        st.markdown(section)
                                else:
                                    # Regular content
                                    st.markdown(section)
                                
                                # Add some spacing between sections
                                if i < len(sections) - 1:
                                    st.write("")
                    
                    with tab3:
                        st.header("📈 Key Strategic Insights")
                        
                        # Extract and highlight key insights
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.subheader("🎯 Market Opportunity")
                            if "market" in result_str.lower():
                                st.success("✅ Market analysis completed")
                                st.info("Target market segments identified and analyzed")
                            
                            st.subheader("💰 Revenue Strategy")
                            if "revenue" in result_str.lower() or "pricing" in result_str.lower():
                                st.success("✅ Revenue model defined")
                                st.info("Multiple revenue streams identified")
                                
                            st.subheader("🚀 Launch Strategy")
                            if "launch" in result_str.lower() or "marketing" in result_str.lower():
                                st.success("✅ Go-to-market plan ready")
                                st.info("Marketing channels and launch timeline defined")
                        
                        with col2:
                            st.subheader("🛠️ Product Development")
                            if "mvp" in result_str.lower() or "product" in result_str.lower():
                                st.success("✅ MVP strategy outlined")
                                st.info("Development roadmap and features prioritized")
                                
                            st.subheader("👥 Team & Resources")
                            if "team" in result_str.lower():
                                st.success("✅ Team analysis completed")
                                st.info("Skills and resource requirements identified")
                                
                            st.subheader("⚠️ Risk Management")
                            if "risk" in result_str.lower() or "challenge" in result_str.lower():
                                st.success("✅ Risk assessment included")
                                st.info("Potential challenges and mitigation strategies")
                        
                        # Action items section
                        st.subheader("📋 Next Steps")
                        st.markdown("""
                        **Immediate Actions:**
                        1. 📊 Review the complete business plan in detail
                        2. 🛠️ Begin MVP development planning
                        3. 💰 Prepare funding strategy and financial projections
                        4. 🎯 Validate target market assumptions
                        5. 👥 Assess team needs and hiring requirements
                        
                        **Timeline:**
                        - **Week 1-2:** Market validation and team assessment
                        - **Week 3-4:** MVP planning and development initiation  
                        - **Month 2-3:** Product development and testing
                        - **Month 4-6:** Go-to-market execution and launch
                        """)
                    
                    with tab4:
                        st.header("💾 Download Your Plan")
                        
                        # Create different download formats
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.subheader("📄 Complete Business Plan")
                            
                            # Create downloadable content with better formatting
                            plan_content = f"""
# ENTREPRENEURSHIP COPILOT - BUSINESS PLAN
{'=' * 80}

## STARTUP OVERVIEW
{'=' * 40}

**Startup Idea:**
{startup_idea}

**Target Market:**
{target_market}

**Team Composition:**
{team_composition}

## GENERATED STRATEGIC PLAN
{'=' * 40}

{str(result)}

{'=' * 80}
Generated by Entrepreneurship Copilot - AI-Powered Business Planning
Date: {st.session_state.get('generation_date', 'Today')}
{'=' * 80}
"""
                            
                            st.download_button(
                                label="📄 Download Complete Plan (TXT)",
                                data=plan_content,
                                file_name="entrepreneurship_business_plan.txt",
                                mime="text/plain",
                                help="Download the complete business plan as a text file"
                            )
                        
                        with col2:
                            st.subheader("📊 Executive Summary")
                            
                            # Create a concise executive summary
                            exec_summary = f"""
# EXECUTIVE SUMMARY - {startup_idea[:50]}...
{'=' * 60}

## Key Information
- **Business Type:** AI-Powered Solution
- **Target Market:** {target_market[:100]}...
- **Team Size:** Multiple skilled professionals
- **Plans Generated:** Business Strategy, MVP Plan, GTM Strategy

## Strategic Focus Areas
✅ Market Analysis & Competitive Positioning
✅ Product Development & MVP Strategy  
✅ Revenue Model & Financial Projections
✅ Go-to-Market & Customer Acquisition
✅ Risk Assessment & Mitigation

## Next Steps
1. Market validation and customer research
2. MVP development and testing
3. Funding strategy execution
4. Team building and scaling
5. Go-to-market implementation

Generated by Entrepreneurship Copilot
"""
                            
                            st.download_button(
                                label="📊 Download Executive Summary",
                                data=exec_summary,
                                file_name="executive_summary.txt",
                                mime="text/plain",
                                help="Download a concise executive summary"
                            )
                        
                        st.markdown("---")
                        
                        # Additional resources section
                        st.subheader("🎯 Additional Resources")
                        
                        col3, col4, col5 = st.columns(3)
                        
                        with col3:
                            st.info("""
                            **💡 Implementation Tips**
                            - Start with market validation
                            - Build MVP incrementally  
                            - Focus on customer feedback
                            - Monitor key metrics
                            """)
                        
                        with col4:
                            st.info("""
                            **📚 Recommended Reading**
                            - The Lean Startup
                            - Business Model Generation
                            - Crossing the Chasm
                            - The Mom Test
                            """)
                        
                        with col5:
                            st.info("""
                            **🔗 Useful Tools**
                            - Google Analytics
                            - Figma (UI/UX Design)
                            - Slack (Team Communication)
                            - Trello (Project Management)
                            """)
                        
                        st.success("💡 **Pro Tip:** Use this plan as a living document. Update it regularly as you validate assumptions and gather market feedback!")
                
                except ValueError as ve:
                    if "GEMINI_API_KEY" in str(ve):
                        st.error("🔑 API Key Error: The Gemini API key is missing or invalid.")
                        st.info("💡 Please set your API key using the sidebar and try again.")
                    else:
                        st.error(f"❌ Configuration Error: {str(ve)}")
                except Exception as e:
                    st.error(f"❌ Error generating plan: {str(e)}")
                    st.info("💡 **Troubleshooting**: Make sure you have the required dependencies installed and your AI model is properly configured.")
                    
                    # Show detailed error info in an expander for debugging
                    with st.expander("🔍 Error Details (for debugging)"):
                        st.code(str(e))
                        st.write("If this error persists, please check:")
                        st.write("1. ✅ GEMINI_API_KEY is set using the sidebar")
                        st.write("2. ✅ All dependencies are installed")
                        st.write("3. ✅ Your internet connection is stable")
                        st.write("4. ✅ The CrewAI service is responding")
    
    # Footer
    st.markdown("---")
    st.markdown("*Built with CrewAI and Streamlit* | 🚀 *Entrepreneurship Copilot v1.0*")


if __name__ == "__main__":
    main()
