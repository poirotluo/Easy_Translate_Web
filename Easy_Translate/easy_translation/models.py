from django.db import models

# Create your models here.
class user_info(models.Model):
    name = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
class diary(models.Model):
    title = models.CharField(max_length=30)
    text = models.CharField(max_length=500)
    dtime = models.DateTimeField(auto_now=True)
    User_info = models.ForeignKey('user_info')