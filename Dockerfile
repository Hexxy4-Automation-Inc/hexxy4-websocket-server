# Use official lightweight Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy files
COPY requirements.txt .
COPY websocketServer.py .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port
EXPOSE 8001

# Run the app
CMD ["python3", "websocketServer.py"]
