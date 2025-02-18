# Use an official Python runtime as a parent image
FROM python:3.12.2

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app


# Install any dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port that the Flask app runs on
EXPOSE 3344

# Run the Gunicorn server
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:3344", "wsgi:app"]
