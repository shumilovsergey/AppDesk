# Base image
FROM python:3.9

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    TG_TOKEN="" \
    GROUP_ID="" \
    ALLOWED_HOST=""
# Set working directory
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install -r requirements.txt

# Copy application code
COPY . .

# Expose port
# EXPOSE 5050

# Define volume for database
VOLUME /app/data

# Start server
CMD python manage.py runserver 0.0.0.0:8000