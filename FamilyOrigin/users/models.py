from django.db import models


class Users(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    realName = models.CharField(max_length=15, blank=False)
    nickName = models.CharField(max_length=50, blank=True, default='')
    sex = models.CharField(max_length=2, blank=False)
    birthday = models.DateTimeField()
    avatar = models.URLField()
    mother = models.IntegerField(max_length=10)
    father = models.IntegerField(max_length=10)
    children = models.TextField()
    forebears = models.TextField()
    lastLogin = models.DateTimeField()
    idCard = models.CharField(max_length=18)
    openId = models.CharField(max_length=100)
    token = models.CharField(max_length=100)

    class Meta:
        ordering = ('created',)
