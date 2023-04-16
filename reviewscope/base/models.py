from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Review(models.Model):
    product_name = models.CharField(max_length=100)
    rating = models.FloatField()
    summary = models.TextField()
    neg = models.FloatField(null=True, blank=True)
    neu = models.FloatField(null=True, blank=True)
    pos = models.FloatField(null=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    def __str__(self):
        return self.product_name[:50]+'...'
