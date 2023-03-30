from django.db import models

# Create your models here.
class Review(models.Model):
    review = models.TextField()
    polarity = models.CharField(max_length=10)
    def __str__(self):
        return self.review

