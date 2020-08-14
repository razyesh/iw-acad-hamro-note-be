from django.db import models
from django.contrib.auth import get_user_model

USER = get_user_model()


class Question(models.Model):
    posted_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=False)
    user = models.ForeignKey(USER, on_delete=models.CASCADE)
    post_slug = models.SlugField()
    caption = models.TextField()
    file = models.FileField(upload_to='posts/files/', blank=True, null=True)
    stars_count = models.IntegerField(default=0)

    def __str__(self):
        return self.caption[:20] + '...'


class Answer(models.Model):
    commented_at = models.DateTimeField(auto_now_add=True)
    comment_modified_at = models.DateTimeField(auto_now=True)
    comment_description = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(USER, on_delete=models.CASCADE)
    stars_count = models.IntegerField(default=0)

    def __str__(self):
        return self.comment_description[:20] + '...'

