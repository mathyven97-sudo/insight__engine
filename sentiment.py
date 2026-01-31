from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import re

analyzer = SentimentIntensityAnalyzer()

def analyze_sentiment(text: str) -> dict:
    vs = analyzer.polarity_scores(text)
    compound = vs['compound']
    
    if compound >= 0.05:
        label = 'Positive'
    elif compound <= -0.05:
        label = 'Negative'
    else:
        label = 'Neutral'
        
    return {
        "score": compound,
        "label": label
    }

def extract_hashtags(text: str) -> list:
    return re.findall(r"#(\w+)", text)
