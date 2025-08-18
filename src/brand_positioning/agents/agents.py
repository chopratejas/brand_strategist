from crewai import Agent
from langchain_openai import ChatOpenAI
from brand_positioning.tools.tools import CompetitorResearchTool, CustomerInsightTool, MarketTrendTool
from brand_positioning.config import Config

def _get_llm():
    """Get LLM instance with current API key"""
    return ChatOpenAI(
        model=Config.OPENAI_MODEL,
        api_key=Config.OPENAI_API_KEY,
        temperature=0.1
    )

def _get_tools():
    """Get tool instances"""
    return {
        'competitor': CompetitorResearchTool(),
        'customer': CustomerInsightTool(),
        'trend': MarketTrendTool()
    }

def create_market_intelligence_agent():
    """Create agent for competitive and market intelligence gathering"""
    llm = _get_llm()
    tools = _get_tools()
    return Agent(
        role="Market Intelligence Specialist",
        goal="Discover and analyze competitors, customer insights, and market trends for strategic positioning",
        backstory="""You are an expert market researcher with deep experience across multiple industries. 
        You excel at uncovering competitive landscapes, identifying customer pain points, and spotting 
        market opportunities. Your analysis helps business leaders understand exactly where their brand can 
        win in competitive markets.""",
        tools=[tools['competitor'], tools['customer'], tools['trend']],
        llm=llm,
        verbose=True,
        allow_delegation=False
    )

def create_positioning_strategist_agent():
    """Create agent for brand positioning strategy"""
    llm = _get_llm()
    return Agent(
        role="Brand Positioning Strategist",
        goal="Synthesize market intelligence into specific, defensible brand positioning strategies",
        backstory="""You are a senior brand strategist with deep expertise in market positioning across industries. 
        You specialize in finding precise, underserved niches that brands can dominate. 
        Your positioning recommendations are specific, actionable, and built on solid market evidence. 
        You think like a world-class strategist - focused on clear differentiation and market leadership.""",
        tools=[],  # This agent analyzes, doesn't search
        llm=llm,
        verbose=True,
        allow_delegation=False
    )

def create_strategic_advisor_agent():
    """Create agent for strategic action planning"""
    llm = _get_llm()
    tools = _get_tools()
    return Agent(
        role="Strategic Growth Advisor",
        goal="Generate concrete, prioritized action plans for brand positioning and market capture",
        backstory="""You are a seasoned business advisor who has helped dozens of brands across industries 
        achieve market leadership. You excel at translating positioning strategies into specific, 
        executable tactical moves. Your recommendations are always business-friendly: concrete, 
        prioritized, and designed for various organizational sizes. You understand modern business 
        ecosystems deeply - from partnerships to content marketing to product positioning.""",
        tools=[tools['trend']],  # Can research implementation tactics if needed
        llm=llm,
        verbose=True,
        allow_delegation=False
    )