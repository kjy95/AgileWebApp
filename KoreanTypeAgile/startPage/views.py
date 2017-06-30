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
def todoSaveForm(todoName, todoContents, startDate, endDate):
    todo = Todo(todoName = todoName,
                todoContents = todoContents,
                startDate = startDate,
                endDate = endDate)
                        
    todo.save()
def sendTodoSubmit(request):
    projectName = request.POST['projectName']
    contents = request.POST['contents']
    startDate = request.POST['startDate']
    endDate = request.POST['endDate']

    maxCount = 0
    projectNameCount = -1
    contentsCount = -1

    tempCount = 0
    
    if startDate != "":
        startDateSplit = startDate.split("T")
        startDateArray = startDateSplit[0].split("-") 
        startTimeArray = startDateSplit[1].split(":") 

    if endDate != "":
        endDateSplit = endDate.split("T")
        endDateArray = endDateSplit[0].split("-") 
        endTimeArray = endDateSplit[1].split(":") 
        
    if projectName != "":
        projectNameArray = projectName.split("`")
        projectNameCount = len(projectNameArray)
        maxCount = projectNameCount - 1
    if contents != "":
       contentsArray = contents.split("`")
       contentsCount = len(contentsArray)
       if projectNameCount < contentsCount:
           maxCount = contentsCount - 1

    while tempCount < maxCount:
        if projectNameCount >= tempCount and contentsCount >= tempCount : 
            todoSaveForm(todoName = projectNameArray[tempCount],
                        todoContents = contentsArray[tempCount],
                        startDate = datetime.datetime(int(startDateArray[0]),int(startDateArray[1]),int(startDateArray[2]), int(startTimeArray[0]), int(startTimeArray[1])),
                        endDate = datetime.datetime(int(endDateArray[0]),int(endDateArray[1]),int(endDateArray[2]),int(endTimeArray[0]),int(endTimeArray[1])))
        #todo - error
        elif projectNameCount >= tempCount and contentsCount < tempCount :
            if contentsCount == -1 :
                todoSaveForm(todoName = projectNameArray[tempCount],
                        todoContents = "",
                        startDate = datetime.datetime(int(startDateArray[0]),int(startDateArray[1]),int(startDateArray[2]), int(startTimeArray[0]), int(startTimeArray[1])),
                        endDate = datetime.datetime(int(endDateArray[0]),int(endDateArray[1]),int(endDateArray[2]),int(endTimeArray[0]),int(endTimeArray[1])))
                        
            else:

                todoSaveForm(todoName = projectNameArray[tempCount],
                            todoContents = contentsArray[contentsCount],
                            startDate = datetime.datetime(int(startDateArray[0]),int(startDateArray[1]),int(startDateArray[2]), int(startTimeArray[0]), int(startTimeArray[1])),
                            endDate = datetime.datetime(int(endDateArray[0]),int(endDateArray[1]),int(endDateArray[2]),int(endTimeArray[0]),int(endTimeArray[1])))

        elif projectNameCount < tempCount and contentsCount >= tempCount :
            if projectNameCount == -1 :
                todoSaveForm(todoName = "",
                            todoContents = contentsArray[tempCount],
                            startDate = datetime.datetime(int(startDateArray[0]),int(startDateArray[1]),int(startDateArray[2]), int(startTimeArray[0]), int(startTimeArray[1])),
                            endDate = datetime.datetime(int(endDateArray[0]),int(endDateArray[1]),int(endDateArray[2]),int(endTimeArray[0]),int(endTimeArray[1])))
            else:
                todoSaveForm(todoName = projectNameArray[projectNameCount],
                        todoContents = contentsArray[tempCount],
                        startDate = datetime.datetime(int(startDateArray[0]),int(startDateArray[1]),int(startDateArray[2]), int(startTimeArray[0]), int(startTimeArray[1])),
                        endDate = datetime.datetime(int(endDateArray[0]),int(endDateArray[1]),int(endDateArray[2]),int(endTimeArray[0]),int(endTimeArray[1])))


        tempCount = tempCount + 1
        

    todoSaveForm(todoName = projectNameArray[tempCount],
                        todoContents = contentsArray[tempCount],
                        startDate = datetime.datetime(int(startDateArray[0]),int(startDateArray[1]),int(startDateArray[2]), int(startTimeArray[0]), int(startTimeArray[1])),
                        endDate = datetime.datetime(int(endDateArray[0]),int(endDateArray[1]),int(endDateArray[2]),int(endTimeArray[0]),int(endTimeArray[1])))
    todos = Todo.objects.all()
    context = {'todos' : todos}
    return render(request, 'startPages/planMainPage.html', context)