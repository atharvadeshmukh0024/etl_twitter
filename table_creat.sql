CREATE TABLE tweets (
    tweet_id BIGINT PRIMARY KEY,
    username VARCHAR(50),
    text TEXT,
    created_at TIMESTAMP,
    favorite_count INTEGER,
    retweet_count INTEGER
);
