# Brand Positioning Intelligence Platform

An AI-powered competitive intelligence platform that helps businesses develop data-driven positioning strategies using multi-agent analysis.

## Overview

This platform uses multiple AI agents to analyze your brand's competitive landscape, customer insights, and market trends, then generates specific positioning recommendations and implementation strategies.

## Quick Start

### Prerequisites
- Python 3.11 or higher
- API keys for OpenAI (required), Anthropic (optional), and SerpAPI (required)

### Installation

1. Clone the repository and set up the environment:
```bash
git clone <repository-url>
cd brand-strategist
python -m venv brand_positioning_env
source brand_positioning_env/bin/activate
pip install -r requirements.txt
```

2. Configure your environment variables:
```bash
cp .env.example .env
# Edit .env with your API keys
```

3. Run the application:
```bash
streamlit run app.py
```

4. Open http://localhost:8501 in your browser

## How It Works

### Input Required
- Brand name
- Product description
- Target audience (optional)

### Analysis Options
- **Quick Analysis**: Market intelligence only (2-4 minutes)
- **Full Analysis**: Complete positioning strategy with implementation plan (6-10 minutes)

### Output Generated
- Competitive landscape analysis
- Customer pain points and insights
- Market trend analysis
- Specific positioning recommendations
- Implementation roadmap with priorities

## Configuration

The platform operates in two modes controlled by the `DEV_MODE` environment variable:

- **Development Mode** (`DEV_MODE=true`): Uses 5 SerpAPI calls for testing
- **Production Mode** (`DEV_MODE=false`): Uses 20 SerpAPI calls for comprehensive analysis

## Architecture

### Core Components
- `app.py`: Streamlit web interface
- `parallel_crews.py`: Multi-agent orchestration system
- `agents.py`: AI agent definitions
- `parallel_tasks.py`: Task definitions for parallel execution
- `tools.py`: SerpAPI integration tools
- `config.py`: Configuration management

### Key Features
- Parallel processing using multiple CrewAI crews
- Real-time status updates during analysis
- Development and production mode configurations
- Comprehensive error handling and logging

## Performance

### Resource Usage
- Development mode: ~5 SerpAPI calls, estimated cost $0.25-0.50 per analysis
- Production mode: ~20 SerpAPI calls, estimated cost $0.50-2.00 per analysis
- Analysis time: 2-10 minutes depending on mode and analysis type

### Technical Stack
- CrewAI for multi-agent orchestration
- OpenAI GPT-4o for strategic analysis
- SerpAPI for real-time market research
- Streamlit for web interface
- Python asyncio and threading for parallel processing

## Development

### Project Structure
```
brand-strategist/
├── app.py                    # Main application
├── parallel_crews.py         # Parallel orchestration
├── agents.py                 # Agent definitions
├── parallel_tasks.py         # Parallel task definitions
├── tools.py                  # Research tools
├── tasks.py                  # Sequential tasks
├── config.py                 # Configuration
└── requirements.txt          # Dependencies
```

### Testing Setup
Run the setup verification script to ensure everything is configured correctly:
```bash
python test_setup.py
```

## Future Development

The current implementation serves as a foundation for potential enterprise features:

- Multi-user authentication and company workspaces
- Database storage for analysis history
- Advanced analytics and trend tracking
- API access for programmatic analysis
- Integration with CRM and marketing platforms
- PDF and presentation export capabilities

See ARCHITECTURE.md for detailed technical information.

## License

Proprietary software. Contact the development team for licensing information.