FROM python:3.12

# Set environment varibles
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /code/

RUN pip install poetry

# Copy only the pyproject.toml and poetry.lock files to the working directory
COPY pyproject.toml poetry.lock /code/

RUN poetry install --no-root

# Copy the rest of the application files
COPY . /code/

ENV PATH="/root/.poetry/bin:$PATH"

# Expose the port the app runs on
EXPOSE 8000