#!/usr/bin/env python3
"""
Setup verification script for Brand Positioning Intelligence Platform.
Run this after installation to ensure all components are working correctly.
"""

import os
import sys
import logging

def test_environment_variables():
    """Test that required environment variables are set."""
    print("Testing environment variables...")
    
    required_vars = ['OPENAI_API_KEY', 'SERP_API_KEY']
    optional_vars = ['ANTHROPIC_API_KEY']
    
    missing_required = []
    for var in required_vars:
        if not os.getenv(var):
            missing_required.append(var)
    
    if missing_required:
        print(f"ERROR: Missing required environment variables: {', '.join(missing_required)}")
        print("Please check your .env file and ensure all required variables are set.")
        return False
    
    print("All required environment variables are set.")
    
    # Check optional variables
    for var in optional_vars:
        if os.getenv(var):
            print(f"Optional variable {var} is configured.")
        else:
            print(f"Optional variable {var} is not set (this is fine).")
    
    return True

def test_imports():
    """Test that all required packages can be imported."""
    print("\nTesting package imports...")
    
    required_packages = [
        ('streamlit', 'Streamlit web framework'),
        ('crewai', 'CrewAI multi-agent framework'),
        ('langchain_openai', 'OpenAI integration'),
        ('serpapi', 'SerpAPI integration'),
        ('openai', 'OpenAI Python client'),
    ]
    
    optional_packages = [
        ('langchain_anthropic', 'Anthropic Claude integration'),
    ]
    
    failed_imports = []
    
    for package, description in required_packages:
        try:
            __import__(package)
            print(f"OK: {package} - {description}")
        except ImportError as e:
            print(f"FAIL: {package} - {description}: {e}")
            failed_imports.append(package)
    
    for package, description in optional_packages:
        try:
            __import__(package)
            print(f"OK: {package} - {description}")
        except ImportError:
            print(f"SKIP: {package} - {description}: Not installed (optional)")
    
    if failed_imports:
        print(f"\nERROR: Failed to import required packages: {', '.join(failed_imports)}")
        print("Please run: pip install -r requirements.txt")
        return False
    
    print("All required packages imported successfully.")
    return True

def test_configuration():
    """Test configuration loading."""
    print("\nTesting configuration loading...")
    
    try:
        from config import Config
        
        # Test configuration loading
        Config.validate()
        print("Configuration validation passed.")
        
        # Test dev/prod mode switching
        mode_info = Config.get_mode_info()
        search_config = Config.get_search_config()
        
        print(f"Current mode: {mode_info['mode']}")
        print(f"SerpAPI calls configured: {search_config['total_serp_calls']}")
        print(f"Estimated cost: {mode_info['estimated_cost']}")
        
        return True
        
    except Exception as e:
        print(f"ERROR: Configuration test failed: {e}")
        return False

def test_agents_and_tools():
    """Test agent and tool creation."""
    print("\nTesting agents and tools...")
    
    try:
        from agents import (
            create_market_intelligence_agent,
            create_positioning_strategist_agent,
            create_strategic_advisor_agent
        )
        from tools import CompetitorResearchTool, CustomerInsightTool, MarketTrendTool
        
        # Test agent creation
        market_agent = create_market_intelligence_agent()
        positioning_agent = create_positioning_strategist_agent()
        advisor_agent = create_strategic_advisor_agent()
        
        print("All agents created successfully.")
        
        # Test tool creation
        competitor_tool = CompetitorResearchTool()
        customer_tool = CustomerInsightTool()
        trend_tool = MarketTrendTool()
        
        print("All tools created successfully.")
        return True
        
    except Exception as e:
        print(f"ERROR: Agent/tool test failed: {e}")
        return False

def test_parallel_crews():
    """Test parallel crews orchestration."""
    print("\nTesting parallel crews orchestration...")
    
    try:
        from parallel_crews import ParallelCrewsOrchestrator
        
        # Test orchestrator creation
        orchestrator = ParallelCrewsOrchestrator()
        print("ParallelCrewsOrchestrator created successfully.")
        
        # Test crew creation (without execution)
        test_brand_info = {
            "brand": "TestBrand",
            "product": "Test product for verification",
            "target": "Test audience"
        }
        
        competitor_crew = orchestrator.create_competitor_crew(test_brand_info)
        customer_crew = orchestrator.create_customer_crew(test_brand_info)
        trends_crew = orchestrator.create_trends_crew(test_brand_info)
        
        print("All parallel crews created successfully.")
        return True
        
    except Exception as e:
        print(f"ERROR: Parallel crews test failed: {e}")
        return False

def main():
    """Run all setup tests."""
    print("Brand Positioning Intelligence Platform - Setup Verification")
    print("=" * 60)
    
    # Suppress non-essential logging during tests
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("openai").setLevel(logging.WARNING)
    
    tests = [
        test_environment_variables,
        test_imports,
        test_configuration,
        test_agents_and_tools,
        test_parallel_crews,
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
            else:
                break  # Stop on first failure for required tests
        except KeyboardInterrupt:
            print("\nTest interrupted by user.")
            sys.exit(1)
        except Exception as e:
            print(f"ERROR: Unexpected error in {test.__name__}: {e}")
            break
    
    print("\n" + "=" * 60)
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("All tests passed. Your setup is ready.")
        print("\nTo start the application, run:")
        print("streamlit run app.py")
    else:
        print("Some tests failed. Please fix the issues above before running the application.")
        sys.exit(1)

if __name__ == "__main__":
    main()