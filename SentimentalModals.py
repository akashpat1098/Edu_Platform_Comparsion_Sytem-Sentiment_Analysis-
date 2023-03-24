import time

#########  Sentiment using pre-trained model of roberta i.e hugging face
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import numpy as np
model_path = "sentiment_model"
tokenizer_path = "tokenizer"
model = AutoModelForSequenceClassification.from_pretrained(model_path)
tokenizer = AutoTokenizer.from_pretrained(tokenizer_path)
labels = ['Negative', 'Neutral', 'Positive']
def get_tweet_sentiment_roberta(text, model=model, tokenizer=tokenizer, labels=labels):
    encoded_input = tokenizer.encode_plus(text, return_tensors='pt')
    output = model(**encoded_input)
    scores = output[0][0].detach().numpy()
    scores = np.exp(scores) / np.exp(scores).sum(-1, keepdims=True)
    
    ranking = np.argsort(scores)
    ranking = ranking[::-1]
    return labels[ranking[0]]





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




# ############### Set up your OpenAI API key
import openai
from decouple import config

# Set up your OpenAI API key
OPENAI_APIKEY = config("OPENAI_APIKEY")
openai.api_key = OPENAI_APIKEY

# sentiment using OPENAI
def get_sentiment_openai(texts):
    # Set the model and parameters
    model_engine = "text-davinci-002"
    temperature = 0.5
    max_tokens = 1000  # Reduced max_tokens for faster response
    if isinstance(texts,list):
        prompt = "Sentiment analysis for the following texts in dictinary form:\n"
        # Concatenate the texts into a single prompt
        for text in texts:
            prompt += f"- {text}\n"

        # Call the OpenAI API to generate the sentiment for all texts
        output = openai.Completion.create(
            engine=model_engine,
            prompt=prompt,
            temperature=temperature,
            max_tokens=max_tokens,
            n = len(texts)  # Set n to the number of texts to get one output for each text
        )
        # Extract the sentiment for each text from the OpenAI API response
        text_dict = output.choices[0].text.strip()
        print(type(text_dict))
        return text_dict
    
    elif isinstance(texts,str):
        prompt = f"Sentiment analysis for the following text: {texts}."
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
        if ("positive" in sentiment or "Positive" in sentiment):
            return "Positive"
        elif ("negative" in sentiment or "Negative" in sentiment):
            return "Negative"
        else:
            return "Neutral"


if __name__=="__main__":
    # Example usage
    # text_list = ["I love OpenAI!", "I hate Mondays","Byju is good","Chatgpt is bad","whitehatjr is not bad","cuemath is not good","How are you?","Bad taste of food","you are bitch","you are not awseome""I love OpenAI!", "I hate Mondays","Byju is good","Chatgpt is bad","whitehatjr is not bad","cuemath is not good","How are you?","Bad taste of food","you are bitch","you are not awseome""I love OpenAI!", "I hate Mondays","Byju is good","Chatgpt is bad","whitehatjr is not bad","cuemath is not good","How are you?","Bad taste of food","you are bitch","you are not awseome"]
    text_list="whitehatjr is not bad"
    print(get_sentiment_openai(text_list))



    # start_time = time.time()
    # print(get_sentiment_openai(text_list))
    # end_time = time.time()
    # print(f"Function 1 took {end_time - start_time:.4f} seconds")


        









