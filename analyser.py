import pymongo
import re
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from scipy.special import softmax
from pprint import pprint
def clean_tweet(tweet):
    '''
    Utility function to clean tweet text by removing links, special characters
    using simple regex statements.
    '''
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())



def get_tweet_sentiment(tweet):
     # load model and tokenizer
    roberta = "cardiffnlp/twitter-roberta-base-sentiment"
    # parsing the model
    model = AutoModelForSequenceClassification.from_pretrained(roberta)
    # tokenizer for encoding of data 
    tokenizer = AutoTokenizer.from_pretrained(roberta)

    labels = ['Negative', 'Neutral', 'Positive']
    encoded_tweet = tokenizer(tweet, return_tensors='pt')
    # sentiment analysis
    # giving data to model for calculating sentiment
    output = model(**encoded_tweet)
    # getting scores of sentiment from output
    scores = output[0][0].detach().numpy()
    # converting scores into probablity
    scores = list(softmax(scores))
    # for checking what sentiment is 
    max_score=max(scores)
    max_index=scores.index(max_score)
    return labels[max_index]

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

if __name__=="__main__":
    # collection_list=["WhiteHatJr_Tweets","Vedantu_Tweets","BYJUS_Tweets","Cuemath_Tweets"]
    collection_list=["Cuemath_Tweets"]
    for collection_name in collection_list:
        tweets=getData(collection_name) #it is cursor iterator
        for tweet in tweets: 
            sentiment=get_tweet_sentiment(tweet["cleanedTweet"])
            updateData(collection_name,sentiment,tweet["_id"])