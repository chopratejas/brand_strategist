"""
Focused agents for specific niche positioning and strategic moves.
Streamlined for founders who need clear, actionable insights.
"""

from crewai import Agent
from langchain_openai import ChatOpenAI
from brand_positioning.tools.focused_tools import CompetitorGapTool, PositioningOpportunityTool
from brand_positioning.config import Config

def create_positioning_specialist_agent():
    """
    Single focused agent that finds positioning opportunities and strategic moves.
    Designed for founders who need specific, actionable insights.
    """
    return Agent(
        role="Brand Positioning Specialist",
        goal="Find the exact niche a brand should dominate and the one strategic move to get there",
        backstory="""You are the world's most research-driven positioning expert. You HATE assumptions and generic advice.
        
        Your method: ALWAYS research the actual brand first, then find MORE specific positioning than they currently claim.
        
        Your rules:
        - FIRST: Research what the brand actually does today (use tools to find their current website/positioning)
        - SECOND: Find their real competitors (not assumed ones)
        - THIRD: Identify specific customer pain points they face (from actual reviews/complaints)
        - FOURTH: Create positioning that's MORE specific than what they currently claim
        - FIFTH: Strategic moves must leverage their ACTUAL capabilities and resources
        
        You NEVER suggest generic moves like "Launch X Quiz" or "Create Y Series" without specific research justification.
        You NEVER assume a brand's current positioning - you research it first.
        You NEVER copy templated examples - you create unique strategies based on research.
        
        Be forensically specific. Every recommendation must trace back to actual research findings.""",
        verbose=True,
        allow_delegation=False,
        llm=ChatOpenAI(
            model=Config.OPENAI_MODEL,
            api_key=Config.OPENAI_API_KEY,
            temperature=0.1
        ),
        tools=[
            CompetitorGapTool(),
            PositioningOpportunityTool()
        ]
    )