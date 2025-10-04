# Pigeonhole Streaming

Streaming website with Firestick support.

## Setup

1. Clone your repository here:
   ```bash
   git clone <your-repo-url> .
   ```

2. Set up environment (adjust based on your stack):

   **If Python/Django/Flask:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

   **If Node.js/React/Vue:**
   ```bash
   npm install
   ```

3. Configure environment variables:
   ```bash
   cp .env.example .env
   vim .env
   ```

4. Run development server

## Firestick Integration

Use ADB tools to deploy to Firestick devices:

```bash
# Connect to Firestick
adb connect <firestick-ip>:5555

# List connected devices
adb devices

# Install app
adb install your-app.apk

# Debug logs
adb logcat
```

## Docker Deployment

If using Docker:

```bash
docker-compose up -d
```

## Services

- Web server: Nginx (configured at /etc/nginx/)
- Database: PostgreSQL or as needed
- Cache: Redis
