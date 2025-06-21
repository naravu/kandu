# Use official Python image
FROM python:3.11

# Set the working directory
WORKDIR /app

# Copy project files into the container
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose Flask app port (default 5000)
EXPOSE 5000

# Run Flask application
CMD ["python", "app.py"]
