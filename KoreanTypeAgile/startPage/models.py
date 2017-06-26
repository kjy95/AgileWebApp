from django.db import models

# Create your models here.
class User(models.Model):
    userId = models.CharField(max_length=20)
    userPassword = models.CharField(max_length=40)
    def __str__(self):
        return self.userId
        
class Todo(models.Model):
    userId = models.CharField(max_length=20)

    todoName = models.CharField(max_length=40)
    todoContents = models.CharField(max_length=40)
    startDate = models.DateTimeField()#날짜, 시간을 나타냄, python datetime.datetime 인스턴스로 표현됨
    endDate = models.DateTimeField()
    
    def __str__(self):
        return self.todoName