FROM jenkins/jenkins:lts-jdk17

# Define build-time argument for Docker group ID
   ARG DOCKER_GID=20

# Switch to root to install Docker CLI and Docker Compose
USER root

# Update and install Docker CLI
RUN apt-get update && apt-get install -y \
    docker.io && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Install Docker Compose
RUN curl -L "https://github.com/docker/compose/releases/download/v2.20.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose && \
    chmod +x /usr/local/bin/docker-compose

# Set environment variable to ensure Docker CLI can connect to Docker daemon
ENV DOCKER_HOST=tcp://docker:2375

# Switch back to Jenkins user
USER jenkins

# Verify Docker installations (optional)
RUN docker --version && docker-compose --version