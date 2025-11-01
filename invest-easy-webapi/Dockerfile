FROM python:3.12.11-alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PATH="/usr/local/bin:$PATH"

# Install uv.
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Copy the application into the container.
COPY . /app

# Install the application dependencies.
WORKDIR /app
RUN uv sync --frozen --no-cache

# Create volumes
VOLUME /invest-easy-webapi/db
VOLUME /invest-easy-webapi/env
VOLUME /invest-easy-webapi/logs

EXPOSE 10008

# Run the application.
CMD ["/app/.venv/bin/fastapi", "run", "app/app.py", "--port", "10008", "--host", "0.0.0.0"]