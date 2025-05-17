# Warehouse Management System Support

An AI-powered support system that helps troubleshoot warehouse management system issues by analyzing past Jira tickets and system specifications.

## Features

- Search and analyze similar issues from ATS and WCS Jira projects
- Incorporate system specifications from documentation
- AI-powered response generation using Google's Gemini model
- User-friendly web interface built with Streamlit

## Setup

1. Clone this repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the project root with the following variables:
```
# Jira Settings
JIRA_SERVER=your_jira_server
JIRA_EMAIL=your_email
JIRA_API_TOKEN=your_api_token
JIRA_PROJECT_KEY=ATS

# Gemini API Settings
GEMINI_API_KEY=your_gemini_api_key
```

4. Place your system specification documents (PDF or TXT) in the `system_specs` directory.

## Running Locally

```bash
python launcher.py
```

## Deployment

### Streamlit Cloud (Recommended)

1. Push your code to GitHub
2. Visit [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repository
4. Add your environment variables in the Streamlit Cloud settings
5. Deploy!

### Alternative Deployment Options

- **Docker**: Use the provided Dockerfile
- **Self-hosted**: Can be deployed on any server with Python support

## Security Notes

- Never commit your `.env` file or any sensitive credentials
- Use environment variables for all sensitive information
- Ensure proper access controls are in place

## Support

For issues or questions, please contact the system administrator. 