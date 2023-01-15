from django.db import models

# Create your models here.

class lists(models.Model):
    id = models.AutoField(primary_key=True)
    added_date = models.DateField(auto_now=True)
    time = models.TimeField(auto_now=True)
    text = models.CharField(max_length=50)
