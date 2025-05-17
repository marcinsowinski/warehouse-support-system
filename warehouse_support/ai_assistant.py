from typing import List, Tuple
import os
from pathlib import Path
import google.generativeai as genai
from PyPDF2 import PdfReader
from .settings import settings

class AIAssistant:
    def __init__(self):
        # Configure the Gemini API
        genai.configure(api_key=settings.GEMINI_API_KEY)
        
        # Use the recommended model version
        self.model_name = "gemini-1.5-flash"
        print(f"\nUsing model: {self.model_name}")
        self.model = genai.GenerativeModel(self.model_name)
        
        # Set up system specs path
        self.specs_dir = Path(__file__).parent.parent / 'system_specs'
        if not self.specs_dir.exists():
            os.makedirs(self.specs_dir, exist_ok=True)

    def _read_pdf(self, file_path: Path) -> str:
        """Read content from a PDF file"""
        try:
            reader = PdfReader(file_path)
            text = []
            for page in reader.pages:
                text.append(page.extract_text())
            return "\n".join(text)
        except Exception as e:
            print(f"Error reading PDF {file_path}: {e}")
            return f"Error reading PDF {file_path.name}: {str(e)}"

    def _load_system_specs(self) -> str:
        """Load system specifications from files in the system_specs directory"""
        specs_content = []
        if self.specs_dir.exists():
            # Handle both PDF and txt files
            for file in self.specs_dir.glob('*.*'):
                if file.suffix.lower() in ['.pdf', '.txt']:
                    try:
                        if file.suffix.lower() == '.pdf':
                            content = self._read_pdf(file)
                        else:
                            with open(file, 'r', encoding='utf-8') as f:
                                content = f.read()
                        
                        if content:  # Only add if we got some content
                            specs_content.append(f"=== {file.name} ===\n{content}")
                    except Exception as e:
                        print(f"Error reading {file}: {e}")
        
        if specs_content:
            return "\n\n".join(specs_content)
        return "No system specifications available."

    def generate_response(self, query: str, similar_issues: List[Tuple[str, str, str]]) -> str:
        """
        Generate a response based on the user query and similar issues
        """
        try:
            # Create context from similar issues
            similar_issues_context = ""
            if similar_issues:
                # Group issues by project
                ats_issues = []
                wcs_issues = []
                for key, summary, desc in similar_issues:
                    if key.startswith('ATS-'):
                        ats_issues.append((key, summary, desc))
                    elif key.startswith('WCS-'):
                        wcs_issues.append((key, summary, desc))

                # Format issues by project
                issues_text = []
                if ats_issues:
                    issues_text.append("ATS Project Issues:\n" + "\n\n".join([
                        f"Issue {key}:\nSummary: {summary}\nDescription: {desc}"
                        for key, summary, desc in ats_issues
                    ]))
                if wcs_issues:
                    issues_text.append("WCS Project Issues:\n" + "\n\n".join([
                        f"Issue {key}:\nSummary: {summary}\nDescription: {desc}"
                        for key, summary, desc in wcs_issues
                    ]))
                
                similar_issues_context = "\n\n".join(issues_text)
            else:
                similar_issues_context = "No similar past issues found in either ATS or WCS projects."

            # Load system specifications
            system_specs = self._load_system_specs()

            # Create the prompt with clear sections and instructions
            prompt = f"""You are a Warehouse Management System Support Assistant. Your task is to help users with their queries by analyzing both past issues from ATS and WCS projects, and system specifications.

User Query: {query}

Past Issues Context:
{similar_issues_context}

System Specifications:
{system_specs}

Please provide a comprehensive response that:
1. First, analyze any similar past issues that are relevant to the query:
   - Reference specific issue numbers (e.g., ATS-123 or WCS-456)
   - Consider patterns across both ATS and WCS projects
   - Explain how past solutions from either project might apply
   - Note any recurring issues or differences between projects

2. Then, incorporate relevant system specifications:
   - Reference specific sections of the documentation
   - Explain how the system is designed to handle this type of situation
   - Point out any relevant configuration or setup requirements
   - Note any differences in handling between ATS and WCS if applicable

3. Finally, provide a solution that:
   - Combines insights from both past issues and system specifications
   - Gives step-by-step instructions when applicable
   - Suggests preventive measures for the future
   - Recommends when to escalate to system administrators
   - Considers both ATS and WCS project contexts

Format your response with clear sections:
- Past Issues Analysis (ATS & WCS)
- System Specifications Reference
- Recommended Solution
"""

            # Get completion from Gemini
            response = self.model.generate_content(prompt)
            
            # Check if the response is valid
            if response.text:
                return response.text
            else:
                return "I apologize, but I couldn't generate a response. Please try rephrasing your query."
        except Exception as e:
            error_msg = f"Error generating response: {str(e)}"
            print(error_msg)
            return error_msg 