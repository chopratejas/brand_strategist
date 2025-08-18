"""
Unit tests for task definitions.
"""

import unittest
import os
import sys

# Add src to path for testing
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from brand_positioning.core.tasks import create_positioning_strategy_task, create_strategic_action_task
from brand_positioning.core.parallel_tasks import (
    create_competitor_analysis_task,
    create_customer_insights_task,
    create_market_trends_task
)


class TestTasks(unittest.TestCase):
    """Test task creation and configuration."""

    def setUp(self):
        """Set up test data."""
        self.test_brand_info = {
            "brand": "TestBrand",
            "product": "AI-powered test platform",
            "target": "Tech entrepreneurs"
        }

    def test_positioning_strategy_task_creation(self):
        """Test positioning strategy task creation."""
        task = create_positioning_strategy_task(self.test_brand_info)
        
        self.assertIsNotNone(task)
        self.assertIn("TestBrand", task.description)
        self.assertIn("AI-powered test platform", task.description)
        self.assertIn("positioning strategy", task.description.lower())
        self.assertIn("ULTRA-SPECIFIC", task.expected_output)

    def test_positioning_task_with_intelligence_data(self):
        """Test positioning task with intelligence context."""
        intelligence_data = {
            "competitor_analysis": "Test competitor data",
            "customer_insights": "Test customer data",
            "market_trends": "Test trend data"
        }
        
        task = create_positioning_strategy_task(self.test_brand_info, intelligence_data)
        
        self.assertIn("MARKET INTELLIGENCE FINDINGS", task.description)
        self.assertIn("Test competitor data", task.description)
        self.assertIn("Test customer data", task.description)
        self.assertIn("Test trend data", task.description)

    def test_strategic_action_task_creation(self):
        """Test strategic action task creation."""
        task = create_strategic_action_task(self.test_brand_info)
        
        self.assertIsNotNone(task)
        self.assertIn("TestBrand", task.description)
        self.assertIn("strategic moves", task.description.lower())
        self.assertIn("implementation roadmap", task.expected_output.lower())

    def test_strategic_action_task_with_positioning_data(self):
        """Test strategic action task with positioning context."""
        positioning_data = "Test positioning strategy results"
        
        task = create_strategic_action_task(self.test_brand_info, positioning_data)
        
        self.assertIn("POSITIONING STRATEGY", task.description)
        self.assertIn("Test positioning strategy results", task.description)

    def test_competitor_analysis_task_creation(self):
        """Test competitor analysis task creation."""
        task = create_competitor_analysis_task(self.test_brand_info)
        
        self.assertIsNotNone(task)
        self.assertIn("TestBrand", task.description)
        self.assertIn("Competitor Research tool", task.description)
        self.assertTrue(task.async_execution)

    def test_customer_insights_task_creation(self):
        """Test customer insights task creation."""
        task = create_customer_insights_task(self.test_brand_info)
        
        self.assertIsNotNone(task)
        self.assertIn("TestBrand", task.description)
        self.assertIn("Customer Insight Research tool", task.description)
        self.assertTrue(task.async_execution)

    def test_market_trends_task_creation(self):
        """Test market trends task creation."""
        task = create_market_trends_task(self.test_brand_info)
        
        self.assertIsNotNone(task)
        self.assertIn("TestBrand", task.description)
        self.assertIn("Market Trend Research tool", task.description)
        self.assertTrue(task.async_execution)

    def test_task_brand_info_validation(self):
        """Test task creation with incomplete brand info."""
        incomplete_brand_info = {"brand": "TestBrand"}
        
        # Tasks should handle missing fields gracefully
        task = create_positioning_strategy_task(incomplete_brand_info)
        self.assertIsNotNone(task)
        self.assertIn("TestBrand", task.description)

    def test_task_descriptions_industry_agnostic(self):
        """Test that task descriptions are industry-agnostic."""
        task = create_positioning_strategy_task(self.test_brand_info)
        
        # Should not contain industry-specific terms
        description = task.description.lower()
        self.assertNotIn("wellness", description)
        self.assertNotIn("health", description)
        self.assertNotIn("supplement", description)
        
        # Should contain generic business terms
        self.assertIn("brand", description)
        self.assertIn("strategist", description)


if __name__ == '__main__':
    unittest.main()