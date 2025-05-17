FROM python:3.12-slim

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the rest of the application
COPY . .

# Create directory for system specifications
RUN mkdir -p system_specs

# Expose the port Streamlit runs on
EXPOSE 8501

# Command to run the application
CMD ["python", "launcher.py"] 