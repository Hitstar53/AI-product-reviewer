from django.shortcuts import render
import pandas as pd
from transformers import AutoTokenizer
from transformers import AutoModelForSequenceClassification
from scipy.special import softmax
from outscraper import ApiClient
from joblib import load
import warnings
from sklearn.linear_model import LinearRegression
import requests

#setup model (roberta)
warnings.filterwarnings("ignore")
lr_model=load('./savedModels/rating_predictor_updated.joblib')

MODEL = f"cardiffnlp/twitter-roberta-base-sentiment"
tokenizer = AutoTokenizer.from_pretrained(MODEL)
model = AutoModelForSequenceClassification.from_pretrained(MODEL)
def polarity_scores_roberta_list(review):
    encoded_text = tokenizer(review, return_tensors='pt')
    output = model(**encoded_text)
    scores = output[0][0].detach().numpy()
    scores = softmax(scores)
    scores_list = [scores[0], scores[1], scores[2]]
    return scores_list


def api_call(link):
    api_client = ApiClient(api_key='Z29vZ2xlLW9hdXRoMnwxMTU3MTI4ODgzMjY3NDgyNTQ2MzF8YzBlN2I4YTE3NQ')
    result = api_client.amazon_reviews(link, limit=10)
    reviews = []
    ratings = []
    p_name = result[0][1]['product_name']
    for i in range(len(result[0])):
        reviews.append(result[0][i]['body'])
    for i in range(len(result[0])):
        ratings.append(result[0][i]['rating'])
    return reviews,ratings,p_name

# Create your views here.
def home(request):
    if request.method == 'POST':
        text = request.POST['query']
        if text == '':
            return render(request, 'base/home.html')
        reviews,ratings,p_name = api_call(text)
        rev_len = len(reviews)
        res = []
        op = []
        columns = ['Id', 'roberta_neg', 'roberta_neu', 'roberta_pos','Score']
        for i in range(rev_len):
            res.append([i]+polarity_scores_roberta_list(reviews[i])+[ratings[i]])
        df_results = pd.DataFrame(res, columns=columns)
        rev_rate=0
        star = 0
        print(rev_len)
        for index, row in df_results.iterrows():
            star += lr_model.predict([[row['roberta_neg'],row['roberta_neu'],row['roberta_pos']]])
            rev_rate+=row['Score']
        star/=rev_len
        rev_rate/=rev_len
        avg_rate = (star[0]+rev_rate)/2
        avg_rate = round(avg_rate, 2)
        iter = [1,2,3,4,5]
        return render(request, 'base/home.html', {'avg' : avg_rate, 'iter' : iter, 'star' : star[0], 'rev' : rev_rate, 'p_name' : p_name})
    return render(request, 'base/home.html')

def search(request):
    if request.method == 'POST':
        text = request.POST['query']
        reviews,ratings = api_call(text)
        rev_len = len(reviews)
        res = []
        op = []
        columns = ['Id', 'roberta_neg', 'roberta_neu', 'roberta_pos','Score']
        for i in range(rev_len):
            res.append([i]+polarity_scores_roberta_list(reviews[i])+[ratings[i]])
        df_results = pd.DataFrame(res, columns=columns)
        rev_rate=0
        star = 0
        print(rev_len)
        for index, row in df_results.iterrows():
            star += lr_model.predict([[row['roberta_neg'],row['roberta_neu'],row['roberta_pos']]])
            rev_rate+=row['Score']
        star/=rev_len
        rev_rate/=rev_len
        return render(request, 'base/search.html', {'star': star[0], 'rev' : rev_rate})
    return render(request, 'base/search.html')