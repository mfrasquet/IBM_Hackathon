from django.db import models
from django.contrib.auth.models import User


class Contract(models.Model):
    contractDate=models.DateField(auto_now_add=True)
    author=models.ForeignKey(User,on_delete=models.CASCADE)
    title=models.CharField(max_length=50, default="Unknown")
    description=models.CharField(max_length=250, blank=True)

    tempMAX=models.FloatField(default=80)
    tempMIN=models.FloatField(default=0)
    hrMAX=models.FloatField(default=100)
    hrMIN=models.FloatField(default=0)
    accMAX=models.FloatField(default=2)
    accMIN=models.FloatField(default=0)
    
    
# Create your models here.
