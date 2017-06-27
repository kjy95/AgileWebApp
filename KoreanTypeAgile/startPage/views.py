from django.shortcuts import render
from django.http import HttpResponse
import datetime
from .models import User, Todo

def index(request): 
    return render(request, 'startPages/index.html')
def loginPage(request):
    return render(request, 'startPages/loginPage.html')
def siginUpPage(request):
    return render(request, 'startPages/signUpPage.html')
def planMainPage(request):
    todos = Todo.objects.all()
    context = {'todos' : todos}
    return render(request, 'startPages/planMainPage.html', context)
def todoPopUp(request):
    return render(request, 'startPages/todoPopUp.html')
def sendTodoSubmit(request):
    projectName = request.POST['projectName']
    contents = request.POST['contents']
    startDate = request.POST['endDate']
    endDate = request.POST['endDate']

    if startDate != "":
        startDateSplit = startDate.split("T")
        startDateArray = startDateSplit[0].split("-") 
        startTimeArray = startDateSplit[1].split(":") 

    if endDate != "":
        endDateSplit = startDate.split("T")
        endDateArray = endDateSplit[0].split("-") 
        endTimeArray = endDateSplit[1].split(":") 

    todo = Todo(todoName = projectName,
                todoContents = contents,
                startDate = datetime.datetime(int(startDateArray[0]),int(startDateArray[1]),int(startDateArray[2]), int(startTimeArray[0]), int(startTimeArray[1])),
                endDate = datetime.datetime(int(endDateArray[0]),int(endDateArray[1]),int(endDateArray[2]),int(endTimeArray[0]),int(endTimeArray[1])))
    todo.save()
    return render(request, 'startPages/planMainPage.html')