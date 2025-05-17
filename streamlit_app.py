"""
Streamlit entry point for the Warehouse Management System Support application.
"""
import sys
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent.absolute()
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

# Import and run the main app
from warehouse_support.app import main

if __name__ == "__main__":
    main() 