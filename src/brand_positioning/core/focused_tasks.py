"""
Focused tasks that deliver exactly what founders need:
1. Specific niche to dominate 
2. One smart strategic move
"""

from crewai import Task

def create_niche_positioning_task(brand_info: dict, agent):
    """
    Task to find the specific niche the brand should dominate.
    Output: Clear positioning angle for category leadership.
    """
    brand_name = brand_info.get("brand", "")
    product = brand_info.get("product", "")
    target = brand_info.get("target", "")
    
    return Task(
        description=f"""
        Find the EXACT niche that {brand_name} should dominate for category leadership.
        
        Brand Details:
        - Brand: {brand_name}
        - Product: {product}  
        - Target: {target}
        
        Use the Competitor Gap Research tool to understand current market positioning.
        Use the Positioning Opportunity Finder tool to identify strategic opportunities.
        
        Your job: Find the specific sub-category this brand can own and defend.
        
        Think like these EXACT examples:
        - "collagen powder for perimenopausal women" (not "wellness supplements" or "women's health")
        - "project management for creative agencies" (not "productivity software" or "team collaboration")
        - "meditation for anxious entrepreneurs" (not "mental health apps" or "business wellness")
        
        ULTRA-SPECIFIC REQUIREMENTS:
        1. Must include EXACT demographic + EXACT use case in one phrase
        2. Must be narrow enough that 5-10 competitors max can claim it
        3. Must use customer language (how THEY describe their problem)
        4. Must be defensible (hard for big players to copy)
        
        BANNED WORDS: wellness, health, productivity, business, platform, solution, tool, service
        
        If you write anything broad like "wellness for women" or "productivity for teams" - RESTART.
        """,
        expected_output="""
        ULTRA-SPECIFIC NICHE POSITIONING:
        
        **Your Exact Niche:** [demographic + use case in 3-6 words, like "collagen for perimenopausal women"]
        
        **Customer Language:** "[Exact words your customers use to describe this problem - quote research]"
        
        **Why You Win:** [One specific reason competitors can't easily copy this positioning]
        
        **Your Category Story:** "[Brand] is the only [exact niche] designed specifically for [exact customer pain]"
        
        MUST BE NARROW. If more than 10 competitors could claim this exact positioning, make it more specific.
        """,
        agent=agent,
        async_execution=False
    )

def create_strategic_move_task(brand_info: dict, agent, positioning_context=None):
    """
    Task to identify ONE smart strategic move for positioning advantage.
    Output: Concrete next action the brand should take.
    """
    brand_name = brand_info.get("brand", "")
    
    context = ""
    if positioning_context:
        context = f"\n\nPOSITIONING CONTEXT:\n{positioning_context}\n"
    
    return Task(
        description=f"""
        Based on the positioning strategy, identify ONE smart strategic move for {brand_name}.
        {context}
        
        Think like these EXACT examples:
        - "Launch a 'Perimenopause Collagen Quiz' to capture this specific audience"
        - "Create 'Creative Agency Chaos' video series interviewing 20 agency owners about project disasters"
        - "Partner with 5 entrepreneurship podcasts for 'Anxious Entrepreneur' segment sponsorships"
        
        ULTRA-SPECIFIC REQUIREMENTS:
        1. Must include EXACT tactic name (like "Perimenopause Collagen Quiz")
        2. Must include EXACT numbers (5 podcasts, 20 interviews, 30-day challenge)
        3. Must be executable in 30-60 days with existing team
        4. Must directly capture your exact niche audience
        
        BANNED MOVES: "create content", "build community", "social media strategy", "email marketing"
        
        If you write anything generic like "create content around X" - RESTART. Be obsessively specific.
        """,
        expected_output="""
        ONE SPECIFIC STRATEGIC MOVE:
        
        **Your Move:** [Exact tactic name with specific numbers - like "Launch 'X Quiz' interviewing 20 Y people"]
        
        **30-Day Execution:**
        - Week 1: [Specific task]
        - Week 2: [Specific task] 
        - Week 3: [Specific task]
        - Week 4: [Specific task]
        
        **Why This Owns Your Niche:** [How this makes you the obvious choice in your exact positioning]
        
        MUST include exact tactic name, specific numbers, and week-by-week execution plan.
        """,
        agent=agent,
        async_execution=False
    )