from crewai import Task

def create_competitor_analysis_task(brand_info: dict):
    """Create task specifically for competitor analysis"""
    brand_name = brand_info.get("brand", "")
    product = brand_info.get("product", "")
    target = brand_info.get("target", "")
    
    return Task(
        description=f"""
        Conduct comprehensive competitor analysis for {brand_name}.
        
        Brand Information:
        - Brand: {brand_name}
        - Product: {product}
        - Target Audience: {target}
        
        Use the Competitor Research tool to:
        1. Find direct and indirect competitors in the {product} space
        2. Identify their positioning, target audiences, and key differentiators
        3. Analyze their messaging, pricing strategies, and market approach
        4. Look for gaps in their positioning
        
        Focus on actionable competitive intelligence that reveals market opportunities.
        """,
        expected_output=f"""
        Competitor analysis report containing:
        
        1. List of 8-12 key competitors with their positioning
        2. Competitive gaps and opportunities
        3. Messaging analysis and differentiation opportunities
        4. Specific insights relevant to {brand_name}'s positioning strategy
        
        All findings should be specific and evidence-based.
        """,
        async_execution=True  # Run in parallel
    )

def create_customer_insights_task(brand_info: dict):
    """Create task specifically for customer insights"""
    brand_name = brand_info.get("brand", "")
    product = brand_info.get("product", "")
    target = brand_info.get("target", "")
    
    return Task(
        description=f"""
        Research customer insights and pain points for {brand_name} in the {product} market.
        
        Brand Information:
        - Brand: {brand_name}
        - Product: {product}
        - Target Audience: {target}
        
        Use the Customer Insight Research tool to:
        1. Uncover customer pain points and frustrations
        2. Find unmet needs and desires
        3. Identify the language customers use to describe their problems
        4. Discover emerging customer behavior patterns
        
        Focus on insights that reveal opportunities for {brand_name}.
        """,
        expected_output=f"""
        Customer intelligence summary containing:
        
        1. Top 5 customer pain points with specific evidence
        2. Unmet needs and desires
        3. Customer language and terminology preferences
        4. Emerging customer behavior patterns
        
        All insights should be actionable for {brand_name}'s strategy.
        """,
        async_execution=True  # Run in parallel
    )

def create_market_trends_task(brand_info: dict):
    """Create task specifically for market trends"""
    brand_name = brand_info.get("brand", "")
    product = brand_info.get("product", "")
    target = brand_info.get("target", "")
    
    return Task(
        description=f"""
        Analyze market trends and opportunities for {brand_name} in the {product} industry.
        
        Brand Information:
        - Brand: {brand_name}
        - Product: {product}
        - Target Audience: {target}
        
        Use the Market Trend Research tool to:
        1. Identify industry developments and emerging opportunities
        2. Find underserved market segments
        3. Analyze market growth patterns and consumer behavior shifts
        4. Identify regulatory or technological changes affecting the market
        
        Focus on trends that create opportunities for {brand_name}.
        """,
        expected_output=f"""
        Market trend analysis containing:
        
        1. 3-5 key market trends affecting the industry
        2. Underserved market segments
        3. Growth opportunities and market dynamics
        4. Regulatory or technological impacts
        
        All trends should be relevant to {brand_name}'s strategic positioning.
        """,
        async_execution=True  # Run in parallel
    )