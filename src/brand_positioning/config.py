import os
from dotenv import load_dotenv

load_dotenv()

# Disable CrewAI telemetry to avoid connection errors
os.environ["OTEL_SDK_DISABLED"] = "true"

# Langfuse Observability Configuration  
os.environ["LANGFUSE_PUBLIC_KEY"] = os.getenv("LANGFUSE_PUBLIC_KEY", "")
os.environ["LANGFUSE_SECRET_KEY"] = os.getenv("LANGFUSE_SECRET_KEY", "")
os.environ["LANGFUSE_HOST"] = os.getenv("LANGFUSE_HOST", "https://us.cloud.langfuse.com")

class Config:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY") 
    SERP_API_KEY = os.getenv("SERP_API_KEY")
    
    # Development Mode Configuration
    DEV_MODE = os.getenv("DEV_MODE", "true").lower() == "true"  # Default to dev mode
    
    # LLM Configuration
    OPENAI_MODEL = "gpt-4o"
    CLAUDE_MODEL = "claude-3-5-sonnet-20241022"
    
    # Focused Search Configuration (Minimal API usage)
    @classmethod
    def get_search_config(cls):
        """Get focused search configuration - minimal API usage for targeted insights"""
        if cls.DEV_MODE:
            return {
                "gap_research_calls": 2,       # Find competitor gaps
                "opportunity_calls": 2,        # Find positioning opportunities
                "results_per_search": 5,       # 5 results per search
                "total_serp_calls": 4          # Total: 2+2 = 4 calls
            }
        else:
            return {
                "gap_research_calls": 2,       # Same focused approach in prod
                "opportunity_calls": 2,        # Quality over quantity
                "results_per_search": 5,       # Still focused
                "total_serp_calls": 4          # Total: 2+2 = 4 calls (much cheaper!)
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
            "estimated_cost": "$0.20" if cls.DEV_MODE else "$0.20",  # Much cheaper!
            "estimated_time": "1-2 minutes" if cls.DEV_MODE else "1-2 minutes"  # Much faster!
        }
    
    @classmethod
    def validate(cls):
        required_keys = ["OPENAI_API_KEY", "SERP_API_KEY"]
        missing = [key for key in required_keys if not getattr(cls, key)]
        if missing:
            raise ValueError(f"Missing API keys: {', '.join(missing)}")
        return True