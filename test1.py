import tweepy
import pymongo
from decouple import config

API_KEY = config("API_KEY")
API_KEY_SECRET = config("API_KEY_SECRET")
ACCESS_TOKEN = config("ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = config("ACCESS_TOKEN_SECRET") 
# Set up your Twitter API credentials
consumer_key = API_KEY
consumer_secret = API_KEY_SECRET
access_token = ACCESS_TOKEN
access_token_secret = ACCESS_TOKEN_SECRET


# Set up your MongoDB connection
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["twitter"]
collection = db["tweets"]

# Set up your Tweepy API connection
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# Define your query
query = {
    "WhiteHatJr_Tweets": ["@whitehatjunior", "#whitehatjunior", "#whitehatjr"],
    "Vedantu_Tweets": ["@vedantu_learn", "@VedantuCare", "#vedantu", "#vedantuscam", "#vedantufraud", "#boycottvedantu"],
    "BYJUS_Tweets": ["@ByjusSupport", "@BYJU", "#byju", "#byjus", "#byjusscam"],
    "Cuemath_Tweets": ["@Cuemath", "@CuemathPune", "#cuemath", "#CuemathMethod", "#CuemathFest", "#cuemathistheplace"]
}

# Loop through each query
for query_name, query_terms in query.items():
    # Loop through each term in the query
    for term in query_terms:
        # Search for tweets containing the term
        tweets = tweepy.Cursor(api.search_tweets,
                               q=term,
                               tweet_mode='extended',
                               lang='en',
                               result_type='recent').items(100)

        # Loop through each tweet and add it to the database if it doesn't already exist
        for tweet in tweets:
            tweet_dict = tweet._json
            if collection.find_one({"id": tweet_dict["id"]}) is None:
                tweet_dict["query_name"] = query_name
                collection.insert_one(tweet_dict)
