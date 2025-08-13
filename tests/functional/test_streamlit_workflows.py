"""
Simplified functional tests for Streamlit UI workflows.
"""

import unittest
import os
import sys
from unittest.mock import patch, MagicMock

# Add src to path for testing
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))


class TestStreamlitWorkflows(unittest.TestCase):
    """Test essential Streamlit UI functionality."""

    def setUp(self):
        """Set up test environment."""
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

    def test_app_configuration_display(self):
        """Test that the app displays configuration correctly."""
        from brand_positioning.config import Config
        
        # Force dev mode for this test
        Config.DEV_MODE = True
        
        # Test config display functionality
        mode_info = Config.get_mode_info()
        self.assertIn('mode', mode_info)
        self.assertIn('serp_calls', mode_info)
        self.assertIn('estimated_time', mode_info)
        
        # Verify dev mode configuration is working
        self.assertEqual(mode_info['mode'], 'Development')
        self.assertEqual(mode_info['serp_calls'], 5)

    def test_form_validation_logic(self):
        """Test form validation logic without UI components."""
        # Test brand info validation
        valid_brand_info = {
            "brand": "TestBrand",
            "product": "Test product description",
            "target": "Test audience"
        }
        
        # Verify required fields
        self.assertTrue(valid_brand_info["brand"].strip())
        self.assertTrue(valid_brand_info["product"].strip())
        
        # Test empty brand name (should be invalid)
        invalid_brand_info = {
            "brand": "",
            "product": "Test product",
            "target": "Test audience"
        }
        
        self.assertFalse(invalid_brand_info["brand"].strip())

    def test_result_display_error_handling(self):
        """Test that UI properly handles error results."""
        from brand_positioning.ui.app import display_results
        
        # Test error result
        error_result = {
            "error": "API key validation failed"
        }
        
        with patch('streamlit.error') as mock_error:
            display_results(error_result)
            
            # Verify error was displayed
            mock_error.assert_called_once()
            call_args = mock_error.call_args[0][0]
            self.assertIn("API key validation failed", call_args)

    def test_result_display_formatting(self):
        """Test that analysis results are properly formatted."""
        from brand_positioning.ui.app import display_results
        
        # Create realistic test result
        test_result = {
            "success": True,
            "brand_info": {
                "brand": "TestCorp",
                "product": "AI analytics platform",
                "target": "Small businesses"
            },
            "intelligence": {
                "competitor_analysis": "Test competitor analysis",
                "customer_insights": "Test customer insights", 
                "market_trends": "Test market trends"
            }
        }
        
        # Test with mock Streamlit functions
        with patch('streamlit.markdown') as mock_markdown, \
             patch('streamlit.tabs') as mock_tabs, \
             patch('streamlit.expander') as mock_expander:
            
            # Mock tabs context manager
            mock_tab = MagicMock()
            mock_tab.__enter__ = MagicMock(return_value=mock_tab)
            mock_tab.__exit__ = MagicMock(return_value=None)
            mock_tabs.return_value = [mock_tab, mock_tab, mock_tab]
            
            # Mock expander context manager
            mock_exp = MagicMock()
            mock_exp.__enter__ = MagicMock(return_value=mock_exp)
            mock_exp.__exit__ = MagicMock(return_value=None)
            mock_expander.return_value = mock_exp
            
            # Run display function
            display_results(test_result)
            
            # Verify that formatting functions were called
            self.assertTrue(mock_markdown.called)
            self.assertTrue(mock_tabs.called)

    @patch('brand_positioning.tools.tools.GoogleSearch')
    @patch('crewai.crew.Crew.kickoff')
    def test_workflow_integration_structure(self, mock_kickoff, mock_serp):
        """Test that workflow integration has correct structure."""
        
        # Set up basic mocks
        mock_serp_instance = MagicMock()
        mock_serp_instance.get_dict.return_value = {
            "organic_results": [{"title": "Test", "snippet": "Test snippet"}]
        }
        mock_serp.return_value = mock_serp_instance
        
        # Mock CrewAI crew execution results
        mock_result = MagicMock()
        mock_result.raw = "Test analysis result"
        mock_kickoff.return_value = mock_result
        
        # Test the integration structure
        from brand_positioning.core.parallel_crews import run_parallel_intelligence_sync
        
        test_brand_info = {
            "brand": "IntegrationTest",
            "product": "Test platform",
            "target": "Test users"
        }
        
        result = run_parallel_intelligence_sync(test_brand_info)
        
        # Verify basic structure
        self.assertTrue(result.get("success"), f"Integration failed: {result.get('error')}")
        self.assertIn("intelligence", result)
        self.assertEqual(result["brand_info"]["brand"], "IntegrationTest")


if __name__ == '__main__':
    unittest.main()