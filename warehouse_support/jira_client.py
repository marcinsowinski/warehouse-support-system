from typing import List, Tuple
from jira import JIRA
from .settings import settings

class JiraClient:
    def __init__(self):
        self.client = JIRA(
            server=settings.JIRA_SERVER,
            basic_auth=(settings.JIRA_EMAIL, settings.JIRA_API_TOKEN)
        )
        # Store both project keys
        self.project_keys = ["ATS", "WCS"]

    def search_similar_issues(self, query: str, max_results: int = 5) -> List[Tuple[str, str, str]]:
        """
        Search for similar issues in both ATS and WCS projects
        Returns a list of tuples containing (issue_key, summary, description)
        """
        # Create JQL to search in both projects
        jql = f'project in ({",".join(self.project_keys)}) AND text ~ "{query}" ORDER BY created DESC'
        
        try:
            issues = self.client.search_issues(jql, maxResults=max_results)
            return [(issue.key, issue.fields.summary, issue.fields.description or "")
                    for issue in issues]
        except Exception as e:
            print(f"Error searching Jira: {str(e)}")
            return []  # Return empty list on error to allow graceful degradation 