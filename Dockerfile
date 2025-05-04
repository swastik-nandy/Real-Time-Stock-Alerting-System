# Use official lightweight Python image
FROM python:3.11-slim

# Set working directory inside the container
WORKDIR /app

# Install system dependencies first (needed for psycopg2)
RUN apt-get update && apt-get install -y gcc libpq-dev

# Install Python packages
RUN pip install requests python-dotenv psycopg2

# Copy project files
COPY . .

# Command to run fetcher
CMD ["python", "services/fetcher.py"]
