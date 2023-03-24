from extraction import main_extraction
from analyser import main_analyser 
import pandas as pd
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_cors import cross_origin

app = Flask(__name__)
CORS(app) 


@app.route('/process', methods=['POST'])
def main():

    # get the platformList from the request body
    platformList = request.get_json()
    print(platformList)
    overall_score = []
    main_extraction(platformList)
    main_analyser(platformList)

    for collection in platformList:

        # read the data from a csv file
        data = pd.read_csv('{}.csv'.format(collection))
    # count the number of positive, negative, and neutral values in the sentiment column
        positive_count = len(data[data['sentiment'] == 'Positive'])
        negative_count = len(data[data['sentiment'] == 'Negative'])
        overall_score.append(positive_count-negative_count)
    m=max(overall_score)
    top_platform = platformList[overall_score.index(m)]
    print(top_platform) 
    # top_platform ='bccjcnj'
    return jsonify({'top_platform': top_platform })

if __name__ == '__main__':
    app.run(debug=True) # http://localhost:5000/