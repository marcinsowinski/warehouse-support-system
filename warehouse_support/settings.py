import os
from pathlib import Path
from dataclasses import dataclass
from dotenv import load_dotenv

def load_environment():
    """Load environment variables from Streamlit secrets or .env file"""
    try:
        # Try to import streamlit and get secrets
        import streamlit as st
        print("Running in Streamlit Cloud, using secrets...")
        os.environ['JIRA_SERVER'] = st.secrets['JIRA_SERVER']
        os.environ['JIRA_USER'] = st.secrets['JIRA_USER']
        os.environ['JIRA_API_TOKEN'] = st.secrets['JIRA_API_TOKEN']
        os.environ['JIRA_PROJECT'] = st.secrets['JIRA_PROJECT']
        os.environ['OPENAI_API_KEY'] = st.secrets['OPENAI_API_KEY']
        return
    except Exception as e:
        print(f"Not running in Streamlit Cloud or secrets not set: {str(e)}")
        print("Falling back to .env file...")

    # Fall back to .env file
    env_path = Path(__file__).parent.parent / '.env'
    env_path_str = str(env_path.absolute())

    if not env_path.exists():
        raise FileNotFoundError(
            f".env file not found at {env_path_str} and Streamlit secrets not available.\n"
            "Please either:\n"
            "1. Create a .env file for local development, or\n"
            "2. Set up secrets in Streamlit Cloud"
        )

    load_dotenv(dotenv_path=env_path_str)

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
