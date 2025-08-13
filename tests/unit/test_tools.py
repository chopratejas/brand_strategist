"""
Unit tests for research tools.
"""

import unittest
import os
import sys
from unittest.mock import patch

# Add src to path for testing
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))


class TestTools(unittest.TestCase):
    """Test research tool functionality."""

    @patch.dict(os.environ, {
        'OPENAI_API_KEY': 'test_openai_key',
        'SERP_API_KEY': 'test_serp_key'
    })
    def test_competitor_research_tool_creation(self):
        """Test competitor research tool creation."""
        from brand_positioning.tools.tools import CompetitorResearchTool
        
        tool = CompetitorResearchTool()
        
        self.assertIsNotNone(tool)
        self.assertEqual(tool.name, "Competitor Research")
        self.assertIn("competitors", tool.description.lower())

    @patch.dict(os.environ, {
        'OPENAI_API_KEY': 'test_openai_key',
        'SERP_API_KEY': 'test_serp_key'
    })
    def test_customer_insight_tool_creation(self):
        """Test customer insight tool creation."""
        from brand_positioning.tools.tools import CustomerInsightTool
        
        tool = CustomerInsightTool()
        
        self.assertIsNotNone(tool)
        self.assertEqual(tool.name, "Customer Insight Research")
        self.assertIn("customer", tool.description.lower())

    @patch.dict(os.environ, {
        'OPENAI_API_KEY': 'test_openai_key',
        'SERP_API_KEY': 'test_serp_key'
    })
    def test_market_trend_tool_creation(self):
        """Test market trend tool creation."""
        from brand_positioning.tools.tools import MarketTrendTool
        
        tool = MarketTrendTool()
        
        self.assertIsNotNone(tool)
        self.assertEqual(tool.name, "Market Trend Research")
        self.assertIn("trends", tool.description.lower())

    def test_tool_configuration_usage(self):
        """Test that tools use configuration settings."""
        from brand_positioning.config import Config
        
        # Test that config returns expected structure
        search_config = Config.get_search_config()
        self.assertIn('competitor_searches', search_config)
        self.assertIn('total_serp_calls', search_config)


if __name__ == '__main__':
    unittest.main()