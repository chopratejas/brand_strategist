"""
Focused functional tests for core brand positioning functionality.
Tests the essential workflows without complex mocking.
"""

import unittest
import os
import sys
from unittest.mock import patch

# Add src to path for testing
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))


class TestCoreFunctionality(unittest.TestCase):
    """Test core functionality that users depend on."""

    def setUp(self):
        """Set up test environment."""
        self.test_brand_info = {
            "brand": "TestBrand",
            "product": "AI-powered test platform",
            "target": "Software engineers"
        }
        
        # Mock environment variables
        self.env_patcher = patch.dict(os.environ, {
            'OPENAI_API_KEY': 'test_openai_key',
            'SERP_API_KEY': 'test_serp_key',
            'DEV_MODE': 'true'
        })
        self.env_patcher.start()

    def tearDown(self):
        """Clean up test environment."""
        self.env_patcher.stop()

    def test_configuration_system_works(self):
        """Test that configuration system provides correct values."""
        from brand_positioning.config import Config
        
        # Test dev mode configuration
        Config.DEV_MODE = True
        dev_config = Config.get_search_config()
        
        self.assertEqual(dev_config['total_serp_calls'], 5)
        self.assertIn('competitor_searches', dev_config)
        self.assertIn('customer_searches', dev_config)
        self.assertIn('trend_searches', dev_config)
        
        # Test mode info
        mode_info = Config.get_mode_info()
        self.assertEqual(mode_info['mode'], 'Development')
        self.assertEqual(mode_info['serp_calls'], 5)

    def test_agents_can_be_created(self):
        """Test that all agent types can be instantiated."""
        from brand_positioning.agents.agents import (
            create_market_intelligence_agent,
            create_positioning_strategist_agent,
            create_strategic_advisor_agent
        )
        
        # Test agent creation
        intelligence_agent = create_market_intelligence_agent()
        positioning_agent = create_positioning_strategist_agent()
        strategic_agent = create_strategic_advisor_agent()
        
        # Verify basic properties
        self.assertEqual(intelligence_agent.role, "Market Intelligence Specialist")
        self.assertEqual(positioning_agent.role, "Brand Positioning Strategist")
        self.assertEqual(strategic_agent.role, "Strategic Growth Advisor")
        
        # Verify tools assignment
        self.assertEqual(len(intelligence_agent.tools), 3)  # Should have 3 research tools
        self.assertEqual(len(positioning_agent.tools), 0)   # No tools for positioning
        self.assertEqual(len(strategic_agent.tools), 1)     # Should have trend tool

    def test_tasks_contain_brand_information(self):
        """Test that tasks are properly created with brand information."""
        from brand_positioning.core.tasks import (
            create_positioning_strategy_task,
            create_strategic_action_task
        )
        from brand_positioning.core.parallel_tasks import (
            create_competitor_analysis_task,
            create_customer_insights_task,
            create_market_trends_task
        )
        
        # Test positioning task
        positioning_task = create_positioning_strategy_task(self.test_brand_info)
        self.assertIn("TestBrand", positioning_task.description)
        self.assertIn("AI-powered test platform", positioning_task.description)
        
        # Test strategic action task
        action_task = create_strategic_action_task(self.test_brand_info)
        self.assertIn("TestBrand", action_task.description)
        
        # Test parallel tasks
        competitor_task = create_competitor_analysis_task(self.test_brand_info)
        customer_task = create_customer_insights_task(self.test_brand_info)
        trends_task = create_market_trends_task(self.test_brand_info)
        
        self.assertIn("TestBrand", competitor_task.description)
        self.assertIn("TestBrand", customer_task.description)
        self.assertIn("TestBrand", trends_task.description)
        
        # Verify async execution is enabled for parallel tasks
        self.assertTrue(competitor_task.async_execution)
        self.assertTrue(customer_task.async_execution)
        self.assertTrue(trends_task.async_execution)

    def test_tools_handle_basic_input_validation(self):
        """Test that tools handle edge cases gracefully."""
        from brand_positioning.tools.tools import (
            CompetitorResearchTool,
            CustomerInsightTool,
            MarketTrendTool
        )
        
        # Test tool creation
        competitor_tool = CompetitorResearchTool()
        customer_tool = CustomerInsightTool()
        trend_tool = MarketTrendTool()
        
        # Verify basic properties
        self.assertEqual(competitor_tool.name, "Competitor Research")
        self.assertEqual(customer_tool.name, "Customer Insight Research")
        self.assertEqual(trend_tool.name, "Market Trend Research")
        
        # Test with empty query (should handle gracefully)
        result = competitor_tool._run("")
        self.assertIsInstance(result, str)
        
        # Test with None query (should handle gracefully)
        result = competitor_tool._run(None)
        self.assertIsInstance(result, str)

    def test_parallel_crews_structure(self):
        """Test that parallel crews system has correct structure."""
        from brand_positioning.core.parallel_crews import (
            run_parallel_intelligence_sync,
            run_parallel_analysis_sync
        )
        
        # Test that functions exist and can be imported
        self.assertTrue(callable(run_parallel_intelligence_sync))
        self.assertTrue(callable(run_parallel_analysis_sync))
        
        # Test basic structure - just verify the functions exist
        # (We don't want to actually run them in functional tests)

    def test_ui_components_can_be_imported(self):
        """Test that UI components can be imported and initialized."""
        from brand_positioning.ui.app import (
            init_session_state,
            display_results
        )
        
        # Test function imports
        self.assertTrue(callable(init_session_state))
        self.assertTrue(callable(display_results))
        
        # Test display with error result
        error_result = {"error": "Test error"}
        # Should not raise exception
        try:
            with patch('streamlit.error'):
                display_results(error_result)
        except Exception as e:
            self.fail(f"display_results raised an exception: {e}")

    def test_brand_info_preservation(self):
        """Test that brand information is preserved through processing."""
        # Test brand info dictionary structure
        brand_info = {
            "brand": "PreservationTest",
            "product": "Data preservation platform",
            "target": "Data engineers"
        }
        
        # Verify the structure we expect
        self.assertIn("brand", brand_info)
        self.assertIn("product", brand_info)
        self.assertIn("target", brand_info)
        
        # Test that tasks preserve brand info
        from brand_positioning.core.tasks import create_positioning_strategy_task
        
        task = create_positioning_strategy_task(brand_info)
        self.assertIn("PreservationTest", task.description)
        self.assertIn("Data preservation platform", task.description)
        self.assertIn("Data engineers", task.description)

    def test_development_vs_production_mode(self):
        """Test that dev/prod modes actually work differently."""
        from brand_positioning.config import Config
        
        # Test development mode
        Config.DEV_MODE = True
        dev_config = Config.get_search_config()
        dev_calls = dev_config['total_serp_calls']
        
        # Test production mode
        Config.DEV_MODE = False
        prod_config = Config.get_search_config()
        prod_calls = prod_config['total_serp_calls']
        
        # Production should use more API calls than development
        self.assertGreater(prod_calls, dev_calls)
        self.assertEqual(dev_calls, 5)   # Dev mode limit
        self.assertEqual(prod_calls, 20)  # Prod mode limit

    def test_error_handling_structure(self):
        """Test that error handling is structured correctly."""
        from brand_positioning.config import Config
        
        # Test config validation with missing keys
        original_openai = Config.OPENAI_API_KEY
        original_serp = Config.SERP_API_KEY
        
        try:
            Config.OPENAI_API_KEY = None
            Config.SERP_API_KEY = None
            
            with self.assertRaises(ValueError) as context:
                Config.validate()
            
            error_message = str(context.exception)
            self.assertIn("Missing API keys", error_message)
            
        finally:
            # Restore original values
            Config.OPENAI_API_KEY = original_openai
            Config.SERP_API_KEY = original_serp


if __name__ == '__main__':
    unittest.main()