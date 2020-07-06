from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Crazybone(models.Model):
    name = models.CharField(max_length=100)
    img = models.CharField(max_length=150)
    description = models.TextField(max_length=300)

    def __str__(self):
        return f"The {self.name} crazybone has the following description: {self.description}"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cb = models.ManyToManyField(Crazybone)

    def __str__(self):
        return f"{self.user.user} has the following cb: {self.cb}"

class Comment(models.Model):
    text = models.TextField(max_length=300)
    date = models.DateTimeField(auto_now_add=True, blank=True)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    cb = models.ForeignKey(Crazybone, on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.text}  - written by {self.user} on the {self.cb} at {self.date}"

class TradeRequest(models.Model):
    user_from = models.ForeignKey(Profile, related_name='user_from', on_delete=models.CASCADE)
    user_to = models.ForeignKey(Profile, related_name='user_to', on_delete=models.CASCADE)
    cb_wanted = models.ForeignKey(Crazybone, related_name='cb_wanted', on_delete=models.CASCADE)
    cb_offered = models.ForeignKey(Crazybone, related_name='cb_offered', on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True, blank=True)
    def __str__(self):
        return f"{self.user_from} wants to trade with {self.user_to}... they want {cb_wanted} in exchange for their {cb_offered}"

class FriendList(models.Model):
    user = models.ForeignKey(Profile, related_name='a', on_delete=models.CASCADE)
    myId = models.ForeignKey(Profile, related_name='b', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.user} is friends with you ({self.myId.user})"



