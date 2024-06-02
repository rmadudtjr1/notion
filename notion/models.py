from django.db import models

class Notion(models.Model):
    user = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    url = models.CharField(max_length=255)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='children')
    content = models.TextField()
    date = models.DateTimeField()

    def __str__(self):
        return self.url;