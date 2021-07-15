from django.db import models

# Create your models here.
class Expressions(models.Model):
    expression=models.CharField(max_length=200)
    result=models.CharField(max_length=200)
    def __str__(self):
        return self.expression