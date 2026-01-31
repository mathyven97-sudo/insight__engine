import duckdb
from app.core.config import settings

class Database:
    def __init__(self):
        self.conn = None

    def get_connection(self):
        if self.conn is None:
            self.conn = duckdb.connect(settings.DATABASE_PATH)
        return self.conn
    
    def init_db(self):
        conn = self.get_connection()
        # Create Main Table
        conn.execute("""
            CREATE TABLE IF NOT EXISTS posts (
                id VARCHAR PRIMARY KEY,
                timestamp TIMESTAMP,
                text VARCHAR,
                sentiment_score FLOAT,
                sentiment_label VARCHAR,
                hashtags VARCHAR[]
            )
        """)
        
        # Create Aggregation Views (Speed up dashboard)
        conn.execute("""
            CREATE OR REPLACE VIEW hourly_sentiment AS
            SELECT 
                time_bucket(INTERVAL '1 hour', timestamp) as bucket,
                sentiment_label,
                COUNT(*) as count
            FROM posts
            GROUP BY bucket, sentiment_label
        """)

db = Database()
