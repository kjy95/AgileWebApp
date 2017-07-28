from django.db import models
# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=20)
    email = models.CharField(max_length=40)
    password = models.CharField(max_length=40, default=' ')
    project = models.CharField(max_length=40, default='')

    def __str__(self):
        return self.name

 

class Project(models.Model):
    big_project_name = models.CharField(max_length=40, default='')
    project_member = models.CharField(max_length=40, default='')
    project_contents = models.CharField(max_length=40, default='')

    def __str__(self):
        return self.project_name


class Todo(models.Model):
    project_name = models.CharField(max_length=40, default='')
    todoName = models.CharField(max_length=40, default='')
    todoContents = models.CharField(max_length=40, default='')
    startDate = models.DateTimeField()#날짜, 시간을 나타냄, python datetime.datetime 인스턴스로 표현됨
    endDate = models.DateTimeField()
    
    create = models.BooleanField(default=False)
    todo = models.BooleanField(default=False)
    do = models.BooleanField(default=False)
    done = models.BooleanField(default=False)

    progress = models.FloatField(default = 0.0)
    person_created = models.CharField(max_length=40, default='')
    performer = models.CharField(max_length=40, default='')

    def __str__(self):
        return self.todoName

class Issue(models.Model):
    issue_name = models.CharField(max_length=40)
    issue_contents = models.CharField(max_length=40)
    person_created = models.CharField(max_length=40)
    commit = models.CharField(max_length=40)