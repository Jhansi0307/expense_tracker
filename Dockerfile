# -------------------------
# Base Image
# -------------------------
FROM python:3.11-slim

# -------------------------
# Set Work Directory
# -------------------------
WORKDIR /app

# -------------------------
# Install system dependencies
# (required by psycopg2-binary + bcrypt)
# -------------------------
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# -------------------------
# Install Python dependencies
# -------------------------
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# -------------------------
# Copy project files
# -------------------------
COPY . .

# -------------------------
# Make Alembic config accessible
# -------------------------
COPY alembic.ini /app/alembic.ini
COPY alembic /app/alembic

# -------------------------
# Add entrypoint script
# -------------------------
COPY docker-entrypoint.sh /app/docker-entrypoint.sh
RUN chmod +x /app/docker-entrypoint.sh

# -------------------------
# Expose port
# -------------------------
EXPOSE 10000

# -------------------------
# Run entrypoint (runs Alembic first)
# -------------------------
ENTRYPOINT ["/app/docker-entrypoint.sh"]

# -------------------------
# Start FastAPI
# -------------------------
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "10000"]
