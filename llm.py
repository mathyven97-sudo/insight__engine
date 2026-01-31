from app.db.database import db
import random

def generate_insights():
    conn = db.get_connection()
    try:
        # Fetch basic stats to ground the insight
        total = conn.execute("SELECT count(*) FROM posts").fetchone()[0]
        neg_count = conn.execute("SELECT count(*) FROM posts WHERE sentiment_label = 'Negative'").fetchone()[0]
        pos_count = conn.execute("SELECT count(*) FROM posts WHERE sentiment_label = 'Positive'").fetchone()[0]
        
        if total == 0:
            return []
            
        neg_pct = (neg_count / total) * 100
        
        # Simulate LLM Logic: Rules-based generation for Mock
        insights = []
        
        if neg_pct > 30:
            insights.append({
                "title": "High Negative Sentiment Detected",
                "description": f"Analysis of {total} posts reveals a concern. {neg_count} posts are negative ({neg_pct:.1f}%). Main keywords involved include 'terrible', 'slow', and 'broken'.",
                "risk": "HIGH",
                "time": "Last 24 Hours"
            })
        else:
            insights.append({
                "title": "Positive Brand Sentiment",
                "description": f"Customers are generally happy. {pos_count} positive posts detected. Trending topics include 'SpaceX' and 'AI'.",
                "risk": "LOW",
                "time": "Last 24 Hours"
            })
            
        return insights
        
    except Exception as e:
        print(f"Error generating insights: {e}")
        return []
