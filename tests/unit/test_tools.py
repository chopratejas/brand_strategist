"""
Unit tests for focused research tools.
"""

import unittest
import os
import sys
from unittest.mock import patch

# Add src to path for testing
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))


class TestFocusedTools(unittest.TestCase):
    """Test focused research tool functionality."""

    @patch.dict(os.environ, {
        'OPENAI_API_KEY': 'test_openai_key',
        'SERP_API_KEY': 'test_serp_key'
    })
    def test_competitor_gap_tool_creation(self):
        """Test competitor gap tool creation."""
        from brand_positioning.tools.focused_tools import CompetitorGapTool
        
        tool = CompetitorGapTool()
        
        self.assertIsNotNone(tool)
        self.assertEqual(tool.name, "Competitor Gap Research")
        self.assertIn("competitor", tool.description.lower())

    @patch.dict(os.environ, {
        'OPENAI_API_KEY': 'test_openai_key',
        'SERP_API_KEY': 'test_serp_key'
    })
    def test_positioning_opportunity_tool_creation(self):
        """Test positioning opportunity tool creation."""
        from brand_positioning.tools.focused_tools import PositioningOpportunityTool
        
        tool = PositioningOpportunityTool()
        
        self.assertIsNotNone(tool)
        self.assertEqual(tool.name, "Positioning Opportunity Finder")
        self.assertIn("opportunity", tool.description.lower())

    def test_tool_configuration_usage(self):
        """Test that tools use configuration settings."""
        from brand_positioning.config import Config
        
        # Test that config returns expected structure
        search_config = Config.get_search_config()
        self.assertIn('gap_research_calls', search_config)
        self.assertIn('opportunity_calls', search_config)
        self.assertIn('total_serp_calls', search_config)


if __name__ == '__main__':
    unittest.main()