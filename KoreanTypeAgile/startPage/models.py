from django.db import models

# Create your models here.
class User(models.Model):
    userId = models.CharField(max_length=20)
    userPassword = models.CharField(max_length=40)
    def __str__(self):
        return self.userId