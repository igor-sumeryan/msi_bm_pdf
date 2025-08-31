FROM mcr.microsoft.com/playwright/python:v1.54.0-noble

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3-venv \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Create and activate virtual environment
RUN python3 -m venv venv
ENV PATH="/app/venv/bin:$PATH"

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Install Playwright browsers
RUN playwright install

# Copy project files
COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]