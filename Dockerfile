# Use the lightweight Alpine base image
FROM python:3.11-alpine

# Set the working directory in the container
WORKDIR /app

# Install build dependencies
RUN apk add --no-cache build-base libffi-dev

# Install Poetry
RUN pip install --no-cache-dir poetry
RUN poetry config virtualenvs.create false

# Copy the necessary files into the container
COPY pyproject.toml poetry.lock /app/

# Install dependencies
RUN poetry install --without dev

# Copy the rest of the files into the container
COPY . /app/

# Expose the port on which the Flask application runs
EXPOSE 8000

# Command to run the Flask application
CMD ["poetry", "run", "gunicorn", "--bind", "0.0.0.0:8000", "-w", "4", "app:create_app()"]
