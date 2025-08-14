"""
Focused tools for finding positioning opportunities with minimal API usage.
"""

import json
import time
from typing import Dict, List, Any
from crewai.tools import BaseTool
from serpapi import GoogleSearch
from brand_positioning.config import Config
import logging

logger = logging.getLogger(__name__)

class CompetitorGapTool(BaseTool):
    name: str = "Competitor Gap Research"
    description: str = "Research specific brand's current positioning and direct competitors (2 API calls max)"

    def _run(self, brand_info: str) -> str:
        """Research the actual brand and its specific competitive landscape"""
        try:
            # Parse brand info to get actual brand name
            brand_data = json.loads(brand_info) if isinstance(brand_info, str) and brand_info.startswith('{') else {"brand": brand_info.split()[0] if brand_info else "", "product": brand_info}
            brand_name = brand_data.get("brand", "")
            
            # Brand-specific searches to understand CURRENT positioning
            search_queries = [
                f'"{brand_name}" brand positioning strategy current website',
                f'"{brand_name}" competitors direct alternatives similar companies'
            ]
            
            all_results = []
            for search_query in search_queries:
                logger.info(f"Gap research: {search_query}")
                search = GoogleSearch({
                    "q": search_query,
                    "api_key": Config.SERP_API_KEY,
                    "num": 5  # Only 5 results per search
                })
                results = search.get_dict()
                
                if "organic_results" in results:
                    all_results.extend(results["organic_results"][:3])  # Only top 3 from each
                
                time.sleep(1)  # Rate limiting
            
            # Format for positioning analysis
            competitor_insights = []
            for result in all_results:
                competitor_insights.append({
                    "title": result.get("title", ""),
                    "positioning_clue": result.get("snippet", "")
                })
            
            return json.dumps({
                "query": f"{brand_name} competitors",
                "competitor_count": len(competitor_insights),
                "positioning_clues": competitor_insights
            })
            
        except Exception as e:
            logger.error(f"Competitor gap research failed: {str(e)}")
            return json.dumps({
                "error": f"Gap research failed: {str(e)}",
                "query": brand_info
            })

class PositioningOpportunityTool(BaseTool):
    name: str = "Positioning Opportunity Finder" 
    description: str = "Find brand-specific positioning gaps and strategic opportunities (2 API calls max)"

    def _run(self, brand_info: str) -> str:
        """Find opportunities based on brand's current market position"""
        try:
            # Parse brand info
            brand_data = json.loads(brand_info) if isinstance(brand_info, str) and brand_info.startswith('{') else {"brand": brand_info.split()[0] if brand_info else "", "product": brand_info}
            brand_name = brand_data.get("brand", "")
            product = brand_data.get("product", "")
            
            # Brand-specific opportunity searches
            search_queries = [
                f'"{brand_name}" customer reviews complaints pain points problems',
                f'"{brand_name}" {product} market gaps underserved segments opportunities'
            ]
            
            all_results = []
            for search_query in search_queries:
                logger.info(f"Opportunity research: {search_query}")
                search = GoogleSearch({
                    "q": search_query,
                    "api_key": Config.SERP_API_KEY,
                    "num": 5  # Only 5 results per search
                })
                results = search.get_dict()
                
                if "organic_results" in results:
                    all_results.extend(results["organic_results"][:3])  # Only top 3 from each
                
                time.sleep(1)  # Rate limiting
            
            # Format for opportunity analysis
            opportunities = []
            for result in all_results:
                opportunities.append({
                    "title": result.get("title", ""),
                    "opportunity_insight": result.get("snippet", "")
                })
            
            return json.dumps({
                "query": f"{brand_name} opportunities",
                "opportunity_count": len(opportunities),
                "strategic_insights": opportunities
            })
            
        except Exception as e:
            logger.error(f"Opportunity research failed: {str(e)}")
            return json.dumps({
                "error": f"Opportunity research failed: {str(e)}",
                "query": brand_info
            })