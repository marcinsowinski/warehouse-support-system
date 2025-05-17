import streamlit as st
from warehouse_support.jira_client import JiraClient
from warehouse_support.ai_assistant import AIAssistant
from warehouse_support.settings import settings

def initialize_session_state():
    """Initialize or get session state variables."""
    if 'jira_client' not in st.session_state:
        st.session_state.jira_client = JiraClient()
    if 'ai_assistant' not in st.session_state:
        st.session_state.ai_assistant = AIAssistant()

def main():
    # Set page config at the very top
    st.set_page_config(
        page_title="Warehouse Management System Support",
        page_icon="🏭",
        layout="wide"
    )

    st.title("🏭 Warehouse Management System Support")
    
    try:
        # Initialize settings and session state
        settings.validate()
        initialize_session_state()

        st.markdown("""
        This application helps troubleshoot warehouse management system issues by leveraging:
        - Historical Jira tickets
        - AI-powered analysis with system specifications
        - Real-time issue resolution
        """)

        # User input
        user_query = st.text_area(
            "Describe your issue:",
            height=100,
            placeholder="e.g., 'Scanner is not connecting to the system' or 'Inventory count is showing incorrect values'"
        )

        if st.button("Get Help", type="primary"):
            if user_query:
                with st.spinner("Analyzing your issue..."):
                    similar_issues = st.session_state.jira_client.search_similar_issues(user_query)
                    response = st.session_state.ai_assistant.generate_response(user_query, similar_issues)
                    
                    st.success("Analysis complete!")
                    
                    if similar_issues:
                        st.subheader("📋 Similar Past Issues")
                        for key, summary, _ in similar_issues:
                            st.markdown(f"- **{key}**: {summary}")
                    
                    st.subheader("🤖 AI Assistant Recommendation")
                    st.markdown(response)
                    
                    st.info("""
                    💡 Note: This is an AI-generated recommendation based on historical data and system specifications.
                    If the issue persists, please contact your system administrator or create a new Jira ticket.
                    """)
            else:
                st.warning("Please describe your issue first.")

    except ValueError as e:
        st.error(f"Configuration Error: {str(e)}")
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        st.exception(e)  # This will show the full traceback in development

if __name__ == "__main__":
    main() 