# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.12-slim

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Set WORKDIR
WORKDIR /app
COPY . /app

# Install git and curl
RUN apt-get update && apt-get install -y git curl
RUN echo "path is $PATH"
RUN echo "home is $HOME"

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python -

# Correct the PATH to include the directory where Poetry is installed
ENV PATH="/root/.local/bin:$PATH"

# Install git and curl
RUN apt-get update && apt-get install -y git curl
RUN echo "path after poetry is $PATH"
RUN echo "home after poetry is $HOME"

# Disable the creation of virtual environments by Poetry
RUN poetry config virtualenvs.create false

# Install dependencies with Poetry
RUN poetry install --no-dev


# Append poetry to the PATH directly in the Dockerfile to ensure it's available globally
ENV PATH="/root/.poetry/bin:$PATH"

# Disable the creation of virtual environments by Poetry
RUN poetry config virtualenvs.create false

# Install dependencies with Poetry
RUN poetry install --no-dev

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
RUN adduser --uid 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser

EXPOSE 80

ENV DOCKER_FLAG=1

CMD ["python", "stoli_bot/main.py"]
