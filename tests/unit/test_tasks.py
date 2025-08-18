"""
Unit tests for focused task definitions.
"""

import unittest
import os
import sys

# Add src to path for testing
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from brand_positioning.core.focused_tasks import create_niche_positioning_task, create_strategic_move_task
from brand_positioning.agents.focused_agents import create_positioning_specialist_agent


class TestFocusedTasks(unittest.TestCase):
    """Test focused task creation and configuration."""

    def setUp(self):
        """Set up test data."""
        self.test_brand_info = {
            "brand": "TestBrand",
            "product": "AI-powered test platform",
            "target": "Tech entrepreneurs"
        }
        self.agent = create_positioning_specialist_agent()

    def test_niche_positioning_task_creation(self):
        """Test niche positioning task creation."""
        task = create_niche_positioning_task(self.test_brand_info, self.agent)
        
        self.assertIsNotNone(task)
        self.assertIn("TestBrand", task.description)
        self.assertIn("AI-powered test platform", task.description)
        self.assertIn("niche", task.description.lower())
        self.assertIn("Your Exact Niche", task.expected_output)

    def test_strategic_move_task_creation(self):
        """Test strategic move task creation."""
        task = create_strategic_move_task(self.test_brand_info, self.agent)
        
        self.assertIsNotNone(task)
        self.assertIn("TestBrand", task.description)
        self.assertIn("strategic move", task.description.lower())
        self.assertIn("30-Day Execution", task.expected_output)

    def test_strategic_move_task_with_positioning_context(self):
        """Test strategic move task with positioning context."""
        positioning_context = "Test positioning results"
        
        task = create_strategic_move_task(self.test_brand_info, self.agent, positioning_context)
        
        self.assertIn("POSITIONING CONTEXT", task.description)
        self.assertIn("Test positioning results", task.description)

    def test_task_brand_info_validation(self):
        """Test task creation with incomplete brand info."""
        incomplete_brand_info = {"brand": "TestBrand"}
        
        # Tasks should handle missing fields gracefully
        task = create_niche_positioning_task(incomplete_brand_info, self.agent)
        self.assertIsNotNone(task)
        self.assertIn("TestBrand", task.description)

    def test_task_descriptions_focus_on_specificity(self):
        """Test that task descriptions emphasize specificity."""
        task = create_niche_positioning_task(self.test_brand_info, self.agent)
        
        # Should emphasize specificity
        description = task.description.lower()
        self.assertIn("specific", description)
        self.assertIn("exact", description) 
        self.assertIn("ultra-specific", description)
        
        # Should ban generic terms
        self.assertIn("banned words", description)
        self.assertIn("wellness", description)  # Listed as banned


if __name__ == '__main__':
    unittest.main()