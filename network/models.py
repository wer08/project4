from email.policy import default
from django.contrib.auth.models import AbstractUser
from django.db import models
from pymysql import Timestamp
from sqlalchemy import null


class User(AbstractUser):
    pass
    number_followers = models.IntegerField(default = 0)
    def __str__(self):
        return self.username

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.CharField(max_length = 1024)
    time_stamp = models.DateTimeField(auto_now_add = True)
    likes = models.PositiveIntegerField(default = 0)

    def __str__(self):
        return f"{self.author} {self.time_stamp}"

    def serialize(self):
        return {
            "author": self.author.username,
            "body": self.body,
            "time_stamp": self.time_stamp,
            "likes": self.likes,
            "id": self.pk
        }

class Following(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followings')
    followed = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')

    def __str__(self):
        return f"{self.follower} follows {self.followed}"

