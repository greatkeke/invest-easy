# Use official Python image
FROM python:3.13.2

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set working directory
WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Add volume for database persistence
VOLUME /app/db

# Expose the configured port
EXPOSE 10008

# Run the application
CMD ["uvicorn", "app.app:app", "--host", "0.0.0.0", "--port", "10008"]
