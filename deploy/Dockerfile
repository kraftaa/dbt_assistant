# Start with Python slim
FROM python:3.11-slim

# Install system deps
RUN apt-get update && apt-get install -y build-essential libfaiss-dev wget curl && rm -rf /var/lib/apt/lists/*

# Set workdir
WORKDIR /app

# Copy files
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Run Gunicorn in container
CMD ["gunicorn", "-c", "gunicorn_conf.py", "app:app"]