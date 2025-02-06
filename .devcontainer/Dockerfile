FROM mcr.microsoft.com/devcontainers/python:1-3.13-bullseye

# Install Docker CLI
RUN curl -fsSL https://get.docker.com | sh

# Install additional OS packages
RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install --no-install-recommends \
        postgresql-client \
        docker-compose \
    && apt-get clean -y && rm -rf /var/lib/apt/lists/*

# Add MongoDB public key and repository, then install mongosh
RUN curl -fsSL https://www.mongodb.org/static/pgp/server-8.0.asc | apt-key add - \
    && echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu noble/mongodb-org/8.0 multiverse" | tee /etc/apt/sources.list.d/mongodb-org-8.0.list \
    && apt-get update \
    && apt-get install -y mongodb-mongosh \
    && mongosh --version

# Setup Docker permissions - improved version
RUN groupadd -f docker \
    && usermod -aG docker vscode \
    && echo '#!/bin/sh\n\
if [ -e /var/run/docker.sock ]; then\n\
    sudo chown root:docker /var/run/docker.sock\n\
    sudo chmod 666 /var/run/docker.sock\n\
fi' > /usr/local/share/docker-init.sh \
    && chmod +x /usr/local/share/docker-init.sh

# Add docker-init.sh to bash and zsh rc files
RUN echo ". /usr/local/share/docker-init.sh" >> /home/vscode/.bashrc \
    && echo ". /usr/local/share/docker-init.sh" >> /home/vscode/.zshrc
