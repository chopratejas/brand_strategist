"""
Focused workflow for niche positioning and strategic moves.
Uses minimal API calls and delivers exactly what founders need.
"""

from crewai import Crew
from brand_positioning.agents.focused_agents import create_positioning_specialist_agent
from brand_positioning.core.focused_tasks import create_niche_positioning_task, create_strategic_move_task
from brand_positioning.config import Config
import logging
import re

logger = logging.getLogger(__name__)

def clean_result_content(raw_content):
    """Clean up raw LLM output by removing internal reasoning and formatting"""
    if not raw_content:
        return raw_content
    
    # Remove "Thought:" sections and other internal reasoning
    content = str(raw_content)
    
    # Remove patterns like "Thought: ..." or "```\nThought: ..."
    content = re.sub(r'```\s*Thought:.*?```\s*', '', content, flags=re.DOTALL)
    content = re.sub(r'Thought:.*?\n\n', '', content, flags=re.DOTALL)
    content = re.sub(r'^```.*?```\s*', '', content, flags=re.DOTALL | re.MULTILINE)
    
    # Clean up multiple newlines
    content = re.sub(r'\n{3,}', '\n\n', content)
    
    return content.strip()

def run_focused_positioning_analysis(brand_info: dict, status_callback=None):
    """
    Run focused brand positioning analysis with minimal API usage.
    Returns: {niche_positioning, strategic_move, success}
    """
    try:
        if status_callback:
            status_callback("Creating positioning specialist agent...", 10)
        
        # Single focused agent
        positioning_agent = create_positioning_specialist_agent()
        
        if status_callback:
            status_callback("Finding your specific niche to dominate...", 30)
        
        # Task 1: Find specific niche positioning  
        positioning_task = create_niche_positioning_task(brand_info, positioning_agent)
        
        # Run positioning analysis
        positioning_crew = Crew(
            agents=[positioning_agent],
            tasks=[positioning_task],
            verbose=True
        )
        
        positioning_result = positioning_crew.kickoff()
        
        if status_callback:
            status_callback("Identifying your smart strategic move...", 70)
        
        # Task 2: Find strategic move based on positioning
        strategic_task = create_strategic_move_task(brand_info, positioning_agent, positioning_result.raw)
        
        # Run strategic move analysis
        strategic_crew = Crew(
            agents=[positioning_agent],
            tasks=[strategic_task], 
            verbose=True
        )
        
        strategic_result = strategic_crew.kickoff()
        
        if status_callback:
            status_callback("Analysis complete!", 100)
        
        return {
            "success": True,
            "brand_info": brand_info,
            "niche_positioning": clean_result_content(positioning_result.raw),
            "strategic_move": clean_result_content(strategic_result.raw),
            "api_calls_used": 4,  # Only 4 SerpAPI calls total
            "cost_estimate": "$0.20"  # Much lower cost
        }
        
    except Exception as e:
        logger.error(f"Focused positioning analysis failed: {str(e)}")
        if status_callback:
            status_callback(f"Analysis failed: {str(e)}", 100)
        
        return {
            "success": False,
            "error": str(e),
            "brand_info": brand_info
        }