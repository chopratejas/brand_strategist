import os
from dotenv import load_dotenv

load_dotenv()

# Disable CrewAI telemetry to avoid connection errors
os.environ["OTEL_SDK_DISABLED"] = "true"

class Config:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY") 
    SERP_API_KEY = os.getenv("SERP_API_KEY")
    
    # Development Mode Configuration
    DEV_MODE = os.getenv("DEV_MODE", "true").lower() == "true"  # Default to dev mode
    
    # LLM Configuration
    OPENAI_MODEL = "gpt-4o"
    CLAUDE_MODEL = "claude-3-5-sonnet-20241022"
    
    # Search Configuration (Dynamic based on mode)
    @classmethod
    def get_search_config(cls):
        """Get search configuration based on dev/prod mode"""
        if cls.DEV_MODE:
            return {
                "competitor_searches": 2,      # Minimal for dev
                "customer_searches": 2,        # Minimal for dev  
                "trend_searches": 1,           # Minimal for dev
                "results_per_search": 5,       # Fewer results per search
                "total_serp_calls": 5          # Total: 2+2+1 = 5 calls
            }
        else:
            return {
                "competitor_searches": 6,      # Full production analysis
                "customer_searches": 8,        # Comprehensive customer insights
                "trend_searches": 6,           # Complete trend analysis  
                "results_per_search": 10,      # Full results per search
                "total_serp_calls": 20         # Total: 6+8+6 = 20 calls
            }
    
    # Rate Limiting
    REQUESTS_PER_MINUTE = 60
    
    @classmethod
    def get_mode_info(cls):
        """Get current mode information"""
        config = cls.get_search_config()
        return {
            "mode": "Development" if cls.DEV_MODE else "Production",
            "serp_calls": config["total_serp_calls"],
            "estimated_cost": "$1-2" if cls.DEV_MODE else "$5-8",
            "estimated_time": "2-3 minutes" if cls.DEV_MODE else "8-12 minutes"
        }
    
    @classmethod
    def validate(cls):
        required_keys = ["OPENAI_API_KEY", "ANTHROPIC_API_KEY", "SERP_API_KEY"]
        missing = [key for key in required_keys if not getattr(cls, key)]
        if missing:
            raise ValueError(f"Missing required environment variables: {missing}")
        return True