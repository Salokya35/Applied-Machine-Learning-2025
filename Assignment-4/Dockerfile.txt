# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Set PYTHONPATH to include the working directory
ENV PYTHONPATH=/app

# Copy the requirements file into the container
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Install NLTK data
RUN python -m nltk.downloader punkt_tab
RUN python -m nltk.downloader punkt
RUN python -m nltk.downloader stopwords

# Copy the application files into the container
COPY app.py .
COPY score.py .
COPY resource/ resource/
COPY src/ src/
COPY Model/ Model/
COPY templates/ templates/

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Run app.py when the container launches
CMD ["python", "app.py"]

