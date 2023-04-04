from django.shortcuts import render
import pandas as pd
from transformers import AutoTokenizer
from transformers import AutoModelForSequenceClassification
from scipy.special import softmax
from outscraper import ApiClient
from joblib import load
import warnings
from sklearn.linear_model import LinearRegression
import cleantext
import requests
from bs4 import BeautifulSoup

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

def clean(text):
    text = cleantext.clean(text, to_ascii=True, lower=True, no_line_breaks=True, no_urls=True, no_emails=True,no_emoji=True, no_phone_numbers=True, no_numbers=False, no_digits=False, no_currency_symbols=True, no_punct=False, replace_with_url="", replace_with_email="", replace_with_phone_number="", replace_with_number="", replace_with_digit="0", replace_with_currency_symbol="")
    return text

# Create your views here.
def home(request):
    if request.method == 'POST':
        reviews = []
        ratings=[]
        p_name = 'Flipkart'
        rev_len=1
        url = request.POST['query']
        if url == '':
            return render(request, 'base/home.html')
        if 'amazon' in url:
            reviews,ratings,p_name = api_call(url)
            rev_len = len(reviews)
        else:
            response = requests.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')
            # get the product name from div with class _2s4DIt _1CDdy2
            try:
                p_name = soup.find('div', {'class': '_2s4DIt _1CDdy2'}).get_text()
                print(p_name)
            except:
                pass
            # Find the div that contains the reviews
            try:
                for i in range(1, 4):
                    url=url+"&page="+str(i)
                    response = requests.get(url)
                    soup = BeautifulSoup(response.content, 'html.parser')
                    # reviews_div = soup.find_all('div', {'class': '_1AtVbE'})
                    # for d in reviews_div:
                    reviews_div = soup.find_all('div', {'class': 't-ZTKy'})
                    for d in reviews_div:
                        text=d.get_text()
                        reviews.append(text)
                    rate_box=soup.find_all('div', {'class': '_3LWZlK _1BLPMq'})
                    for r in rate_box:
                        rate=r.get_text()
                        ratings.append(int(rate))
            except:
                pass
        res = []
        op = []
        rev_len = len(reviews)
        columns = ['Id', 'roberta_neg', 'roberta_neu', 'roberta_pos','Score']
        try:
            for i in range(rev_len):
                #reviews[i]=clean(reviews[i])
                res.append([i]+polarity_scores_roberta_list(reviews[i])+[ratings[i]])
        except:
            pass
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

def payment(request):
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        address = request.form.get('address')+','+request.form.get('city')+','+request.form.get('zipcode')
        amt = 690
        pstatus = 'success'
    return render(request, 'base/payment.html')

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