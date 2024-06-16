# Use an official Python runtime as a parent image
FROM python:3.12

# Set environment varibles
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /code/

# Install Poetry
RUN pip install poetry

# Copy only the pyproject.toml and poetry.lock files to the working directory
COPY pyproject.toml poetry.lock /code/

# Install dependencies
RUN poetry install --no-root

# Copy the rest of the application files
COPY . /code/

# Set environment variables (if needed)
ENV PATH="/root/.poetry/bin:$PATH"

# Expose the port the app runs on
EXPOSE 8000