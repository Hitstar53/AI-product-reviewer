from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import ReviewSerializer
from base.models import Review
# Create your views here.

@api_view(['GET'])
def getRoutes(request):
    routes = [
        {
            'Endpoint': '/api/reviews/<product_url>',
            'method': 'GET',
            'body': None,
            'description': 'Returns all reviews for a product'
        }, 
        {
            'Endpoint': '/api/summary/<product_url>/',
            'method': 'GET',
            'body': None,
            'description': 'Returns summary of reviews for a product'
        },
        {
            'Endpoint': '/api/rating/<product_url>/',
            'method': 'GET',
            'body': None,
            'description': 'Returns rating of a product'
        },
        {
            'Endpoint': '/api/name/<product_url>/',
            'method': 'GET',
            'body': None,
            'description': 'Returns name of a product'
        }
    ]
    return Response(routes)

