from django.db import models
from django.conf import settings


class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE,)
    text = models.TextField(blank=False)
    date_added = models.DateTimeField(auto_now_add=True)


class PostRating(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    post = models.ForeignKey(Post,
                             on_delete=models.CASCADE)
    rating = models.CharField(
        max_length=1,
        choices=(("+", "+"),
                 ("-", "-")
                 )
    )
