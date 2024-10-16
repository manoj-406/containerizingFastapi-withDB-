# Use the official Python image as the base image
FROM python:3.11

# Set the working directory to /app
WORKDIR /app

ENV DATABASE_URL=postgresql://user:password@localhost:5432/movieshop

# Copy the requirements file into the container
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copy the FastAPI application code into the container
COPY . .

# Expose the port that the FastAPI application will run on
EXPOSE 8000


# Set the command to start the FastAPI application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]