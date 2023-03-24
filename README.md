# Step to run the program

You need to run this program using`` python version 3.7``
and download ``MongoDB`` for database

Create the environment and download the dependencies using following command
```
pip install virtualenv
virtualenv env
pip install -r requirements.txt
```
**If some error occur while downloading the dependencies then download alll module manually which are:**
## Commands for installing required module
```
- pip install pymongo
- pip install transformer
- pip install scipy
- pip install tweepy
- pip install config
```

**For intstalling pytorch**
1. In Windows/Linux:
```
    pip3 install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu113
```

 **Have to create the .env file with following API KEYS**
```
API_KEY= **Twitter API KEY**
API_KEY_SECRET = **Twitter API KEY**
ACCESS_TOKEN =**Twitter ACESS TOKEN**
ACCESS_TOKEN_SECRET =**Twitter ACCESS_TOKEN_SECRET**
OPENAI_APIKEY=**OPENAI CHATGPT API KEY**
```
## Backend /Server
**It has 4 main files**

the entry file is `app.py` -> from where the application start running

the dependency files are -> ``extraction, analyser, SentimentalModals`` respectively

**These files are server file. To run this, type in terminal**
```
python ./app.py
```
## Frontend
open the ``main.html`` file and run with ``live server`` 

**Note:** You have to keep index.html & style.css file into another folder and have to open with new instance of IDE bcz due to backend development server , the frontend file is getting refershed if kept in single folder and ran in same window of IDE

`test1.py` is for testing purpose only
