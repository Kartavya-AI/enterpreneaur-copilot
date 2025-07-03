# Entrepreneurship Copilot

An AI-powered business planning assistant that helps entrepreneurs create comprehensive business plans, MVP strategies, and go-to-market plans.

## Features

- **Business Plan Generation**: Comprehensive market analysis, financial projections, and strategic recommendations
- **MVP Strategy**: Lean product development roadmap with validation methods
- **Go-to-Market Planning**: Customer acquisition strategies and launch plans
- **Interactive UI**: Easy-to-use Streamlit interface
- **AI-Powered**: Uses CrewAI with specialized agents for different aspects of business planning

## Setup

1. **Install Python 3.13+**

2. **Install dependencies**:
   ```bash
   pip install -e .
   ```

3. **Set up environment** (optional - for OpenAI):
   Create a `.env` file:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

## Usage

### Option 1: Streamlit UI (Recommended)
```bash
streamlit run ui.py
```

### Option 2: Command Line
```bash
python src/crew/main.py
```

### Option 3: Python Script
```python
from crew.ene_crew import EntrepreneurshipCrew

crew = EntrepreneurshipCrew()
results = crew.run(
    startup_idea="Your startup idea...",
    target_market="Your target market...",
    team_composition="Your team details..."
)
print(results['business_plan'])
```

## What You'll Get

The system generates three comprehensive documents:

1. **Business Plan** (2000-3000 words):
   - Executive Summary
   - Market Analysis
   - Business Model
   - SWOT Analysis
   - Financial Projections
   - Risk Assessment
   - Implementation Timeline

2. **MVP Plan** (1500-2000 words):
   - Core Problem & Customer Persona
   - Key Assumptions to Validate
   - Essential Features
   - Success Metrics
   - Development Timeline
   - Testing Strategy

3. **Go-to-Market Strategy** (2000-2500 words):
   - Customer Segmentation
   - Value Proposition
   - Pricing Strategy
   - Distribution Channels
   - Marketing Mix
   - Launch Timeline

## Configuration

The system uses three AI agents defined in `src/crew/config/`:

- **Business Strategy Agent**: Creates comprehensive business plans
- **MVP Development Agent**: Designs lean product strategies
- **GTM Strategy Agent**: Develops marketing and launch plans

## Requirements

- Python 3.13+
- CrewAI
- Streamlit
- LangChain Community
- Local LLM (Ollama) or OpenAI API access

## Example

Input:
- **Idea**: AI-powered meal planning app
- **Market**: Health-conscious millennials
- **Team**: CEO, CTO, AI Engineer, Designer, Marketing Manager

Output: Complete business plan with market analysis, MVP roadmap, and launch strategy.

## License

MIT License
