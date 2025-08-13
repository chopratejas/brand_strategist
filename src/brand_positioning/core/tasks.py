from crewai import Task

def create_positioning_strategy_task(brand_info: dict, intelligence_data=None):
    """Create task for brand positioning strategy development"""
    brand_name = brand_info.get("brand", "")
    product = brand_info.get("product", "")
    target = brand_info.get("target", "")
    
    # Add intelligence context if provided
    intelligence_context = ""
    if intelligence_data:
        intelligence_context = f"""
        
        MARKET INTELLIGENCE FINDINGS:
        
        Competitor Analysis:
        {intelligence_data.get('competitor_analysis', 'No competitor data available')}
        
        Customer Insights:
        {intelligence_data.get('customer_insights', 'No customer data available')}
        
        Market Trends:
        {intelligence_data.get('market_trends', 'No trend data available')}
        """
    
    return Task(
        description=f"""
        You are an expert brand strategist who has helped dozens of startups find winning market positions. 
        Analyze the market intelligence and create a HIGHLY SPECIFIC, ACTIONABLE positioning strategy for {brand_name}.
        
        Brand Information:
        - Brand: {brand_name}
        - Product: {product}
        - Target Audience: {target}
        {intelligence_context}
        
        CRITICAL REQUIREMENTS - Your output must be:
        1. SPECIFIC (not generic advice)
        2. EVIDENCE-BASED (cite specific findings from intelligence)
        3. IMMEDIATELY ACTIONABLE (founders can implement today)
        4. DIFFERENTIATED (clear competitive advantage)
        
        DELIVER THE FOLLOWING ANALYSIS:
        
        1. ULTRA-SPECIFIC NICHE IDENTIFICATION:
        - Find the EXACT micro-segment this brand should own (be hyper-specific)
        - Provide market size data with sources
        - Explain WHY this niche is winnable vs competitors found in research
        - Identify the specific customer trigger that makes them buy
        
        2. BATTLE-TESTED POSITIONING STATEMENT:
        - Write the exact 1-sentence positioning statement to use everywhere
        - Create 3 different headline variations for A/B testing
        - Provide the "elevator pitch" version (30 seconds)
        - Give the "website hero section" version with specific copy
        
        3. COMPETITIVE MESSAGING FRAMEWORK:
        - Analyze competitors' exact messaging (quote their websites/ads)
        - Identify the specific messaging gaps your research found
        - Create 5 key messages that differentiate from competitors
        - Provide "comparison table" positioning vs top 3 competitors
        
        4. CUSTOMER PSYCHOLOGY DEEP-DIVE:
        - Map the exact customer journey from problem awareness to purchase
        - Identify the specific emotional triggers that drive buying decisions
        - Quote actual customer language from your research findings
        - Create messaging for each stage of the buyer journey
        
        5. PROOF POINT STRATEGY:
        - Identify what specific credentials/proof points this brand needs
        - Recommend exact testimonial collection strategy
        - Suggest specific partnerships/associations to pursue
        - Define measurable claims the brand can make
        
        6. MESSAGING ARCHITECTURE:
        - Primary message (the main thing people should remember)
        - Secondary messages (supporting proof points)
        - Objection handling messages (address top 3 customer concerns)
        - Call-to-action messaging (exact words to drive conversion)
        
        Use insights from your market intelligence to make every recommendation specific and defensible.
        Think like a world-class brand strategist who has positioned global brands for market domination.
        """,
        expected_output="""
        ULTRA-SPECIFIC POSITIONING STRATEGY REPORT:
        
        ## 1. EXACT NICHE DOMINATION STRATEGY
        **Recommended Micro-Niche:** [Hyper-specific segment with exact demographics/psychographics]
        **Market Size:** [Specific numbers with sources from research]
        **Why We Can Win:** [Evidence-based reasoning citing competitor gaps found]
        **Customer Trigger:** [The exact moment/pain point that makes them buy]
        **Defensibility:** [Specific barriers preventing competitor entry]
        
        ## 2. COPY-READY POSITIONING STATEMENTS
        **Master Positioning Statement:** [The one sentence to rule them all]
        
        **A/B Test Headlines:**
        - Headline Version A: [Specific copy]
        - Headline Version B: [Alternative approach]  
        - Headline Version C: [Third variation]
        
        **30-Second Elevator Pitch:** [Exact script with timing]
        **Website Hero Copy:** [Complete headline + subheadline + CTA copy]
        
        ## 3. COMPETITIVE MESSAGING WARFARE
        **Competitor Message Analysis:**
        - [Competitor 1]: "[Exact quote from their messaging]" → Gap: [Specific opportunity]
        - [Competitor 2]: "[Exact quote from their messaging]" → Gap: [Specific opportunity]
        - [Competitor 3]: "[Exact quote from their messaging]" → Gap: [Specific opportunity]
        
        **Our Differentiating Messages:**
        1. [Specific message that competitors can't claim]
        2. [Unique angle based on research findings]
        3. [Customer language they use but competitors don't]
        4. [Benefit only we can deliver credibly]
        5. [Emotional trigger competitors miss]
        
        **Competitive Comparison Table:**
        | Feature/Benefit | Us | Competitor A | Competitor B | Competitor C |
        |[Specific comparison with our advantage highlighted]
        
        ## 4. CUSTOMER PSYCHOLOGY PLAYBOOK
        **Journey Stage 1 - Problem Unaware:** [Exact messaging + channels]
        **Journey Stage 2 - Problem Aware:** [Specific pain point messaging]
        **Journey Stage 3 - Solution Searching:** [Differentiation messaging]
        **Journey Stage 4 - Vendor Evaluation:** [Proof point messaging]
        **Journey Stage 5 - Purchase Decision:** [Urgency/scarcity messaging]
        
        **Emotional Triggers:**
        - Primary: [Main emotional driver with evidence]
        - Secondary: [Supporting emotional appeal]
        - Tertiary: [Additional psychological motivator]
        
        **Customer Voice Quotes:** [Actual language from research to use in copy]
        
        ## 5. CREDIBILITY BUILDING ROADMAP
        **Required Proof Points:**
        - [Specific credential/achievement needed]
        - [Particular testimonial format to collect]
        - [Exact metric/statistic to establish]
        
        **Partnership Strategy:** [3 specific organizations to partner with]
        **Content Authority Plan:** [Topics to become known for]
        **Social Proof Collection:** [Exact testimonial collection system]
        
        ## 6. MESSAGING ARCHITECTURE SYSTEM
        **Primary Message:** [The one thing people remember]
        **Supporting Messages:** [3 key proof points]
        **Objection Handlers:** [Responses to top 3 concerns]
        **Conversion CTAs:** [Exact call-to-action copy for each channel]
        
        **Channel-Specific Messaging:**
        - Website: [Exact copy]
        - Social Media: [Platform-specific messaging]
        - Email: [Subject lines + body copy approaches]
        - Sales Calls: [Key talking points]
        - PR/Media: [Soundbites and angles]
        
        Every recommendation includes specific implementation steps and is immediately actionable.
        """
    )

