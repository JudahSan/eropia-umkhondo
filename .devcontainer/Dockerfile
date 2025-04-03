
FROM mcr.microsoft.com/devcontainers/python:3.11

WORKDIR /workspace

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libyaml-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt .
RUN pip install -r requirements.txt

# Default command
CMD ["streamlit", "run", "app.py", "--server.address", "0.0.0.0", "--server.port", "5000"]
