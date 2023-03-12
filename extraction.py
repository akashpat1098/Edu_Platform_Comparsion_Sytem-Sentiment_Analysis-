'''It fetches tweets from Twitter API and saved it to database.
It saves actual tweets, there users & cleaned tweets also
& converting it into different csv file'''

import pymongo
import tweepy
from decouple import config
from pprint import pprint
import re
import csv

def connectToTwitter():
    """To Authorize the connection with Twitter API"""
    API_KEY = config("API_KEY")
    API_KEY_SECRET = config("API_KEY_SECRET")
    ACCESS_TOKEN = config("ACCESS_TOKEN")
    ACCESS_TOKEN_SECRET = config("ACCESS_TOKEN_SECRET") 

    auth = tweepy.OAuthHandler(API_KEY,API_KEY_SECRET)
    auth.set_access_token(ACCESS_TOKEN,ACCESS_TOKEN_SECRET)

    api=tweepy.API(auth)
    return api

def extract_tweets(api,query, count = 10):
    '''
    Main function to fetch tweets and store it in dict then in list.
    '''
    # empty list to store parsed tweets
    tweets = []
    # call twitter api to fetch tweets
    fetched_tweets=tweepy.Cursor(method=api.search_tweets,q=query,tweet_mode="extended",lang="en").items(count)

    # parsing tweets one by one
    for tweet in fetched_tweets:
        # empty dictionary to store required params of a tweet
        parsed_tweet = {}

        # saving text of tweet
        parsed_tweet['tweet'] = tweet.full_text
        parsed_tweet['user'] = tweet.user.screen_name
        parsed_tweet['cleanedTweet'] = clean_tweet(tweet.full_text)


        # appending parsed tweet to tweets list
        if tweet.retweet_count > 0:
            # if tweet has retweets, ensure that it is appended only once
            if parsed_tweet not in tweets:
                tweets.append(parsed_tweet)
        else:
            tweets.append(parsed_tweet)

    # return parsed tweets
    return tweets

def clean_tweet(tweet):
    '''
    Utility function to clean tweet text by removing links, special characters
    using simple regex statements.
    '''
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())


def storeInDB(data,collection_name):
    """connecting to localdatabase and extract tweets from database and compare it with tweets extracted from twitter and avoid insertion of duplicate tweet"""
    client=pymongo.MongoClient()
    db=client["Sentimental_Tweets"]
    collection=db[collection_name]
    tweets=list(collection.find({},{"_id":0,"sentiment":0}))
    # loop for checking Duplicate entry
    for tweet in data:
        if tweet not in tweets:
            tweet_ids=collection.insert_one(tweet).inserted_id
            print(f"Tweet with id {tweet_ids} has been inserted\n")
        else:
            print(f"|{tweet['tweet']}| is a dublicate entry\n")

def dataToCSV(collection_name):
    # Connect to MongoDB
    client = pymongo.MongoClient()
    db = client['Sentimental_Tweets']
    collection=db[collection_name]
    cursor = collection.find()
    data = [(doc['_id'], doc['tweet'], doc['user'], doc['cleanedTweet']) for doc in cursor]
    
    # Save data to CSV file
    with open(f'{collection_name}.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['_id', 'tweet', 'user', 'cleanedTweet'])
        writer.writerows(data)

if __name__=="__main__":
    query={"WhiteHatJr_Tweets":["@whitehatjunior","#whitehatjunior","#whitehatjr"],
    "Vedantu_Tweets":["@vedantu_learn","@VedantuCare","#vedantu","#vedantuscam","#vedantufraud","#boycottvedantu"],
    "BYJUS_Tweets":["@ByjusSupport","@BYJU","#byju","#byjus","#byjusscam"],
    "Cuemath_Tweets":["@Cuemath","@CuemathPune","#cuemath","#CuemathMethod","#CuemathFest","#cuemathistheplace"]}
    
    api=connectToTwitter()
    for collection in query:
        for hastag in query[collection]:
            keywords=hastag
            collection_name=collection
            limit=15
            tweets_list=extract_tweets(api,keywords,limit)
            storeInDB(tweets_list,collection_name)
            dataToCSV(collection)



    

    

    

