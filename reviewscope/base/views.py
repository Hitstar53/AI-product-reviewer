from django.shortcuts import render
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
import pandas as pd
from transformers import AutoTokenizer
from transformers import AutoModelForSequenceClassification
from scipy.special import softmax
from outscraper import ApiClient
from joblib import load
import warnings
import cleantext
import requests
from bs4 import BeautifulSoup
from .models import UserReviews, GeneralReviews
import time

#setup model (roberta)
warnings.filterwarnings("ignore")
lr_model=load('./savedModels/rating_predictor_updated.joblib')

MODEL1 = f"cardiffnlp/twitter-roberta-base-sentiment"
tokenizer1 = AutoTokenizer.from_pretrained(MODEL1)
model1 = AutoModelForSequenceClassification.from_pretrained(MODEL1)

def get_flipkart_reviews(product_name):
    # replace spaces with plus sign for URL
    search_query = product_name.replace(' ', '+')
    url = f'https://www.flipkart.com/search?q={search_query}&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&sort=relevance'

    # request Flipkart search page
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # get product link from search results
    product_link = soup.find('a', {'class': '_1fQZEK'})['href']

    # request product page
    url = f'https://www.flipkart.com{product_link}'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    reviews_link = [i['href'] for i in soup.find_all('a', href=True) if 'product-reviews' in i['href']][0]
    stop=reviews_link.index('&aid')
    reviews_link=reviews_link[:stop]
    print(reviews_link)
    url=f'https://www.flipkart.com{reviews_link}'
    print(url)
    review_text=[]
    rating_score=[]
    # Find the div that contains the reviews
    for i in range(1, 2):
        url=url+"&page="+str(i)
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        reviews = soup.find_all('div', {'class': 't-ZTKy'})
        for d in reviews:
            text=d.get_text()
            review_text.append(text)
        rate_box=soup.find_all('div', {'class': '_3LWZlK _1BLPMq'})
        for r in rate_box:
            rate=r.get_text()
            rating_score.append(rate)
    min_len=min(len(review_text),len(rating_score))
    review_text=review_text[:min_len]
    rating_score=rating_score[:min_len]
    return review_text,rating_score,min_len

def polarity_scores_roberta_list(review):
    print(review)
    print()
    encoded_text = tokenizer1(review, return_tensors='pt')
    output = model1(**encoded_text)
    scores = output[0][0].detach().numpy()
    scores = softmax(scores)
    scores_list = [scores[0], scores[1], scores[2]]
    return scores_list

#setup model (gpt3)

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

def get_asin(url):
    if 'amazon' in url:
        asin = url.split('product-reviews/')[1].split('/')[0]
        print(asin)
    return asin

