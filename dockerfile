# Use the official Python image as the base image
FROM python:3.9

# Set environment variables for Flask
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5000

# Copy the application files into the container
WORKDIR /app
COPY . .

# Install the required packages
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port on which Flask will run
EXPOSE 5000

# Start the Flask application
CMD ["flask", "run"]