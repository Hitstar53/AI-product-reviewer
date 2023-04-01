from django.shortcuts import render
import pandas as pd
from transformers import AutoTokenizer
from transformers import AutoModelForSequenceClassification
from scipy.special import softmax
from outscraper import ApiClient
import requests

#setup model (roberta)
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
    # make a generator to get the reviews from results[0][i]['body']
    reviews = []
    ratings = []
    for i in range(10):
        reviews.append(result[0][i]['body'])

    for i in range(10):
        ratings.append(result[0][i]['rating'])

    return reviews,ratings

# Create your views here.
def home(request):
    return render(request, 'base/home.html')

def search(request):
    if request.method == 'POST':
        text = request.POST['query']
        reviews,ratings = api_call(text)
        print(len(reviews))
        res = []
        op = []
        columns = ['Id', 'roberta_neg', 'roberta_neu', 'roberta_pos','Score']
        for i in range(10):
            res.append([i]+polarity_scores_roberta_list(reviews[i])+[ratings[i]])
        df_results = pd.DataFrame(res, columns=columns)
        rev_rate=0
        star = 0
        for index, row in df_results.iterrows():
            star += 5*row['roberta_pos'] + 2.5*row['roberta_neu'] + 0*row['roberta_neg']
            rev_rate+=row['Score']
        star/=10
        rev_rate/=10
        return render(request, 'base/search.html', {'star': star, 'rev' : rev_rate})
    return render(request, 'base/search.html')