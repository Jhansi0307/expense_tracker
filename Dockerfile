FROM python:3.11-slim

# Prevent python from buffering logs
ENV PYTHONUNBUFFERED=1

# Create directory
WORKDIR /app

# Install system dependencies (needed for psycopg2 & pandas)
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirement file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port used by uvicorn
EXPOSE 10000

# Run the FastAPI app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "10000"]