def create_strategic_action_task(brand_info: dict, positioning_data=None):
    """Create task for strategic action planning"""
    brand_name = brand_info.get("brand", "")
    
    # Add positioning context if provided
    positioning_context = ""
    if positioning_data:
        positioning_context = f"""
        
        POSITIONING STRATEGY:
        {positioning_data}
        """
    
    return Task(
        description=f"""
        Based on the positioning strategy, create a prioritized action plan of strategic moves for {brand_name}.
        {positioning_context}
        
        Develop 3-5 specific tactical recommendations that will help {brand_name}:
        - Establish leadership in their chosen niche
        - Build brand awareness and credibility
        - Drive customer acquisition and growth
        - Strengthen competitive positioning
        
        For each strategic move, provide:
        
        1. SPECIFIC ACTION DESCRIPTION:
        - What exactly needs to be done
        - Why this move is strategically important
        - How it supports the positioning strategy
        
        2. IMPLEMENTATION ROADMAP:
        - Step-by-step execution plan
        - Timeline and milestones
        - Resource requirements
        
        3. SUCCESS METRICS:
        - How to measure success
        - Expected outcomes and ROI
        - Key performance indicators
        
        4. PRIORITY RANKING:
        - High/Medium/Low priority
        - Rationale for prioritization
        - Dependencies and prerequisites
        
        Focus on moves that are:
        - Executable by the existing team structure
        - Cost-effective and high-impact
        - Aligned with the positioning strategy
        - Defensible and sustainable
        
        Think like an experienced business strategist - recommend tactics that deliver measurable results.
        """,
        expected_output="""
        A prioritized strategic action plan containing:
        
        1. Strategic Move #1 (Highest Priority):
        - Specific action description and rationale
        - Implementation roadmap with timeline
        - Resource requirements and budget estimate
        - Success metrics and expected outcomes
        
        2. Strategic Move #2:
        - Same detailed format as above
        
        3. Strategic Move #3:
        - Same detailed format as above
        
        4. Strategic Move #4 (if applicable):
        - Same detailed format as above
        
        5. Strategic Move #5 (if applicable):
        - Same detailed format as above
        
        6. Implementation Timeline:
        - 30-day quick wins
        - 90-day medium-term objectives
        - 6-month strategic goals
        
        7. Resource Allocation:
        - Budget requirements for each move
        - Team member responsibilities
        - External resource needs
        
        All recommendations must be specific, actionable, and appropriate for the business scale and industry context.
        """
    )