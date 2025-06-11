# Build stage
FROM python:3.13.2-alpine as builder

WORKDIR /install
COPY requirements.txt .
RUN apk add --no-cache --virtual .build-deps gcc musl-dev \
    && pip install --prefix=/install --no-cache-dir --no-warn-script-location -r requirements.txt \
    && apk del .build-deps

# Runtime stage
FROM python:3.13.2-alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PATH="/usr/local/bin:$PATH"

WORKDIR /invest-easy-webapi

# Copy installed packages to Python's standard location
COPY --from=builder /install /usr/local

# Copy application code to working directory
COPY ./app ./app
COPY ./db ./db
COPY main.py .

# Create volumes
VOLUME /invest-easy-webapi/db
VOLUME /invest-easy-webapi/env

EXPOSE 10008

CMD ["uvicorn", "app.app:app", "--host", "0.0.0.0", "--port", "10008"]
