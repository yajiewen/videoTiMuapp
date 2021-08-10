from django.db import models

# Create your models here.
class Table(models.Model):
    id = models.AutoField(primary_key=True)
    anliuuid = models.CharField(max_length=100,default='')
    Subject = models.CharField(max_length=200,default='')
    rightAnswer = models.CharField(max_length=100,default='')
    wrongAnswer1 = models.CharField(max_length=100,default='')
    wrongAnswer2 = models.CharField(max_length=100,default='')
    wrongAnswer3 = models.CharField(max_length=100,default='')