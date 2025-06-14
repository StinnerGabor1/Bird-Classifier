FROM python:3.10-slim

# Install needed system packages for ML (e.g., OpenCV, TensorFlow)
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Set working directory in the container
WORKDIR /app

# Copy all local files to the container
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

# Start the Flask app with Gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:8000", "app:app"]