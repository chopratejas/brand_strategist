"""
Main entry point for Streamlit Cloud deployment.
Streamlit Cloud looks for this file by default.
"""

import sys
import os

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Import and run the main app
from brand_positioning.ui.app import main

if __name__ == "__main__":
    main()