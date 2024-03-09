FROM mcr.microsoft.com/devcontainers/base:jammy
RUN apt-get update && apt-get install -y python3 python3-pip

# Install SQLite 3
RUN apt-get install -y sqlite3

# Set the working directory
WORKDIR /workspace

# Copy the project files to the container
COPY . /app

# Install project dependencies
COPY requirements.txt /tmp/pip-tmp/
RUN pip3 --disable-pip-version-check --no-cache-dir install -r /tmp/pip-tmp/requirements.txt \
    && rm -rf /tmp/pip-tmp
