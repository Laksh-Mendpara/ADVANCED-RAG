# Use the official Python image from the Docker Hub
FROM python:3.12-slim

WORKDIR /app

# Copy the poetry lock file and pyproject file first to install dependencies
COPY pyproject.toml poetry.lock ./

# Install poetry
RUN pip install poetry

# Install project dependencies
RUN poetry install --no-dev

COPY . .

CMD ["python", "rag/main.py"]
