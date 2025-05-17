"""
Launcher script for the Warehouse Management System Support application.
This ensures proper Python path setup before running the Streamlit app.
"""

import os
import sys
from pathlib import Path

def setup_environment():
    """Set up the Python path to include the package directory."""
    # Get the absolute path of the project root (parent of this file)
    project_root = Path(__file__).parent.absolute()
    
    # Add the project root to Python path if not already there
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))
        print(f"Added {project_root} to Python path")

def main():
    setup_environment()
    
    # Get the path to app.py
    app_path = os.path.join(os.path.dirname(__file__), "warehouse_support", "app.py")
    
    # Run the Streamlit app using the streamlit command
    os.system(f"streamlit run {app_path}")

if __name__ == "__main__":
    main() 