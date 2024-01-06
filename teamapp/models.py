from django.db import models

# Create your models here.
# models.py



class SavedResult(models.Model):
    sql_result = models.TextField()
    sql_result = models.CharField(max_length=255) # 追加
    
    def __str__(self):
        return self.sql_result