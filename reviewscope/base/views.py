from django.shortcuts import render
from django.core.mail import send_mail
import pandas as pd
from transformers import AutoTokenizer, pipeline
from transformers import AutoModelForSequenceClassification
from transformers import AutoModelWithLMHead
from scipy.special import softmax
from outscraper import ApiClient
from joblib import load
import torch
import warnings
from sklearn.linear_model import LinearRegression
import cleantext
import requests
from bs4 import BeautifulSoup
from .models import Review
import time
#setup model (roberta)
warnings.filterwarnings("ignore")
lr_model=load('./savedModels/rating_predictor_updated.joblib')

MODEL1 = f"cardiffnlp/twitter-roberta-base-sentiment"
tokenizer1 = AutoTokenizer.from_pretrained(MODEL1)
model1 = AutoModelForSequenceClassification.from_pretrained(MODEL1)
def polarity_scores_roberta_list(review):
    encoded_text = tokenizer1(review, return_tensors='pt')
    output = model1(**encoded_text)
    scores = output[0][0].detach().numpy()
    scores = softmax(scores)
    scores_list = [scores[0], scores[1], scores[2]]
    return scores_list

#setup model (t5)
tokenizer2 = AutoTokenizer.from_pretrained('t5-base')
model2 = AutoModelWithLMHead.from_pretrained('t5-base', return_dict=True)

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

def get_summary(reviews):
    # text summarization
    # merge reviews
    merged_reviews = ''
    for i in range(len(reviews)):
        merged_reviews += reviews[i]
    # tokenize
    inputs = tokenizer2.encode("summarize: " + merged_reviews, return_tensors="pt", max_length=512, truncation=True)
    # generate summary
    outputs = model2.generate(inputs, max_length=150, min_length=40, length_penalty=2.0, num_beams=4, early_stopping=True)
    # decode
    summary = tokenizer2.decode(outputs[0])
    summary = summary.replace('<pad>', '')
    summary = summary.replace('</s>', '')
    # summarizer = pipeline("summarization")
    # summarized = summarizer(to_tokenize, min_length=75, max_length=300)
    # summ=' '.join([str(i) for i in summarized])
    return summary

# Create your views here.
def home(request):
    if request.method == 'POST':
            reviews = []
            ratings=[]
            p_name = ''
            rev_len=1
            iter = [1,2,3,4,5]
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36'}
            url = request.POST['query']
            if url == '':
                return render(request, 'base/home.html')
            if 'amazon' in url:
                a=True
                while a:
                    try:
                        reviews,ratings,p_name = api_call(url)
                        a=False
                    except:
                        #wait for 10 sec
                        print('waiting for 10 sec')
                        a=True
                        time.sleep(10)
                rev_len = len(reviews)
                review = Review.objects.filter(product_name=p_name)
                if review.exists():
                    avg_rate = review[0].rating
                    summary = review[0].summary
                    return render(request, 'base/home.html', {'avg' : avg_rate, 'iter' : iter, 'p_name' : p_name, 'summary': summary})
            elif 'myntra' in url:
                response = requests.get(url, headers=headers)
                soup = BeautifulSoup(response.content, 'html.parser')
                # get the product name from div with class product-details-brand
                try:
                    p_name = soup.find('div', {'class': 'product-details-brand'}).get_text()
                    p_name += soup.find('div', {'class': 'product-details-name'}).get_text()
                    print(p_name)
                    review = Review.objects.filter(product_name=p_name)
                    if review.exists():
                        avg_rate = review[0].rating
                        summary = review[0].summary
                        return render(request, 'base/home.html', {'avg' : avg_rate, 'iter' : iter, 'p_name' : p_name, 'summary': summary})
                except:
                    pass
                # get the review from div with class user-review-reviewTextWrapper
                try:
                    reviews_div = soup.find_all('div', {'class': 'user-review-reviewTextWrapper'})
                    for d in reviews_div:
                        text=d.get_text()
                        reviews.append(text)
                    print(len(reviews))
                    rate_box=soup.find_all('div', {'class': 'index-flexRow index-averageRating'})
                    for r in rate_box:
                        rate=r.get_text()
                        ratings.append(int(rate))
                except:
                    pass
            else:
                response = requests.get(url)
                soup = BeautifulSoup(response.content, 'html.parser')
                # get the product name from div with class _2s4DIt _1CDdy2
                try:
                    p_name = soup.find('div', {'class': '_2s4DIt _1CDdy2'}).get_text()
                    # remove the "reviews" from the end of the product name
                    p_name = p_name[:-7]
                    print(p_name)
                    review = Review.objects.filter(product_name=p_name)
                    if review.exists():
                        avg_rate = review[0].rating
                        summary = review[0].summary
                        return render(request, 'base/home.html', {'avg' : avg_rate, 'iter' : iter, 'p_name' : p_name, 'summary': summary})
                except:
                    pass
                # Find the div that contains the reviews
                try:
                    for i in range(1, 7):
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
            summary = get_summary(reviews)
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
            avg_pos=0
            avg_neg=0
            avg_neu=0
            for index, row in df_results.iterrows():
                avg_pos+=row['roberta_pos']
                avg_neg+=row['roberta_neg']
                avg_neu+=row['roberta_neu']
                star += lr_model.predict([[row['roberta_neg'],row['roberta_neu'],row['roberta_pos']]])
                rev_rate+=row['Score']
            avg_pos/=rev_len
            avg_neg/=rev_len
            avg_neu/=rev_len
            star/=rev_len
            rev_rate/=rev_len
            avg_rate = (star[0]+rev_rate)/2
            avg_rate = round(avg_rate, 2)
            review = Review.objects.filter(product_name=p_name)
            if review.exists():
                review = review[0]
                review.summary = summary
                review.rating = avg_rate
                review.neg = avg_neg
                review.neu = avg_neu
                review.pos = avg_pos
                review.save()
            else:
                user = None
                if request.user.is_authenticated:
                    user = request.user
                review = Review.objects.create(summary=summary, rating=avg_rate, product_name=p_name,neg=avg_neg,neu=avg_neu,pos=avg_pos,user=user)
                review.save()
            return render(request, 'base/home.html', {'avg' : avg_rate, 'iter' : iter, 'star' : star[0], 'rev' : rev_rate, 'p_name' : p_name, 'summary': summary})
    return render(request, 'base/home.html')

def payment(request,plan):
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        address = request.form.get('address')+','+request.form.get('city')+','+request.form.get('zipcode')
        pstatus = 'success'
    if plan == 'soldier':
            amt = 38
    elif plan == 'commander':
            amt = 69
    elif plan == 'prince':
            amt = 138
    else:
        amt = 0
    return render(request, 'base/payment.html',{'amt':amt})

def success(request):
    return render(request, 'base/success.html')

def contact(request):
    if request.method == 'POST':
        name = request.POST['uname']
        email = request.POST['email']
        message = request.POST['message']
        send_mail(
            'Contact Form',
            message,
            email,
            ['hatim.sawai@spit.ac.in'],
            fail_silently=False,
        )
        return render(request, 'base/contact.html')
    return render(request, 'base/contact.html')

def reviews(request):
    iter = [1,2,3,4,5]
    return render(request, 'base/reviews.html', {'reviews': Review.objects.all(), 'iter': iter})

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