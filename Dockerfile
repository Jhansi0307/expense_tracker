# Use Python 3.11
FROM python:3.11-slim

# Set work directory
WORKDIR /app

# Install system dependencies (psycopg2 dependencies)
RUN apt-get update && apt-get install -y gcc libpq-dev

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy code
COPY . .

# Run Alembic migrations before starting the app
RUN alembic upgrade head

# Start FastAPI server
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "10000"]
