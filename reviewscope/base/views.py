from django.shortcuts import render
from transformers import AutoTokenizer
from transformers import AutoModelForSequenceClassification
from scipy.special import softmax
from outscraper import ApiClient
import requests

#setup model (roberta)
MODEL = f"cardiffnlp/twitter-roberta-base-sentiment"
tokenizer = AutoTokenizer.from_pretrained(MODEL)
model = AutoModelForSequenceClassification.from_pretrained(MODEL)
def polarity_scores_roberta(example):
    encoded_text = tokenizer(example, return_tensors='pt')
    output = model(**encoded_text)
    scores = output[0][0].detach().numpy()
    scores = softmax(scores)
    scores_dict = {
        'roberta_neg' : scores[0],
        'roberta_neu' : scores[1],
        'roberta_pos' : scores[2]
    }
    print(scores_dict)
    return scores_dict

def api_call(link):
    api_client = ApiClient(api_key='Z29vZ2xlLW9hdXRoMnwxMTU3MTI4ODgzMjY3NDgyNTQ2MzF8YzBlN2I4YTE3NQ')
    results = api_client.amazon_reviews(link, limit=1)
    review = results[0][0]['body']
    rating = results[0][0]['rating']
    return review

# Create your views here.
def home(request):
    return render(request, 'base/home.html')

def search(request):
    if request.method == 'POST':
        text = request.POST['query']
        text = api_call(text)
        print(text)
        op = polarity_scores_roberta(text)
        return render(request, 'base/search.html', {'out': op})
    return render(request, 'base/search.html')