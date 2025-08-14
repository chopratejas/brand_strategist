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
    description: str = "Find gaps in competitor positioning with focused searches (2 API calls max)"

    def _run(self, brand_query: str) -> str:
        """Find positioning gaps with minimal API usage"""
        try:
            # Only 2 focused searches to find gaps
            search_queries = [
                f"{brand_query} competitors alternatives market leaders",
                f"best {brand_query} brands positioning strategy"
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
                "query": brand_query,
                "competitor_count": len(competitor_insights),
                "positioning_clues": competitor_insights
            })
            
        except Exception as e:
            logger.error(f"Competitor gap research failed: {str(e)}")
            return json.dumps({
                "error": f"Gap research failed: {str(e)}",
                "query": brand_query
            })

class PositioningOpportunityTool(BaseTool):
    name: str = "Positioning Opportunity Finder"
    description: str = "Find specific positioning opportunities and strategic moves (2 API calls max)"

    def _run(self, brand_query: str) -> str:
        """Find positioning opportunities with minimal API usage"""
        try:
            # Only 2 strategic searches
            search_queries = [
                f"{brand_query} market trends opportunities 2024",
                f"{brand_query} customer pain points unmet needs"
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
                "query": brand_query,
                "opportunity_count": len(opportunities),
                "strategic_insights": opportunities
            })
            
        except Exception as e:
            logger.error(f"Opportunity research failed: {str(e)}")
            return json.dumps({
                "error": f"Opportunity research failed: {str(e)}",
                "query": brand_query
            })