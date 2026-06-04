# FutuOpenD Protocol Encryption Setup Guide

This guide explains how to enable and configure protocol encryption for FutuOpenD API communications.

## Overview

FutuOpenD now supports protocol-level encryption using RSA keys. This provides an additional layer of security for API communications between the client and the FutuOpenD server.

## Prerequisites

1. FutuOpenD server that supports encryption (check with your provider)
2. RSA private key file (`rsa_private_key.pem`)
3. For Docker: A `certs` directory to store the key file

## Configuration

### Step 1: Prepare Your RSA Private Key

Obtain your RSA private key file from your FutuOpenD provider. The file should be in PEM format:
- Filename: `rsa_private_key.pem`
- Ref: https://openapi.futunn.com/futu-api-doc/ftapi/init.html#319

### Step 2: Configure Environment Variables

Edit your `.env` file (or create one from `.env.example`):

```env
# Enable FutuOpenD protocol encryption
ENABLE_PROTO_ENCRYPT=true

# Path to RSA private key file
# Local: C:\path\to\rsa_private_key.pem (Windows) or /path/to/rsa_private_key.pem (Unix)
# Docker: /invest-easy-webapi/certs/rsa_private_key.pem
RSA_FILE_PATH=/path/to/your/rsa_private_key.pem
```

### Step 3: Running Without Docker (Local Development)

1. Place your `rsa_private_key.pem` file in a known location
2. Set the `RSA_FILE_PATH` environment variable to the absolute path:

```bash
# Linux/macOS
export RSA_FILE_PATH=/home/user/certs/rsa_private_key.pem

# Windows (PowerShell)
$env:RSA_FILE_PATH = "C:\certs\rsa_private_key.pem"

# Windows (Command Prompt)
set RSA_FILE_PATH=C:\certs\rsa_private_key.pem
```

Then start the application normally:

```bash
python -m uvicorn app.app:app --host 0.0.0.0 --port 10008
```

### Step 4: Running With Docker

#### Option A: Using docker-compose (Recommended)

1. Create a `certs` directory in your project root:
```bash
mkdir certs
```

2. Copy your `rsa_private_key.pem` file to the certs directory:
```bash
cp /path/to/rsa_private_key.pem ./certs/
```

3. Create a `.env` file from `.env.example`:
```bash
cp .env.example env/.env
```

4. Edit `env/.env` and set:
```env
ENABLE_PROTO_ENCRYPT=true
RSA_FILE_PATH=/invest-easy-webapi/certs/rsa_private_key.pem
```

5. Start the container:
```bash
docker-compose -f docker-compose.example.yml up -d
```

#### Option B: Using Docker CLI

```bash
docker run -d \
  --name invest-easy-webapi \
  -p 10008:10008 \
  -e ENABLE_PROTO_ENCRYPT=true \
  -e RSA_FILE_PATH=/invest-easy-webapi/certs/rsa_private_key.pem \
  -v $(pwd)/certs:/invest-easy-webapi/certs:ro \
  -v $(pwd)/db:/invest-easy-webapi/db \
  -v $(pwd)/logs:/invest-easy-webapi/logs \
  invest-easy-webapi:latest
```

## Verification

### Check Logs

Look for the encryption initialization message in the application logs:

```
INFO:     FutuOpenD encryption enabled with RSA key: /invest-easy-webapi/certs/rsa_private_key.pem
```

### Health Check

The application provides a health check endpoint that returns status information:

```bash
curl http://localhost:10008/
# Should return: {"health": "ok"}
```

## Troubleshooting

### Error: "Failed to initialize FutuOpenD encryption"

**Possible causes:**
1. RSA key file not found at the specified path
2. RSA key file format is incorrect
3. Permission issues reading the file

**Solution:**
- Verify the file path is correct
- Ensure the file is readable (check permissions)
- Verify the file is in valid PEM format

### Error: "FutuOpenD encryption enabled but RSA file path not provided"

**Cause:** `ENABLE_PROTO_ENCRYPT=true` but `RSA_FILE_PATH` is not set

**Solution:** 
- Set the `RSA_FILE_PATH` environment variable before starting the application

### Docker Volume Mount Issues

**Problem:** Docker can't find the certs volume

**Solution:**
- Verify the `certs` directory exists on the host machine
- Check that the path in the docker-compose file is correct
- Ensure you're using absolute paths or paths relative to where docker-compose is run

## Security Considerations

1. **Key Storage:** Keep your RSA private key file secure
   - Store it outside of the repository (not in .git)
   - Use appropriate file permissions (e.g., `chmod 600` on Unix)
   - In Docker, mount it as read-only (`:ro`)

2. **Environment Variables:** Avoid storing sensitive information in version control
   - Use `.env` files (add `.env` to `.gitignore`)
   - Use `.env.example` as a template with empty values

3. **Network Security:** Encryption is for application-layer security
   - Consider using TLS/HTTPS for additional transport-layer security
   - Use secure networks when possible

## Related Configuration

See `config.py` for all available configuration options:
- `ENABLE_PROTO_ENCRYPT`: Enable/disable encryption (boolean)
- `RSA_FILE_PATH`: Path to RSA private key file (string)
- `FUTU_OPEND_HOST`: FutuOpenD server host
- `FUTU_OPEND_PORT`: FutuOpenD server port

## Need Help?

- Check the application logs: `./logs/app.log`
- Review FutuOpenD documentation for more details on encryption
- Verify your RSA key file is compatible with the version of FutuOpenD you're using