def get_image(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36'}
    asin=get_asin(url)
    ind=url.index('product-reviews')
    url=url[:ind]+'dp/'+asin+'/ref=cm_cr_arp_d_product_top?ie=UTF8'
    print(url)
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    image = soup.find('img', {'id': 'landingImage'})['src']
    print(image)
    return image

def clean(text):
    text = cleantext.clean(text, to_ascii=True, lower=True, no_line_breaks=True, no_urls=True, no_emails=True,no_emoji=True, no_phone_numbers=True, no_numbers=False, no_digits=False, no_currency_symbols=True, no_punct=False, replace_with_url="", replace_with_email="", replace_with_phone_number="", replace_with_number="", replace_with_digit="0", replace_with_currency_symbol="")
    return text

def web_scraper(url):
    reviews = []
    ratings=[]
    p_name = ''
    image = ''
    created = ''
    if 'amazon' in url:
        while True:
            try:
                reviews,ratings,p_name = api_call(url)
                break
            except:
                print('waiting for 10 sec')
                time.sleep(10)
        #flipkart reviews, append review and rating, continue
        is_available=False
        review = GeneralReviews.objects.filter(product_name=p_name)
        avg_rate = 0
        summary = ''
        len_review = len(reviews)
        # print(reviews)
        if review.exists():
            avg_rate = review[0].rating
            summary = review[0].summary
            image = review[0].img
            created = review[0].created
        else:
            try:
                review_text,rating_score,min_len = get_flipkart_reviews(p_name)
                for i in range(min_len):
                    reviews.append(review_text[i])
                    ratings.append(rating_score[i])
                is_available=True
            except:
                print('no flipkart reviews')
            image = get_image(url)
            rev_len = len(reviews)
    return avg_rate,p_name,summary,reviews,ratings,len_review,image,created,is_available

def get_summary(reviews):
    # text summarization
    merged_reviews = ''
    for i in range(len(reviews)):
        merged_reviews += reviews[i]
    url = "https://article-extractor-and-summarizer.p.rapidapi.com/summarize-text"
    payload = { "text": merged_reviews}
    headers = {
	    "content-type": "application/json",
	    "X-RapidAPI-Key": "c5f70b06ddmsh1f4a649c3843cabp1204ccjsn3025fdfa0cc3",
	    "X-RapidAPI-Host": "article-extractor-and-summarizer.p.rapidapi.com"
    }
    response = requests.post(url, json=payload, headers=headers)
    summary = response.json()['summary']
    return summary

# Create your views here.
def home(request):
    if request.method == 'POST':
            reviews = []
            ratings=[]
            p_name = ''
            image = ''
            created = ''
            rating_count = [0,0,0,0,0]
            rev_len=1
            iter = [1,2,3,4,5]
            url = request.POST['query']
            if url == '':
                return render(request, 'base/home.html')
            avg_rate, p_name, summary, reviews, ratings, rev_len, image, created, is_available = web_scraper(url)

            if avg_rate != 0:
                review = GeneralReviews.objects.filter(product_name=p_name)
                avg_rate = review[0].rating
                summary = review[0].summary
                check=None
                if request.user.is_authenticated:
                    check = UserReviews.objects.filter(product_name=p_name, user=request.user)
                else:
                    return render(request, 'base/home.html', {'avg' : avg_rate, 'iter' : iter, 'p_name' : p_name, 'summary': summary, 'img': image, 'created': created})
                if request.user.is_authenticated and not check.exists():
                    user = request.user
                    review_save = UserReviews.objects.create(summary=review[0].summary, rating=review[0].rating, product_name=review[0].product_name,neg=review[0].neg,neu=review[0].neu,pos=review[0].pos,user=user,flipkart=is_available,img=image)
                    review_save.save()
                return render(request, 'base/home.html', {'avg' : avg_rate, 'iter' : iter, 'p_name' : p_name, 'summary': summary, 'img': image, 'created': created})
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
                star += float(lr_model.predict([[row['roberta_neg'],row['roberta_neu'],row['roberta_pos']]])[0])
                current_rating=float(row['Score'])
                print(current_rating)
                rev_rate+=current_rating
                rating_count[int(current_rating)-1]+=1
            avg_pos/=rev_len
            avg_neg/=rev_len
            avg_neu/=rev_len
            star/=rev_len
            rev_rate/=rev_len
            avg_rate = (star+rev_rate)/2
            avg_rate = round(avg_rate, 2)
            print("Avg Rating : ",avg_rate)
            print("Star Rating : ",star)
            user = None
            if request.user.is_authenticated:
                user = request.user
                review = UserReviews.objects.create(summary=summary, rating=avg_rate, product_name=p_name,neg=avg_neg,neu=avg_neu,pos=avg_pos,user=user,flipkart=is_available,img=image)
                review.save()
                review2 = GeneralReviews.objects.create(summary=summary, rating=avg_rate, product_name=p_name,neg=avg_neg,neu=avg_neu,pos=avg_pos,flipkart=is_available,sc_1=rating_count[0],sc_2=rating_count[1],sc_3=rating_count[2],sc_4=rating_count[3],sc_5=rating_count[4],img=image)
                review2.save()
            else:
                review = GeneralReviews.objects.create(summary=summary, rating=avg_rate, product_name=p_name,neg=avg_neg,neu=avg_neu,pos=avg_pos,flipkart=is_available,sc_1=rating_count[0],sc_2=rating_count[1],sc_3=rating_count[2],sc_4=rating_count[3],sc_5=rating_count[4],img=image)
                review.save()
            return render(request, 'base/home.html', {'avg' : avg_rate, 'iter' : iter, 'star' : star, 'rev' : rev_rate, 'p_name' : p_name, 'summary': summary, 'img': image,'rating_data':rating_count,'avg_pos':avg_pos,'avg_neg':avg_neg,'avg_neu':avg_neu, 'created': created})
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

@login_required
def reviews(request, pname):
    iter = [1,2,3,4,5]
    highlighted=GeneralReviews.objects.filter(product_name=pname)
    highlighted=highlighted[0]
    return render(request, 'base/reviews.html', {'reviews': UserReviews.objects.all(), 'iter': iter, 'highlighted':highlighted,'check':True})

@login_required
def history(request):
    iter = [1,2,3,4,5]
    return render(request, 'base/reviews.html', {'reviews': UserReviews.objects.all(), 'iter': iter,'check':False})