# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 5000 available to the world outside this container
EXPOSE 8080

# Define environment variable
ENV FLASK_APP=app.py
ENV AMADEUS_API_KEY="KDzdGffAcDALOLdXrd1BK1xWP6LmUoro"
ENV AMADEUS_API_SECRET_KEY="Ateg3JNMLLmVefig"

# Run flask when the container launches
CMD ["python", "server.py"]
