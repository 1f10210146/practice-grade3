from django.db import models

# Create your models here.
# models.py



class SavedResult(models.Model):
    sql_result = models.TextField()