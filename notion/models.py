from django.db import models

class Notion(models.Model):
    user = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    url = models.CharField(max_length=255)
    parent = models.CharField(max_length=255)
    content = models.TextField()
    date = models.DateTimeField()