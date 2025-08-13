#!/usr/bin/env python3
"""
Entry point for the Brand Positioning Intelligence Platform.
Launches the Streamlit web interface.
"""

import sys
import os

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

if __name__ == "__main__":
    import streamlit.web.cli as stcli
    import sys
    
    # Path to the main app
    app_path = os.path.join(os.path.dirname(__file__), 'src', 'brand_positioning', 'ui', 'app.py')
    
    # Launch Streamlit
    sys.argv = ["streamlit", "run", app_path]
    sys.exit(stcli.main())