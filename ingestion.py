import pandas as pd
import numpy as np
import uuid
from datetime import datetime, timedelta
import random
from app.db.database import db
from app.services.sentiment import analyze_sentiment, extract_hashtags

# Synthetic Data Config
TOPICS = ["AI", "Crypto", "Politics", "Sports", "Tech", "Climate", "Health", "Movies"]
HASHTAGS = ["#AI", "#Bitcoin", "#Election", "#Football", "#Pixel8", "#GlobalWarming", "#Vaccine", "#Oscar"]
ADJECTIVES = ["amazing", "terrible", "okay", "great", "bad", "wonderful", "horrible", "average"]
VERBS = ["is", "seems", "looks", "feels", "might be"]
NOUNS = ["future", "scam", "mess", "game", "feature", "disaster", "solution", "show"]

def generate_tweet_text():
    # Simple templates to make sentiment vary
    template = random.choice([
        f"{random.choice(TOPICS)} {random.choice(VERBS)} {random.choice(ADJECTIVES)}!",
        f"Just saw the new {random.choice(TOPICS)} update. It {random.choice(VERBS)} {random.choice(ADJECTIVES)}.",
        f"Why is {random.choice(TOPICS)} so {random.choice(ADJECTIVES)}? {random.choice(HASHTAGS)}",
        f"I love {random.choice(TOPICS)}! {random.choice(HASHTAGS)}",
        f"I hate {random.choice(TOPICS)}! {random.choice(HASHTAGS)}"
    ])
    return template

def generate_data(count=500_000):
    print(f"Generating {count} synthetic records...")
    
    # Generate data using numpy/pandas for speed
    # We will generate in chunks to avoid memory issues if needed, but 500k fits in memory easily.
    
    data = []
    # Create simple texts relative to the count
    # This loop might be the bottleneck, so we'll keep the text generation simple.
    
    # Vectorized generation approach
    topics = np.random.choice(TOPICS, count)
    adj = np.random.choice(ADJECTIVES, count)
    tags = np.random.choice(HASHTAGS, count)
    
    # Create DataFrame
    # Optimizing for 500k: Generate sentiment directly since data is synthetic
    print("Generating synthetic sentiment/metadata...")
    sentiment_scores = np.random.uniform(-0.9, 0.9, count)
    sentiment_labels = np.where(sentiment_scores >= 0.05, 'Positive', 
                               np.where(sentiment_scores <= -0.05, 'Negative', 'Neutral'))
    
    df = pd.DataFrame({
        'id': [str(uuid.uuid4()) for _ in range(count)],
        'timestamp': [datetime.now() - timedelta(minutes=random.randint(0, 10000)) for _ in range(count)],
        'text': [f"{t} is {a} {tg}" for t, a, tg in zip(topics, adj, tags)],
        'sentiment_score': sentiment_scores,
        'sentiment_label': sentiment_labels,
        'hashtags': [[t.replace("#", "")] for t in tags] # Simple extraction since we know the structure
    })
    
    return df

def process_and_store(df: pd.DataFrame):
     # Skip slow sentiment analysis since we verified it's pre-calculated
    print("Ingesting into DuckDB...")
    
    # Drop temp column (none to drop now)
    # df = df.drop(columns=['sentiment_res'])
    
    print("Ingesting into DuckDB...")
    conn = db.get_connection()
    # DuckDB can register the dataframe and insert efficiently
    conn.register('df_view', df)
    conn.execute("INSERT INTO posts SELECT id, timestamp, text, sentiment_score, sentiment_label, hashtags FROM df_view")
    conn.unregister('df_view')
    
    count = conn.execute("SELECT count(*) FROM posts").fetchone()[0]
    print(f"Total records in DB: {count}")
    return count

def run_ingestion_pipeline(count=10000):
    # Initialize DB (create tables)
    db.init_db()
    
    # Generate
    df = generate_data(count)
    
    # Process & Store
    total_count = process_and_store(df)
    
    return total_count
