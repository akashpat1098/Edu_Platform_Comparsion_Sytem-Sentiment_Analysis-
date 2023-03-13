#########  Sentiment using pre-trained model of robertai.e hugging face
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import numpy as np
model_path = "sentiment_model"
tokenizer_path = "tokenizer"
model = AutoModelForSequenceClassification.from_pretrained(model_path)
tokenizer = AutoTokenizer.from_pretrained(tokenizer_path)
labels = ['Negative', 'Neutral', 'Positive']
def get_tweet_sentiment(text, model=model, tokenizer=tokenizer, labels=labels):
    encoded_input = tokenizer.encode_plus(text, return_tensors='pt')
    output = model(**encoded_input)
    scores = output[0][0].detach().numpy()
    scores = np.exp(scores) / np.exp(scores).sum(-1, keepdims=True)
    
    ranking = np.argsort(scores)
    ranking = ranking[::-1]
    return labels[ranking[0]]
print(get_tweet_sentiment("I do not hate you"))





################ Sentiment using nltk
import nltk
# nltk.download('vader_lexicon')
from nltk.sentiment import SentimentIntensityAnalyzer
def get_sentiment_using_nltk(text):
    sid = SentimentIntensityAnalyzer()
    sentiment_scores = sid.polarity_scores(text)
    if sentiment_scores['pos'] > sentiment_scores['neg']:
        return 'Positive'
    elif sentiment_scores['neg'] > sentiment_scores['pos']:
        return 'Negative'
    else:
        return 'Neutral'
print(get_sentiment_using_nltk("I do not hate you"))




############### Set up your OpenAI API key
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

print(get_sentiment("I do not hate you"))

