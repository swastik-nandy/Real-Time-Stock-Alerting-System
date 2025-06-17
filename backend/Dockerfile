FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy all files into the image
COPY . .

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt && \
    pip install gunicorn  # ✅ Add this if not in requirements.txt

# Install supervisord
RUN apt-get update && \
    apt-get install -y supervisor && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Make sure start.sh is executable
RUN chmod +x /app/start.sh

# Expose the port Render will use
EXPOSE 8000

# Start all services via supervisord
CMD ["supervisord", "-c", "/app/supervisord.conf"]
