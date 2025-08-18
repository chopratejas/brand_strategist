"""
Unit tests for focused positioning agents.
"""

import unittest
import os
import sys
from unittest.mock import patch, MagicMock

# Add src to path for testing
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))


class TestFocusedAgents(unittest.TestCase):
    """Test focused positioning agent creation and configuration."""

    @patch.dict(os.environ, {
        'OPENAI_API_KEY': 'test_openai_key',
        'SERP_API_KEY': 'test_serp_key'
    })
    def test_positioning_specialist_agent_creation(self):
        """Test positioning specialist agent creation."""
        from brand_positioning.agents.focused_agents import create_positioning_specialist_agent
        
        agent = create_positioning_specialist_agent()
        
        self.assertIsNotNone(agent)
        self.assertEqual(agent.role, "Brand Positioning Specialist")
        self.assertIn("positioning expert", agent.backstory.lower())
        self.assertEqual(len(agent.tools), 2)  # Should have 2 focused tools

    @patch.dict(os.environ, {
        'OPENAI_API_KEY': 'test_openai_key',
        'SERP_API_KEY': 'test_serp_key'
    })
    def test_agent_llm_configuration(self):
        """Test that agent is configured with correct LLM."""
        from brand_positioning.agents.focused_agents import create_positioning_specialist_agent
        
        agent = create_positioning_specialist_agent()
        
        # Check that agent has LLM configured
        self.assertIsNotNone(agent.llm)
        self.assertEqual(agent.llm.temperature, 0.1)

    @patch.dict(os.environ, {
        'OPENAI_API_KEY': 'test_openai_key',
        'SERP_API_KEY': 'test_serp_key'
    })  
    def test_agent_properties(self):
        """Test agent properties and configuration."""
        from brand_positioning.agents.focused_agents import create_positioning_specialist_agent
        
        agent = create_positioning_specialist_agent()
        
        # Agent should have these properties
        self.assertIsNotNone(agent.role)
        self.assertIsNotNone(agent.goal)
        self.assertIsNotNone(agent.backstory)
        self.assertFalse(agent.allow_delegation)
        self.assertTrue(agent.verbose)


if __name__ == '__main__':
    unittest.main()