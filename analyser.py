import pymongo
import re
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from scipy.special import softmax
from pprint import pprint
import numpy as np
import nltk
# nltk.download('vader_lexicon')
from nltk.sentiment import SentimentIntensityAnalyzer


model_path = "sentiment_model"
tokenizer_path = "tokenizer"

model = AutoModelForSequenceClassification.from_pretrained(model_path)
tokenizer = AutoTokenizer.from_pretrained(tokenizer_path)

labels = ['Negative', 'Neutral', 'Positive']


def clean_tweet(tweet):
    '''
    Utility function to clean tweet text by removing links, special characters
    using simple regex statements.
    '''
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())



def get_tweet_sentiment(text, model=model, tokenizer=tokenizer, labels=labels):
    encoded_input = tokenizer.encode_plus(text, return_tensors='pt')
    output = model(**encoded_input)
    scores = output[0][0].detach().numpy()
    scores = np.exp(scores) / np.exp(scores).sum(-1, keepdims=True)
    
    ranking = np.argsort(scores)
    ranking = ranking[::-1]
    return labels[ranking[0]]

def get_sentiment_using_nltk(text):
    sid = SentimentIntensityAnalyzer()
    sentiment_scores = sid.polarity_scores(text)
    if sentiment_scores['pos'] > sentiment_scores['neg']:
        return 'Positive'
    elif sentiment_scores['neg'] > sentiment_scores['pos']:
        return 'Negative'
    else:
        return 'Neutral'
    

import openai
from decouple import config
# Set up your OpenAI API key
OPENAI_APIKEY = config("OPENAI_APIKEY") 
openai.api_key = OPENAI_APIKEY
# sentiment using OPENAI
def get_sentiment(text):
    # Set the model and parameters
    model_engine = "text-davinci-002"
    prompt = f"Sentiment analysis for the following text: {text}."
    temperature = 0.5
    max_tokens = 5  # Reduced max_tokens for faster response

    # Call the OpenAI API to generate the sentiment
    output = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        temperature=temperature,
        max_tokens=max_tokens
    )

    # Extract the sentiment from the OpenAI API response
    sentiment = output.choices[0].text.strip()

    # Map sentiment to one of three categories
    if sentiment == "Positive":
        return "positive"
    elif sentiment == "Negative":
        return "negative"
    else:
        return "neutral"

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


import time
if __name__=="__main__":
    collection_list=["WhiteHatJr_Tweets","Vedantu_Tweets","BYJUS_Tweets","Cuemath_Tweets"]
    # collection_list=["Cuemath_Tweets"]
    for collection_name in collection_list:
        tweets=getData(collection_name) #it is cursor iterator
        for tweet in tweets: 
            sentiment=get_sentiment_using_nltk(tweet["cleanedTweet"])
            updateData(collection_name,sentiment,tweet["_id"])
   

