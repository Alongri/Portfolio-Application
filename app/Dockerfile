# Use official Python slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies if needed (optional)
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy only requirements first to leverage Docker cache
COPY requirements.txt ./

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy only the application code needed

COPY main.py ./
COPY static ./static
COPY templates ./templates

# Expose the port the app runs on
EXPOSE 5000

# Start the Flask server
CMD ["python", "main.py"]

