from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
# Create your models here.


class User(models.Model):
    name = models.CharField(max_length=20)
    email = models.CharField(max_length=40)
    password = models.CharField(max_length=40, default=' ')
    Lastproject= models.CharField(max_length=40, default='')
    

    def __str__(self):
        return self.name

 

class Project(models.Model):
    project_name = models.CharField(max_length=40, default='')
    project_leader = models.CharField(max_length=40, default='')
    project_member = models.CharField(max_length=40, default='')
    project_contents = models.CharField(max_length=40, default='')
    project_Cycle=models.IntegerField(default=7,validators=[MaxValueValidator(10), MinValueValidator(5)])
    project_start_time = models.DateTimeField(auto_now=True)
    project_role=models.CharField(max_length=40,default='')
    def __str__(self):
        return self.project_name


class Todo(models.Model):
    project_week=models.IntegerField(default=1)
    project_name = models.CharField(max_length=40, default='')
    todoName = models.CharField(max_length=40, default='')
    todoContents = models.CharField(max_length=40, default='')
    startDate = models.DateTimeField()#날짜, 시간을 나타냄, python datetime.datetime 인스턴스로 표현됨
    endDate = models.DateTimeField()
    updated_at = models.DateTimeField(auto_now=True)
    
    todo = models.BooleanField(default=True)
    do = models.BooleanField(default=False)
    done = models.BooleanField(default=False)

    progress = models.FloatField(default = 0.0)
    person_created = models.CharField(max_length=40, default='')
    performer = models.CharField(max_length=40, default='')

    def make_status_todo(self):
        self.todo = True
        self.do = False
        self. done = False
    def make_status_do(self):
        self.todo = False
        self.do = True
        self. done = False
    def make_status_done(self):
        self.todo = False
        self.do = False
        self. done = True
    def get_status(self):
        if self.todo:
            return "todo"
        if self.do:
            return "do"
        if self.done:
            return "done" 

    def __str__(self):
        return self.todoName

class Issue(models.Model):
    issue_name = models.CharField(max_length = 40, default = '')
    issue_contents = models.CharField(max_length = 40)
    issue_type = models.CharField(max_length = 40)
    issue_severity = models.CharField(max_length = 40, default = '')
    issue_priority = models.CharField(max_length = 40, default = '')
    issue_status = models.CharField(max_length = 40, default = '')
    issue_create = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.issue_name

class Wiki(models.Model):
    bookmark_listname = models.CharField(max_length=10, default='')

    
class Brainstorm(models.Model):
    project_week=models.IntegerField(default=1)
    project_name=models.CharField(max_length=40)
    ideas=models.TextField()
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.project_name

