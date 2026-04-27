# Use the official slim Python 3.13 image as the base
FROM python:3.13-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the dependency manifest first so Docker can cache this layer
# independently of the application source code
COPY requirements.txt .

# Install dependencies (no cache keeps the image smaller)
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application source code
COPY app.py .

# Expose the port gunicorn will listen on
EXPOSE 5000

# Run the app with gunicorn:
#   -w 2          → 2 worker processes
#   -b 0.0.0.0    → listen on all interfaces inside the container
CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:5000", "app:app"]
