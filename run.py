import os
import sys
from pathlib import Path

# Get the absolute path of the project root directory
root_dir = Path(__file__).parent.absolute()

# Add the project root to Python path so we can import from warehouse_support
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

# Import and run the Streamlit app
import streamlit.web.bootstrap as bootstrap

def main():
    app_path = os.path.join(root_dir, "warehouse_support", "app.py")
    print(f"Running app from: {app_path}")
    print(f"Python path: {sys.path}")
    bootstrap.run(app_path, "", [], {})

if __name__ == "__main__":
    main() 