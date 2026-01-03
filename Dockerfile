FROM python:3.12-slim

ENV DEBIAN_FRONTEND=noninteractive

RUN ls
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    git \
    build-essential \
    libgl1 \
    libglu1-mesa \
    libxrender1 \
    libxcursor1 \
    libxrandr2 \
    libxinerama1 \
    libxi6 \
    libxext6 \
    libsm6 \
    libice6 \
    libxfixes3 \
    libxft2 \
    && rm -rf /var/lib/apt/lists/*


WORKDIR /app
ENV VIRTUAL_ENV=/opt/venv
ENV PATH="/opt/venv/bin:$PATH"
ENV UV_PROJECT_ENVIRONMENT=/opt/venv


COPY pyproject.toml uv.lock ./
RUN pip install --no-cache-dir uv \
    && uv venv /opt/venv \
    && uv sync --frozen
COPY . .