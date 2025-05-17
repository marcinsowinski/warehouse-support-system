from setuptools import setup, find_packages

setup(
    name="warehouse_support",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "streamlit>=1.24.0",
        "jira>=3.5.1",
        "google-generativeai>=0.3.0",
        "python-dotenv>=1.0.0",
    ],
) 