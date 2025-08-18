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

    def _run(self, brand: str, product: str = "") -> str:
        """Research the actual brand and its specific competitive landscape"""
        try:
            # Handle both direct parameters and JSON string input
            if brand.startswith("{") and brand.endswith("}"):
                # Agent passed JSON string, parse it
                data = json.loads(brand)
                brand_name = data.get("brand", "")
                product_name = data.get("product", "")
            else:
                # Direct parameters
                brand_name = brand
                product_name = product
                
            brand_data = {"brand": brand_name, "product": product_name}
            
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
                "query": f"{brand} {product}"
            })

class PositioningOpportunityTool(BaseTool):
    name: str = "Positioning Opportunity Finder" 
    description: str = "Find brand-specific positioning gaps and strategic opportunities (2 API calls max)"

    def _run(self, brand: str, product: str = "") -> str:
        """Find opportunities based on brand's current market position"""
        try:
            # Handle both direct parameters and JSON string input
            if brand.startswith("{") and brand.endswith("}"):
                # Agent passed JSON string, parse it
                data = json.loads(brand)
                brand_name = data.get("brand", "")
                product_name = data.get("product", "")
            else:
                # Direct parameters
                brand_name = brand
                product_name = product
                
            brand_data = {"brand": brand_name, "product": product_name}
            
            # Brand-specific opportunity searches
            search_queries = [
                f'"{brand_name}" customer reviews complaints pain points problems',
                f'"{brand_name}" {product_name} market gaps underserved segments opportunities'
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
                "query": f"{brand} {product}"
            })