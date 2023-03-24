import pymongo
import re
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from scipy.special import softmax
from pprint import pprint
import numpy as np
import nltk
# nltk.download('vader_lexicon')
from nltk.sentiment import SentimentIntensityAnalyzer
import csv
import SentimentalModals



def getData(collection_name):
    """connecting to localdatabase and extracting data from same and returns tweets as Cursor iterator"""
    client=pymongo.MongoClient()
    db=client["Sentimental_Tweets"]
    collection=db[collection_name]
    tweets=collection.find({},{"sentiment":0})
    print(f"Getting data from {collection_name} is done")
    return list(tweets)


def updateData(collection_name,sentiment,tweet_id):
    """connecting to localdatabase and updating the sentiments of tweets on basis of _id"""
    client=pymongo.MongoClient()
    db=client["Sentimental_Tweets"]
    collection=db[collection_name]
    collection.update_one({"_id":tweet_id},{"$set":{"sentiment":sentiment}},upsert=False,array_filters=None)   

def dataToCSV(collection_name):
    # Connect to MongoDB
    client = pymongo.MongoClient()
    db = client['Sentimental_Tweets']
    collection=db[collection_name]
    cursor = collection.find()
    data = [(doc['user'],doc['cleanedTweet'],doc['sentiment']) for doc in cursor]
    
    # Save data to CSV file
    with open(f'{collection_name}.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['user', 'cleanedTweet','sentiment'])
        writer.writerows(data)

def main_analyser(userList):
    # userList = ['WhiteHatJr_Tweets','Vedantu_Tweets']
    for collection_name in userList:
        tweets=getData(collection_name) #it is cursor iterator
        for tweet in tweets: 
            sentiment=SentimentalModals.get_sentiment_using_nltk(tweet["cleanedTweet"])
            updateData(collection_name,sentiment,tweet["_id"])
        dataToCSV(collection_name)


if __name__=="__main__":
    userList=["WhiteHatJr_Tweets","Vedantu_Tweets","BYJUS_Tweets","Cuemath_Tweets"]
    # userList = ['WhiteHatJr_Tweets','Vedantu_Tweets']
    for collection_name in userList:
        tweets=getData(collection_name) #it is cursor iterator
        for tweet in tweets: 
            sentiment=SentimentalModals.get_sentiment_using_nltk(tweet["cleanedTweet"])
            updateData(collection_name,sentiment,tweet["_id"])
        dataToCSV(collection_name)

