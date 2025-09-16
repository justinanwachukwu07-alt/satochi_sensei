# Satoshi Sensei Backend

AI-powered Bitcoin/Stacks DeFi copilot backend implementation.

## Architecture

- **FastAPI** - High-performance Python web framework
- **PostgreSQL** - Primary database for user data and recommendations
- **Redis** - Real-time caching and session management
- **Groq API** - Low-latency LLM inference for strategy reasoning
- **Stacks/Bitcoin Nodes** - Blockchain data integration

## Quick Start

1. Install dependencies: `pip install -r requirements.txt`
2. Set up environment variables in `.env`
3. Run database migrations: `alembic upgrade head`
4. Start the server: `uvicorn main:app --reload`

## API Documentation

Once running, visit `http://localhost:8000/docs` for interactive API documentation.
