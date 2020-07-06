from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Crazybone(models.Model):
    name = models.CharField(max_length=100)
    img = models.CharField(max_length=150)
    description = models.TextField(max_length=300)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cb = models.ManyToManyField(Crazybone)

class Comment(models.Model):
    text = models.TextField(max_length=300)
    date = models.DateTimeField(auto_now_add=True, blank=True)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)


class TradeRequest(models.Model):
    user_from = models.ForeignKey(Profile, on_delete=models.CASCADE)
    user_to = models.ForeignKey(Profile, on_delete=models.CASCADE)
    cb_wanted = models.ForeignKey(Crazybone, on_delete=models.CASCADE)
    cb_offered = models.ForeignKey(Crazybone, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True, blank=True)


class FriendList(models.Model):
    user = models.ForeignKey(Profile, related_name='a', on_delete=models.CASCADE)
    myId = models.ForeignKey(Profile, related_name='b', on_delete=models.CASCADE)

    # def __str__(self):
    #     return f"{self.user.user} is friends with you ({self.myId.user})"



