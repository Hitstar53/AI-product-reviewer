from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import ReviewSerializer
from .models import Review
# Create your views here.

@api_view(['GET'])
def getRoutes(request):
    routes = [
        '/api/reviews/',
    ]
    return Response(routes)

@api_view(['GET'])
def getReviews(request):
    reviews = Review.objects.all()
    serializer = ReviewSerializer(reviews, many=True)
    return Response(serializer.data)