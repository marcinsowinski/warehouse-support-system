import os
from pathlib import Path
from dataclasses import dataclass
from dotenv import load_dotenv

def load_environment():
    """Load environment variables from Streamlit secrets or .env file"""
    # First try to use Streamlit secrets
    try:
        import streamlit as st
        if st._is_running_with_streamlit:
            print("Running in Streamlit Cloud, using secrets...")
            os.environ['JIRA_SERVER'] = st.secrets['JIRA_SERVER']
            os.environ['JIRA_USER'] = st.secrets['JIRA_USER']
            os.environ['JIRA_API_TOKEN'] = st.secrets['JIRA_API_TOKEN']
            os.environ['JIRA_PROJECT'] = st.secrets['JIRA_PROJECT']
            os.environ['OPENAI_API_KEY'] = st.secrets['OPENAI_API_KEY']
            return
    except Exception as e:
        print("Not running in Streamlit Cloud, will try .env file...")

    # If we're here, we're running locally and need the .env file
    try:
        env_path = Path(__file__).parent.parent / '.env'
        if env_path.exists():
            print("Loading from .env file...")
            load_dotenv(dotenv_path=str(env_path.absolute()))
        else:
            print("No .env file found for local development.")
    except Exception as e:
        print(f"Error loading .env file: {str(e)}")

# Load environment variables
load_environment()

@dataclass
class Settings:
    JIRA_SERVER: str = os.getenv('JIRA_SERVER', '')
    JIRA_USER: str = os.getenv('JIRA_USER', '')
    JIRA_API_TOKEN: str = os.getenv('JIRA_API_TOKEN', '')
    JIRA_PROJECT: str = os.getenv('JIRA_PROJECT', '')
    OPENAI_API_KEY: str = os.getenv('OPENAI_API_KEY', '')

    def validate(self):
        """Validate that all required settings are set"""
        missing = []
        for field in [
            'JIRA_SERVER',
            'JIRA_USER',
            'JIRA_API_TOKEN',
            'JIRA_PROJECT',
            'OPENAI_API_KEY'
        ]:
            value = getattr(self, field)
            if not value or value.isspace():
                missing.append(field)
        
        if missing:
            raise ValueError(
                f"Missing required environment variables: {', '.join(missing)}\n"
                "Please ensure all required variables are set either in:\n"
                "1. Your local .env file, or\n"
                "2. Streamlit Cloud secrets"
            )

print("\nInitializing settings...")
settings = Settings()
