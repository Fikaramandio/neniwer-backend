from fastapi import FastAPI
import os
import logging
from typing import Dict, Any
from dotenv import load_dotenv

load_dotenv()

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Neniwer v3.0 API",
    description="Early Warning System for Bener Meriah",
    version="3.0.0"
)

@app.get("/")
async def root() -> Dict[str, Any]:
    return {
        "message": "🚀 Neniwer v3.0 API is LIVE!",
        "status": "operational",
        "version": "3.0.0"
    }

@app.get("/health")
async def health_check() -> Dict[str, Any]:
    return {
        "status": "healthy",
        "timestamp": "2024-01-01T00:00:00Z",
        "services": ["api", "database", "ai"]
    }

@app.get("/config")
async def config_check() -> Dict[str, Any]:
    """Check environment configuration"""
    config_status = {
        "supabase": "✅ READY" if os.getenv("SUPABASE_URL") else "❌ MISSING",
        "database": "✅ READY" if os.getenv("DATABASE_URL") else "❌ MISSING",
        "ai_service": "✅ READY" if os.getenv("HUGGINGFACE_TOKEN") else "❌ MISSING",
        "environment": os.getenv("RAILWAY_ENVIRONMENT", "development")
    }
    
    logger.info(f"Config check: {config_status}")
    return config_status

@app.get("/test/database")
async def test_database() -> Dict[str, Any]:
    """Test database connection"""
    try:
        import psycopg2
        db_url = os.getenv("DATABASE_URL")
        if db_url:
            connection = psycopg2.connect(db_url)
            connection.close()
            return {"database": "✅ CONNECTED", "status": "success"}
        else:
            return {"database": "❌ NOT CONFIGURED", "status": "error"}
    except ImportError:
        return {"database": "❌ PSYCOPG2 NOT INSTALLED", "status": "error"}
    except Exception as e:
        return {"database": f"❌ CONNECTION FAILED: {str(e)}", "status": "error"}

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
