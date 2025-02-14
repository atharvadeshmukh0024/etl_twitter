import tweepy
import psycopg2
from datetime import datetime

# Twitter API credentials (replace with your valid credentials)
BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAAIT%2FzAEAAAAAw8zPuqc4eE8FgvSOl5NqwZVglbQ%3DQ6gSOjtjv8TOnsL109FlMyRMGjPrTh8CvmjlGYzg648B1N37QK"  # Update with your actual Bearer Token

# Connect to PostgreSQL
conn = psycopg2.connect(
    dbname="twitter_etl",
    user="postgres",
    password="admin",
    host="localhost",
    port="5432"
)
cur = conn.cursor()

# Authenticate Twitter API
client = tweepy.Client(bearer_token=BEARER_TOKEN)

# Get user ID (Elon Musk)
user = client.get_user(username="elonmusk", user_fields=["id"])
user_id = user.data.id

# Fetch the latest 10 tweets with necessary fields
tweets = client.get_users_tweets(id=user_id, max_results=10, tweet_fields=["public_metrics", "created_at"])

# Check if tweets are available
if tweets.data:
    for tweet in tweets.data:
        # Insert tweet data into the PostgreSQL table
        cur.execute(
            """
            INSERT INTO tweets (tweet_id, username, text, created_at, favorite_count, retweet_count)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT (tweet_id) DO NOTHING;
            """,
            (
                tweet.id,  # tweet_id
                "elonmusk",  # username
                tweet.text,  # tweet text
                tweet.created_at,  # created_at
                tweet.public_metrics["like_count"] if tweet.public_metrics else 0,  # favorite_count
                tweet.public_metrics["retweet_count"] if tweet.public_metrics else 0  # retweet_count
            )
        )

# Commit and close connection
conn.commit()
cur.close()
conn.close()

print("Tweets inserted successfully!")
