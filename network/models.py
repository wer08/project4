from email.policy import default
from django.contrib.auth.models import AbstractUser
from django.db import models
from pymysql import Timestamp


class User(AbstractUser):

    pass
    def __str__(self):
        return self.username

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.CharField(max_length = 1024)
    time_stamp = models.DateTimeField(auto_now_add = True)
    likes = models.PositiveIntegerField(default = 0)

    def __str__(self):
        return f"{self.author} {self.time_stamp}"

