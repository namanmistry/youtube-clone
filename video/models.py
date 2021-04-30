from django.db import models
from django.db.models.fields.related import ForeignKey
from account.models import Account



class Channel(models.Model):
    name = models.CharField(max_length=50, null=False)
    dateCreated = models.DateField(auto_now_add=True)
    subscribers = models.CharField(max_length=10, null=False, default='0')
    Account = models.ForeignKey(Account, on_delete=models.CASCADE)
    image = models.ImageField(default = 'default.png', upload_to='channel_pics')

class Video(models.Model):
    title = models.CharField(max_length=300, null=False)
    description1 = models.CharField(max_length=3000, null=False)
    description2 = models.CharField(max_length=3000, null=False)
    views = models.CharField(max_length=10, default='0')
    likes = models.CharField(max_length=10, default='0')
    dislikes = models.CharField(max_length=10, default='0')
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)
    datePosted = models.DateField(auto_now_add=True)
    thumbnail = models.ImageField(default='default.png', upload_to='thumbnails')

class History(models.Model):
    Account = models.ForeignKey(Account, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)

class Library(models.Model):
    Account = models.ForeignKey(Account ,on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)

class Comments(models.Model):
    Account = models.ForeignKey(Account ,on_delete=models.CASCADE)
    description = models.CharField(max_length=1000, null=False)
    edited = models.CharField(max_length=1, null=False, default='0')
    datePosted= models.DateField(auto_now_add=True)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    

