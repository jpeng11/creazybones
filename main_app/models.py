from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
# Create your models here.

class Crazybone(models.Model):
    name = models.CharField(max_length=100)
    img = models.CharField(max_length=150)
    description = models.TextField(max_length=300)

    def __str__(self):
        return f"{self.name}"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cb = models.ManyToManyField(Crazybone)

    def __str__(self):
        return f"{self.user}"

class Comment(models.Model):
    text = models.TextField(max_length=300)
    date = models.DateTimeField(auto_now_add=True, blank=True)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    cb = models.ForeignKey(Crazybone, on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.text}"

    def get_absolute_url(self):
        cb = Crazybone.objects.get(comment=self)
        return reverse('cb_detail', kwargs={'cb_id': cb.id})

class TradeRequest(models.Model):
    user_from = models.ForeignKey(Profile, related_name='user_from', on_delete=models.CASCADE)
    user_to = models.ForeignKey(Profile, related_name='user_to', on_delete=models.CASCADE)
    cb_wanted = models.ForeignKey(Crazybone, related_name='cb_wanted', on_delete=models.CASCADE)
    cb_offered = models.ForeignKey(Crazybone, related_name='cb_offered', on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True, blank=True)
    def __str__(self):
        return f"{self.user_from} <-> {self.user_to} ... {self.cb_wanted} <-> {self.cb_offered}"

class FriendList(models.Model):
    user = models.ForeignKey(Profile, related_name='a', on_delete=models.CASCADE)
    myId = models.ForeignKey(Profile, related_name='b', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user} - {self.myId}"



