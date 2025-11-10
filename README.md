# Smart Energy Monitoring Backend

IoT-Enabled Smart Energy Monitoring System with Real-Time Analytics and AI-Powered Predictions.

## Quick Start

### Prerequisites
- Docker & Docker Compose
- Python 3.11+ (for local development)

### Setup

1. Extract the ZIP file
2. Create environment file: `cp .env.example .env`
3. Start services: `docker-compose up`
4. Access API at http://localhost:8000/docs

## Project Structure

- `app/` - FastAPI application
- `ml/` - Machine learning models
- `tests/` - Test suite (pytest)
- `docker/` - Docker configuration

## Development

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements-dev.txt
pytest tests/ -v --cov=app
```

## Next Steps

1. Implement data generator
2. Create REST API routes
3. Set up WebSocket handlers
4. Train LSTM model
