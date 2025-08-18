"""
Unit tests for AI agents.
"""

import unittest
import os
import sys
from unittest.mock import patch, MagicMock

# Add src to path for testing
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))


class TestAgents(unittest.TestCase):
    """Test AI agent creation and configuration."""

    @patch.dict(os.environ, {
        'OPENAI_API_KEY': 'test_openai_key',
        'SERP_API_KEY': 'test_serp_key'
    })
    def test_market_intelligence_agent_creation(self):
        """Test market intelligence agent creation."""
        from brand_positioning.agents.agents import create_market_intelligence_agent
        
        agent = create_market_intelligence_agent()
        
        self.assertIsNotNone(agent)
        self.assertEqual(agent.role, "Market Intelligence Specialist")
        self.assertIn("market researcher", agent.backstory.lower())
        self.assertEqual(len(agent.tools), 3)  # Should have 3 tools

    @patch.dict(os.environ, {
        'OPENAI_API_KEY': 'test_openai_key',
        'SERP_API_KEY': 'test_serp_key'
    })
    def test_positioning_strategist_agent_creation(self):
        """Test positioning strategist agent creation."""
        from brand_positioning.agents.agents import create_positioning_strategist_agent
        
        agent = create_positioning_strategist_agent()
        
        self.assertIsNotNone(agent)
        self.assertEqual(agent.role, "Brand Positioning Strategist")
        self.assertIn("brand strategist", agent.backstory.lower())
        self.assertEqual(len(agent.tools), 0)  # Positioning agent has no tools

    @patch.dict(os.environ, {
        'OPENAI_API_KEY': 'test_openai_key',
        'SERP_API_KEY': 'test_serp_key'
    })
    def test_strategic_advisor_agent_creation(self):
        """Test strategic advisor agent creation."""
        from brand_positioning.agents.agents import create_strategic_advisor_agent
        
        agent = create_strategic_advisor_agent()
        
        self.assertIsNotNone(agent)
        self.assertEqual(agent.role, "Strategic Growth Advisor")
        self.assertIn("business advisor", agent.backstory.lower())
        self.assertEqual(len(agent.tools), 1)  # Should have trend tool

    @patch.dict(os.environ, {
        'OPENAI_API_KEY': 'test_openai_key',
        'SERP_API_KEY': 'test_serp_key'
    })
    def test_agent_llm_configuration(self):
        """Test that agents are configured with correct LLM."""
        from brand_positioning.agents.agents import create_market_intelligence_agent
        
        agent = create_market_intelligence_agent()
        
        # Check that agent has LLM configured
        self.assertIsNotNone(agent.llm)
        self.assertEqual(agent.llm.temperature, 0.1)

    @patch.dict(os.environ, {
        'OPENAI_API_KEY': 'test_openai_key',
        'SERP_API_KEY': 'test_serp_key'
    })
    def test_agent_properties(self):
        """Test agent properties and configuration."""
        from brand_positioning.agents.agents import (
            create_market_intelligence_agent,
            create_positioning_strategist_agent,
            create_strategic_advisor_agent
        )
        
        agents = [
            create_market_intelligence_agent(),
            create_positioning_strategist_agent(),
            create_strategic_advisor_agent()
        ]
        
        for agent in agents:
            # All agents should have these properties
            self.assertIsNotNone(agent.role)
            self.assertIsNotNone(agent.goal)
            self.assertIsNotNone(agent.backstory)
            self.assertFalse(agent.allow_delegation)
            self.assertTrue(agent.verbose)


if __name__ == '__main__':
    unittest.main()