from django.db import models
from django.contrib.auth.models import User
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

TRADE_STATUS = (
    ('A', 'Accepted'),
    ('R', 'Rejected'),
    ('P', 'Pending')
)
class TradeRequest(models.Model):
    user_from = models.ForeignKey(Profile, related_name='user_from', on_delete=models.CASCADE)
    user_to = models.ForeignKey(Profile, related_name='user_to', on_delete=models.CASCADE)
    cb_wanted = models.ForeignKey(Crazybone, related_name='cb_wanted', on_delete=models.CASCADE)
    cb_offered = models.ForeignKey(Crazybone, related_name='cb_offered', on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True, blank=True)
    status = models.CharField(
        max_length=1,
        choices=TRADE_STATUS,
        default=[2][0]
    )
    def __str__(self):
        return f"{self.user_from} <-> {self.user_to} ... {self.cb_wanted} <-> {self.cb_offered}"

class FriendList(models.Model):
    user = models.ForeignKey(Profile, related_name='a', on_delete=models.CASCADE)
    myId = models.ForeignKey(Profile, related_name='b', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user} - {self.myId}"


TYPE_OF_NOTIFICATION = (
    ('T', 'Trade Request'),
    ('F', 'Friend Request')
)
class Notification(models.Model):
    notification_type = models.CharField(
        max_length=1,
        choices=TYPE_OF_NOTIFICATION,
        default=TYPE_OF_NOTIFICATION[0][0]
    )
    noti_from = models.ForeignKey(Profile, related_name='noti_from', on_delete=models.CASCADE)
    noti_to = models.ForeignKey(Profile, related_name='noti_to', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.noti_from} -> {self.noti_to} ; {self.notification_type}"

