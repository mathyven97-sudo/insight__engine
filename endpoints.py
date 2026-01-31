from fastapi import APIRouter

router = APIRouter()

from app.services.ingestion import run_ingestion_pipeline
from app.db.database import db

@router.get("/health")
def health_check():
    return {"status": "ok"}

@router.post("/ingest")
def ingest_data():
    # Trigger ingestion
    # optimized for 500k
    count = run_ingestion_pipeline(count=500000) 
    return {"status": "success", "count": count}

@router.get("/stats")
def get_stats():
    conn = db.get_connection()
    try:
        total = conn.execute("SELECT count(*) FROM posts").fetchone()[0]
        
        # Get sentiment distribution
        sentiment_counts = conn.execute("SELECT sentiment_label, COUNT(*) FROM posts GROUP BY sentiment_label").fetchall()
        sentiment_dist = {row[0]: row[1] for row in sentiment_counts}
        
    except:
        total = 0
        sentiment_dist = {}
        
    return {
        "total_posts": total,
        "sentiment_distribution": sentiment_dist
    }

from app.services.llm import generate_insights

@router.get("/insights")
def get_insights():
    return generate_insights()


