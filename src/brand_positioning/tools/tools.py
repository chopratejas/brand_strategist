import json
import time
from typing import Dict, List, Any
from crewai.tools import BaseTool
from serpapi import GoogleSearch
from brand_positioning.config import Config
import logging

logger = logging.getLogger(__name__)

class CompetitorResearchTool(BaseTool):
    name: str = "Competitor Research"
    description: str = "Search and analyze competitors in a specific market using SerpAPI and LLM analysis"

    def _run(self, query: str) -> str:
        """Search for competitors and return structured analysis"""
        try:
            # Get search configuration based on dev/prod mode
            search_config = Config.get_search_config()
            
            # Base search queries (will be limited by config)
            base_queries = [
                f"{query} competitors brands 2025",
                f"best {query} companies market leaders", 
                f"{query} vs alternatives comparison",
                f"top {query} startups companies",
                f"{query} market analysis competitive landscape",
                f"{query} industry leaders pricing strategy"
            ]
            
            # Limit queries based on configuration
            search_queries = base_queries[:search_config["competitor_searches"]]
            
            all_results = []
            for search_query in search_queries:
                logger.info(f"Searching competitors: {search_query}")
                search = GoogleSearch({
                    "q": search_query,
                    "api_key": Config.SERP_API_KEY,
                    "num": search_config["results_per_search"]
                })
                results = search.get_dict()
                
                if "organic_results" in results:
                    all_results.extend(results["organic_results"])
                
                time.sleep(1)  # Rate limiting
            
            # Format results for LLM analysis
            formatted_results = []
            for result in all_results[:30]:  # Limit for efficiency
                formatted_results.append({
                    "title": result.get("title", ""),
                    "snippet": result.get("snippet", ""),
                    "link": result.get("link", "")
                })
            
            return json.dumps({
                "query": query,
                "total_results": len(formatted_results),
                "results": formatted_results
            })
            
        except Exception as e:
            logger.error(f"Competitor research error: {e}")
            return json.dumps({"error": str(e), "results": []})

class CustomerInsightTool(BaseTool):
    name: str = "Customer Insight Research"
    description: str = "Research customer pain points, reviews, and discussions about products/markets"

    def _run(self, query: str) -> str:
        """Search for customer insights and return structured data"""
        try:
            # Get search configuration based on dev/prod mode
            search_config = Config.get_search_config()
            
            # Base insight queries (will be limited by config)
            base_queries = [
                f"{query} customer reviews problems 2025",
                f"{query} reddit complaints issues",
                f"{query} customer testimonials feedback",
                f"{query} user experience problems",
                f"{query} customer pain points survey",
                f"{query} negative reviews analysis",
                f"{query} customer satisfaction problems",
                f"{query} user complaints forums discussions"
            ]
            
            # Limit queries based on configuration
            insight_queries = base_queries[:search_config["customer_searches"]]
            
            all_results = []
            for search_query in insight_queries:
                logger.info(f"Searching customer insights: {search_query}")
                search = GoogleSearch({
                    "q": search_query,
                    "api_key": Config.SERP_API_KEY,
                    "num": search_config["results_per_search"]
                })
                results = search.get_dict()
                
                if "organic_results" in results:
                    all_results.extend(results["organic_results"])
                
                time.sleep(1)
            
            # Format results
            formatted_results = []
            for result in all_results[:30]:
                formatted_results.append({
                    "title": result.get("title", ""),
                    "snippet": result.get("snippet", ""),
                    "link": result.get("link", "")
                })
            
            return json.dumps({
                "query": query,
                "total_results": len(formatted_results),
                "results": formatted_results
            })
            
        except Exception as e:
            logger.error(f"Customer insight error: {e}")
            return json.dumps({"error": str(e), "results": []})

class MarketTrendTool(BaseTool):
    name: str = "Market Trend Research"
    description: str = "Research market trends, opportunities, and industry developments"

    def _run(self, query: str) -> str:
        """Search for market trends and return structured data"""
        try:
            # Get search configuration based on dev/prod mode
            search_config = Config.get_search_config()
            
            # Base trend queries (will be limited by config)
            base_queries = [
                f"{query} market trends 2025 industry report",
                f"{query} market size growth forecast",
                f"{query} industry analysis emerging trends",
                f"{query} market opportunities 2025",
                f"{query} consumer behavior trends",
                f"{query} market research statistics data"
            ]
            
            # Limit queries based on configuration
            trend_queries = base_queries[:search_config["trend_searches"]]
            
            all_results = []
            for search_query in trend_queries:
                logger.info(f"Searching market trends: {search_query}")
                search = GoogleSearch({
                    "q": search_query,
                    "api_key": Config.SERP_API_KEY,
                    "num": search_config["results_per_search"]
                })
                results = search.get_dict()
                
                if "organic_results" in results:
                    all_results.extend(results["organic_results"])
                
                time.sleep(1)
            
            # Format results
            formatted_results = []
            for result in all_results[:30]:
                formatted_results.append({
                    "title": result.get("title", ""),
                    "snippet": result.get("snippet", ""),
                    "link": result.get("link", "")
                })
            
            return json.dumps({
                "query": query,
                "total_results": len(formatted_results),
                "results": formatted_results
            })
            
        except Exception as e:
            logger.error(f"Market trend error: {e}")
            return json.dumps({"error": str(e), "results": []})