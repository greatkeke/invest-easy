# Build stage
FROM ghcr.io/astral-sh/uv:python3.12-alpine as builder

WORKDIR /install
COPY pyproject.toml uv.lock .
RUN apk add --no-cache --virtual .build-deps gcc musl-dev \
    && uv sync --frozen --no-cache \
    && apk del .build-deps

# Runtime stage
FROM python:3.12.11-alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PATH="/usr/local/bin:$PATH"

WORKDIR /invest-easy-webapi

# Copy installed packages to Python's standard location
COPY --from=builder /install /usr/local

# Copy application code to working directory
COPY ./app ./app
COPY main.py .

# Create volumes
VOLUME /invest-easy-webapi/db
VOLUME /invest-easy-webapi/env
VOLUME /invest-easy-webapi/logs

EXPOSE 10008

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:10008/health || exit 1

CMD ["uv run uvicorn", "app.app:app", "--host", "0.0.0.0", "--port", "10008"]
