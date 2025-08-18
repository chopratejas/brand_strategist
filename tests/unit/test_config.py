"""
Unit tests for configuration management.
"""

import unittest
import os
from unittest.mock import patch, MagicMock
import sys

# Add src to path for testing
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from brand_positioning.config import Config


class TestConfig(unittest.TestCase):
    """Test configuration management functionality."""

    def setUp(self):
        """Set up test environment."""
        # Store original environment
        self.original_env = os.environ.copy()

    def tearDown(self):
        """Clean up test environment."""
        # Restore original environment
        os.environ.clear()
        os.environ.update(self.original_env)

    @patch.dict(os.environ, {
        'OPENAI_API_KEY': 'test_openai_key',
        'SERP_API_KEY': 'test_serp_key',
        'DEV_MODE': 'true'
    })
    def test_config_validation_success(self):
        """Test successful configuration validation."""
        # Should not raise any exception
        Config.validate()

    def test_config_validation_missing_keys(self):
        """Test configuration validation with missing keys."""
        # Temporarily clear the config values
        original_openai = Config.OPENAI_API_KEY
        original_serp = Config.SERP_API_KEY
        
        Config.OPENAI_API_KEY = None
        Config.SERP_API_KEY = None
        
        try:
            with self.assertRaises(ValueError) as context:
                Config.validate()
            self.assertIn("Missing API keys", str(context.exception))
        finally:
            # Restore original values
            Config.OPENAI_API_KEY = original_openai
            Config.SERP_API_KEY = original_serp

    @patch.dict(os.environ, {'DEV_MODE': 'true'})
    def test_dev_mode_configuration(self):
        """Test development mode configuration."""
        # Force reload of config
        Config.DEV_MODE = os.getenv("DEV_MODE", "true").lower() == "true"
        
        self.assertTrue(Config.DEV_MODE)
        
        search_config = Config.get_search_config()
        self.assertEqual(search_config['total_serp_calls'], 5)
        self.assertEqual(search_config['competitor_searches'], 2)
        self.assertEqual(search_config['customer_searches'], 2)
        self.assertEqual(search_config['trend_searches'], 1)

    @patch.dict(os.environ, {'DEV_MODE': 'false'})
    def test_prod_mode_configuration(self):
        """Test production mode configuration."""
        # Force reload of config
        Config.DEV_MODE = os.getenv("DEV_MODE", "true").lower() == "true"
        
        self.assertFalse(Config.DEV_MODE)
        
        search_config = Config.get_search_config()
        self.assertEqual(search_config['total_serp_calls'], 20)
        self.assertEqual(search_config['competitor_searches'], 6)
        self.assertEqual(search_config['customer_searches'], 8)
        self.assertEqual(search_config['trend_searches'], 6)

    @patch.dict(os.environ, {'DEV_MODE': 'true'})
    def test_mode_info_dev(self):
        """Test mode info in development mode."""
        Config.DEV_MODE = True
        
        mode_info = Config.get_mode_info()
        self.assertEqual(mode_info['mode'], 'Development')
        self.assertEqual(mode_info['serp_calls'], 5)

    @patch.dict(os.environ, {'DEV_MODE': 'false'})
    def test_mode_info_prod(self):
        """Test mode info in production mode."""
        Config.DEV_MODE = False
        
        mode_info = Config.get_mode_info()
        self.assertEqual(mode_info['mode'], 'Production')
        self.assertEqual(mode_info['serp_calls'], 20)


if __name__ == '__main__':
    unittest.main()