FROM alpine:3

LABEL maintainer="@jay_townsend1 & @NotoriousRebel1"

# Install dependencies
RUN apk update && apk upgrade --available && apk add --no-cache \
    musl-dev \
    git \
    libffi-dev \
    gcc \
    python3-dev \
    py3-pip \
    libxml2-dev \
    libxslt-dev \
    bash

# Install playwright dependencies
RUN apk add --no-cache \
    nss \
    chromium \
    harfbuzz \
    ca-certificates \
    ttf-freefont

# Create necessary directories
RUN mkdir -p /root/.local/share/theHarvester/static/

# Create a virtual environment
RUN python3 -m venv /opt/venv

# Activate the virtual environment (in the current RUN command, it will be deactivated afterwards)
ENV PATH="/opt/venv/bin:$PATH"

# ... (rest of the Dockerfile remains the same)

# Copy the requirements.txt file
COPY requirements.txt /tmp/requirements.txt

# Copy the requirements/base.txt file
COPY requirements/base.txt /tmp/requirements/base.txt

# Install packages within the virtual environment
RUN pip install --no-cache-dir -r /tmp/requirements.txt && \
    pip install playwright==1.49.1 && \
    playwright install

# ... (rest of the Dockerfile remains the same)

# Remove the requirements.txt file
RUN rm /tmp/requirements.txt

# Install theHarvester
RUN pip install --no-cache-dir git+https://github.com/laramies/theHarvester.git

# Set the entrypoint
ENTRYPOINT ["theHarvester"]
