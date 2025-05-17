import os
from pathlib import Path
from dataclasses import dataclass
from dotenv import load_dotenv

# Get the absolute path to the .env file
env_path = Path(__file__).parent.parent / '.env'
env_path_str = str(env_path.absolute())

print("\n=== Environment Setup Debug Information ===")
print(f"1. Looking for .env file at: {env_path_str}")

# Check if .env file exists
if not env_path.exists():
    print(f"ERROR: .env file not found!")
    print(f"Please create the file at exactly this location: {env_path_str}")
    print("Make sure the file is named '.env' (with the dot)")
    raise FileNotFoundError(f".env file not found at {env_path_str}")

print(f"2. .env file found: Yes")

# Try to read the .env file content (without showing sensitive data)
try:
    with open(env_path, 'r') as f:
        lines = f.readlines()
    print(f"3. Number of lines in .env file: {len(lines)}")
    print("4. Variables found in .env file (checking format):")
    for line in lines:
        line = line.strip()
        if line and not line.startswith('#'):
            if '=' not in line:
                print(f"   WARNING: Line missing '=' symbol: {line}")
            else:
                var_name, var_value = line.split('=', 1)
                var_name = var_name.strip()
                var_value = var_value.strip()
                if not var_value:
                    print(f"   WARNING: Empty value for variable: {var_name}")
                if ' ' in var_name or ' ' in var_value:
                    print(f"   WARNING: Spaces found in variable {var_name}")
                print(f"   - {var_name}: {'[Set]' if var_value else '[Empty]'}")
except Exception as e:
    print(f"ERROR reading .env file: {str(e)}")

# Load the .env file
print("\n5. Attempting to load environment variables...")
load_dotenv(dotenv_path=env_path_str)

# Debug: Print current environment variables
print("6. Environment variables after loading:")
for var in ['JIRA_SERVER', 'JIRA_EMAIL', 'JIRA_API_TOKEN', 'JIRA_PROJECT_KEY', 'GEMINI_API_KEY']:
    value = os.getenv(var)
    print(f"   - {var}: {'[Set]' if value else '[Not set]'}")

@dataclass
class Settings:
    JIRA_SERVER: str = os.getenv('JIRA_SERVER', '')
    JIRA_EMAIL: str = os.getenv('JIRA_EMAIL', '')
    JIRA_API_TOKEN: str = os.getenv('JIRA_API_TOKEN', '')
    JIRA_PROJECT_KEY: str = os.getenv('JIRA_PROJECT_KEY', '')
    GEMINI_API_KEY: str = os.getenv('GEMINI_API_KEY', '')

    def validate(self):
        """Validate that all required settings are set"""
        missing = []
        for field in [
            'JIRA_SERVER',
            'JIRA_EMAIL',
            'JIRA_API_TOKEN',
            'JIRA_PROJECT_KEY',
            'GEMINI_API_KEY'
        ]:
            value = getattr(self, field)
            if not value or value.isspace():
                missing.append(field)
        
        if missing:
            raise ValueError(
                f"Missing required environment variables: {', '.join(missing)}\n"
                f"Please check your .env file at: {env_path_str}\n"
                "Make sure:\n"
                "1. The file is named exactly '.env'\n"
                "2. There are no spaces before or after the '=' sign\n"
                "3. All variables have values\n"
                "4. The file is saved in plain text format"
            )

print("\n7. Creating settings object...")
settings = Settings()
