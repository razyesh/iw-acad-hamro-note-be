from django.db import models
from . blog import Blog

class Comment(models.Model):
    name = models.CharField(max_length=120)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    email = models.EmailField(unique=True)
    message = models.TextField()
    stars_count = models.IntegerField(default=0)
    date = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.name