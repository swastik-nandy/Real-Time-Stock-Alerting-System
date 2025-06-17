FROM python:3.11-slim

# Set workdir
WORKDIR /app

# Copy all project files
COPY . .

# Install dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Install supervisord
RUN apt-get update && apt-get install -y supervisor

# Expose port
EXPOSE 8000


# Start all services with supervisord
CMD ["supervisord", "-c", "/app/supervisord.conf"]
