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
        
        self.assertEqual(dev_config['total_serp_calls'], 4)
        self.assertIn('gap_research_calls', dev_config)
        self.assertIn('opportunity_calls', dev_config)
        self.assertIn('results_per_search', dev_config)
        
        # Test mode info
        mode_info = Config.get_mode_info()
        self.assertEqual(mode_info['mode'], 'Development')
        self.assertEqual(mode_info['serp_calls'], 4)

    def test_focused_agent_can_be_created(self):
        """Test that focused positioning agent can be instantiated."""
        from brand_positioning.agents.focused_agents import create_positioning_specialist_agent
        
        # Test agent creation
        positioning_agent = create_positioning_specialist_agent()
        
        # Verify basic properties
        self.assertEqual(positioning_agent.role, "Brand Positioning Specialist")
        
        # Verify tools assignment
        self.assertEqual(len(positioning_agent.tools), 2)  # Should have 2 focused tools

    def test_focused_tasks_contain_brand_information(self):
        """Test that focused tasks are properly created with brand information."""
        from brand_positioning.core.focused_tasks import (
            create_niche_positioning_task,
            create_strategic_move_task
        )
        from brand_positioning.agents.focused_agents import create_positioning_specialist_agent
        
        agent = create_positioning_specialist_agent()
        
        # Test niche positioning task
        positioning_task = create_niche_positioning_task(self.test_brand_info, agent)
        self.assertIn("TestBrand", positioning_task.description)
        self.assertIn("AI-powered test platform", positioning_task.description)
        
        # Test strategic move task
        move_task = create_strategic_move_task(self.test_brand_info, agent)
        self.assertIn("TestBrand", move_task.description)

    def test_focused_tools_handle_basic_input_validation(self):
        """Test that focused tools handle edge cases gracefully."""
        from brand_positioning.tools.focused_tools import (
            CompetitorGapTool,
            PositioningOpportunityTool
        )
        
        # Test tool creation
        gap_tool = CompetitorGapTool()
        opportunity_tool = PositioningOpportunityTool()
        
        # Verify basic properties
        self.assertEqual(gap_tool.name, "Competitor Gap Research")
        self.assertEqual(opportunity_tool.name, "Positioning Opportunity Finder")
        
        # Test with empty brand (should handle gracefully)
        result = gap_tool._run("")
        self.assertIsInstance(result, str)
        
        # Test with basic brand info
        result = opportunity_tool._run("TestBrand", "test product")
        self.assertIsInstance(result, str)

    def test_focused_workflow_structure(self):
        """Test that focused workflow system has correct structure."""
        from brand_positioning.core.focused_workflow import run_focused_positioning_analysis
        
        # Test that function exists and can be imported
        self.assertTrue(callable(run_focused_positioning_analysis))
        
        # Test basic structure - just verify the function exists
        # (We don't want to actually run it in functional tests)

    def test_ui_components_can_be_imported(self):
        """Test that UI components can be imported and initialized."""
        from brand_positioning.ui.app import (
            init_session_state,
            display_focused_results
        )
        
        # Test function imports
        self.assertTrue(callable(init_session_state))
        self.assertTrue(callable(display_focused_results))
        
        # Test display with error result
        error_result = {"error": "Test error"}
        # Should not raise exception
        try:
            with patch('streamlit.error'):
                display_focused_results(error_result)
        except Exception as e:
            self.fail(f"display_focused_results raised an exception: {e}")

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
        
        # Test that focused tasks preserve brand info
        from brand_positioning.core.focused_tasks import create_niche_positioning_task
        from brand_positioning.agents.focused_agents import create_positioning_specialist_agent
        
        agent = create_positioning_specialist_agent()
        task = create_niche_positioning_task(brand_info, agent)
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
        self.assertEqual(dev_calls, 4)   # Dev mode limit
        self.assertEqual(prod_calls, 6)  # Prod mode limit

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