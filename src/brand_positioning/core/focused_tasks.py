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
        
        STEP 1: Use the Competitor Gap Research tool with brand JSON: {{"brand": "{brand_name}", "product": "{product}"}}
        STEP 2: Use the Positioning Opportunity Finder tool with the same brand JSON
        
        CRITICAL: Research the ACTUAL brand first. What do they currently claim? Who are their real competitors?
        Your job: Find a MORE SPECIFIC sub-category than what they currently claim.
        
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
        BRAND-SPECIFIC NICHE POSITIONING:
        
        **Current Positioning Research:** [What does this brand currently claim based on your research?]
        
        **Direct Competitors Found:** [List 2-3 actual competitors you discovered]
        
        **Your Exact Niche:** [demographic + use case in 3-6 words, MORE specific than current positioning]
        
        **Customer Language:** "[Exact words from research - quote actual customer reviews/complaints]"
        
        **Why This Brand Wins:** [Specific advantage based on their current product/capabilities]
        
        **Positioning Gap:** [What specific gap in competitor positioning does this fill?]
        
        MUST be based on ACTUAL research, not assumptions.
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
        Based on {brand_name}'s CURRENT capabilities and positioning research, identify ONE strategic move.
        {context}
        
        CRITICAL: Don't use templated examples. Base this on:
        1. What this specific brand actually does today
        2. What customer pain points you found in research
        3. What competitors are NOT doing
        4. What this brand could realistically execute
        
        AVOID these templated patterns:
        - Generic "Launch X Quiz" suggestions
        - "Create Y video series" without brand relevance  
        - "Partner with Z podcasts" without specific rationale
        
        ULTRA-SPECIFIC REQUIREMENTS:
        1. Must include EXACT tactic name (like "Perimenopause Collagen Quiz")
        2. Must include EXACT numbers (5 podcasts, 20 interviews, 30-day challenge)
        3. Must be executable in 30-60 days with existing team
        4. Must directly capture your exact niche audience
        
        BANNED MOVES: "create content", "build community", "social media strategy", "email marketing"
        
        If you write anything generic like "create content around X" - RESTART. Be obsessively specific.
        """,
        expected_output="""
        BRAND-SPECIFIC STRATEGIC MOVE:
        
        **Research Foundation:** [What you learned about this brand's current state and customer problems]
        
        **Your Move:** [Exact tactic name based on brand's actual capabilities and customer research]
        
        **Why This Brand Can Execute:** [Specific reason this aligns with their current resources/positioning]
        
        **30-Day Execution:**
        - Week 1: [Specific task based on brand's actual situation]
        - Week 2: [Specific task based on research findings] 
        - Week 3: [Specific task leveraging brand's strengths]
        - Week 4: [Specific task targeting discovered customer pain]
        
        **Competitive Advantage:** [How this exploits a gap you found in competitor research]
        
        MUST be based on ACTUAL brand research, not generic templates.
        """,
        agent=agent,
        async_execution=False
    )