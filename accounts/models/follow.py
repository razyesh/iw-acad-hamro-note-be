from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class UserFollow(models.Model):
    follow_to = models.ForeignKey(User, related_name='user_follow_to', on_delete=models.CASCADE)
    follow_by = models.ForeignKey(User, related_name='user_follow_by', on_delete=models.CASCADE)
    datetime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.follow_to.username

    class Meta:
        verbose_name_plural = 'User Follow Records'
        ordering = ['-datetime']