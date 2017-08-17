from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from .models import User, Todo, Project, Brainstorm
from konlpy.tag import Twitter
from collections import Counter
from os import path
import datetime,csv,pytagcloud,os
import matplotlib.pyplot as plt

def index(request): 
    return render(request, 'startPages/index.html')  
def loginPage(request):
    return render(request, 'startPages/loginPage.html')
def signUpPage(request):
    return render(request, 'startPages/signUpPage.html')
def planMainPage_project(request,project_name):
    request.session['project_name']=project_name
    todos = Todo.objects.all()
    context = {'todos' : todos}
    return render(request, 'startPages/left_navi/planMainPage.html', context)
def planMainPage(request):
    todos = Todo.objects.all()
    context = {'todos' : todos}
    return render(request, 'startPages/left_navi/planMainPage.html', context)
def todoPopUp(request):
    return render(request, 'startPages/todoPopUp.html')
def todoSaveForm(todoName, todoContents, startDate, endDate):
    todo = Todo(todoName = todoName,
                todoContents = todoContents,
                startDate = startDate,
                endDate = endDate)
                        
    todo.save()
    
def send_project_submit(request):
    big_project_name = request.POST.get('big_project_name', False)
    project_contents = request.POST['project_contents']
    project_member = request.POST['project_member']
    project = Project(
                project_name = big_project_name,
                project_contents = project_contents,
                project_member = project_member)
                
                        
    project.save()
    projects = Project.objects.all()
    context = {'projects' : projects}
    request.session['member_count'] = 0
    return render(request, 'startPages/top_navi/homepage.html', context)
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
    content_todo=Todo.objects.values('todoContents')
    todos = Todo.objects.all()
    context = {'todos' : todos}
    return render(request, 'startPages/left_navi/planMainPage.html', context)

def homepage(request):
    wordcloud_flag=request.session['flag']
    if wordcloud_flag is 1 :
        output_csv('Brainstorming_idea.csv','ideas') #csv 파일로 아이디어들을 추출합니다.
        try:
            os.remove('..//KoreanTypeAgile/startPage/static/image/wordcloud.jpg')
            make_wordcloud('Brainstorming_idea.csv','wordcloud.jpg',530,300)
            os.rename('wordcloud.jpg','..//KoreanTypeAgile/startPage/static/image/wordcloud.jpg')
        except:    
            make_wordcloud('Brainstorming_idea.csv','wordcloud.jpg',530,300)
            os.rename('wordcloud.jpg','..//KoreanTypeAgile/startPage/static/image/wordcloud.jpg')
        request.session['flag'] = 0
    projects = Project.objects.all()
    context = {'projects' : projects}
    return render(request, 'startPages/top_navi/homepage.html', context)
def profile(request):
    userid=request.session['userid']
    #로그인 할때 저장한 session 을 불러서 userid 에 저장 해줍니다. userid 에는 로그인한 email이 저장 됩니다.
    userinfo=User.objects.filter(email=userid).values('name','email','project')
    #로그인한 email 값들 중에서 name , email , project 값들을 가져 옵니다.
    #129~134 -> render 함수에서 dict 형태를 요구해서 바꿔주는 코드 입니다.
    userinfo_list = [entry for entry in userinfo] # userinfo를 list로 바꿔주는 코드    
    userinfo_dict={}
    for user in userinfo_list:#list를 dict로 바꿔주는 for문 입니다. 
        for items in user :
           value=user[items]
           userinfo_dict[items]=value
    return render(request, 'startPages/top_navi/profile.html',userinfo_dict)  
def create_project(request):
    request.session['member_count'] = 0
    return render(request, 'startPages/top_navi/create_project.html')    
def search(request):
    return render(request, 'startPages/left_navi/search.html')    
def timeline(request):
    return render(request, 'startPages/left_navi/timeline.html')    
def backlog(request):
    return render(request, 'startPages/left_navi/backlog.html')    
def kanban(request):
    todos = Todo.objects.all()
    context = {'todos' : todos} 
    return render(request, 'startPages/left_navi/kanban.html', context)    
def issues(request):
    return render(request, 'startPages/left_navi/issues.html')    
def wiki(request):
    return render(request, 'startPages/left_navi/wiki.html')    
def team(request):
    return render(request, 'startPages/left_navi/team.html')    
def popup_invite_team(request):
    count=request.session['member_count']
    member=request.POST.get('project_member',None)
    print(member)
    if member is None :
        context={}
        return render(request,'startPages/popup_invite_team.html',context)    
    member_exist=User.objects.filter(email=member).exists()
    
    if member_exist is True :
        messages.info(request,"추가되었습니다.")
        request.session['member_count'] = count + 1
        context={'useremail':member,'count':count}
    else :
        messages.info(request,"존재하지 않는 이메일 입니다.")
        context={}
    return render(request,'startPages/popup_invite_team.html',context)    
    

def Signup(request) :
    name=request.POST['name']
    email=request.POST['email']
    password=request.POST['password']
    #signuppage.html 에서 POST 방식으로 입력 받은 값을 전송 해주고, 받아오는 코드 
    userdata=User(name = name,email = email,password = password)
    #userdata에 User 클래스 필드에 값을 초기화 시켜 놓습니다
    if User.objects.filter(email=email).exists() is True : #입력받은 이메일이 DB에 존재 한다면! (이메일중복검사)
        messages.error(request,"이미 존재하는 이메일 입니다.") #error 타입으로 message를 보내줍니다.
        return render(request,'startPages/signUpPage.html') 
    else : # 이메일이 중복되지 않은 경우 
        userdata.save() 
    
    userdatas=User.objects.all()
    userdatas={'userdatas':userdatas}
    return render(request,'startPages/index.html',userdatas)

def Signin(request):
    input_email = request.POST.get('email',None)
    input_password=request.POST.get('password',None)
    #signin.html에서 받은 값을 체크하고, 없는경우 None 으로 설정 해줍니다.
    check_email=User.objects.filter(email=input_email).exists()
    #DB에 입력받은 email 이 있는지 체크하고 Ture False 로 return 받은 값을 check_email 에 초기화 시킵니다.
    if check_email is True : # email 은 일치 
        check_password=User.objects.filter(email=input_email,password=input_password).exists()
    
        if check_password is True : # password 도 일치
            
            projects = Project.objects.all()
            request.session['userid']=input_email
            request.session['flag'] = 1
            #로그인한 유저를 저장하기 위해 session 에 저장을 해줍니다. 
            # ex ) {'userid' : input_email } 
            userdatas={'email' :input_email,'password':input_password, 'projects' : projects}
            return render(request,'startPages/top_navi/homepage.html',userdatas)
        
        elif check_password is False : # email 은 일치, password는 불일치
            messages.error(request,"비밀번호가 일치하지 않습니다.")
            
    elif check_email is False:# email이 불일치 , password는 체크 X 
        messages.error(request,"존재하지 않는 이메일 입니다.")
    
    userdatas={'email' :input_email,'password':input_password}   
    return render(request,'startPages/index.html',userdatas)
   
def brain_storming(request):
    idea=request.POST.get('input_idea',None)
    project_name=request.session['project_name']
    #idea에 입력받은 값을 저장, 없으면 None 으로 초기화.
    #None 은 처음 Brainstorming.html을 실행시켰을때 발생하는 값입니다. 
    if idea is not None :# idea에 내용을 입력한 경우
        temp=Brainstorm(ideas=idea,project_name=project_name)
        temp.save()
        request.session['flag'] = 1
        content=Brainstorm.objects.all()
        return render(request,'startPages/left_navi/brain_storming.html',{'content':content,'project_name':project_name})
    else :# 입력하지 않은 경우 or 처음 실행시킨 경우
        content=Brainstorm.objects.all()
        return render(request,'startPages/left_navi/brain_storming.html',{'content':content,'project_name':project_name})


def output_csv(text,key): 
    with open(text, 'w',newline='') as csvfile:
        #Brainstorming_idea.csv 를 w 만들어주고, csvfile 이라는 변수에 초기화
        spamwriter = csv.writer(csvfile)
        #csv 객체를 만들어주고
        ideas=Brainstorm.objects.values(key)
        #<QuerySet [{'ideas': '테스트 1'}, {'ideas': '테스트 2'} >
        for idea in ideas:
            spamwriter.writerow([idea[key]])
            #Brainstorming.idea.csv 파일에 적어 줍니다. 
            # idea['ideas']가 아니라 [idea['ideas']] 인 이유는, 전자의 경우 모든 단어마다 쉼표를 넣어주게 됩니다. 
def return_list_of_tuples(csv_file):
    with open(csv_file,'r') as csvfile:
        #Brainstorming_idea.csv 를 w 만들어주고, csvfile 이라는 변수에 초기화
        text=csvfile.read()
        split=Twitter()
        #konlpy 라는 한국어 정보처리 모듈 중 하나인 Twitter 기능입니다.
        nouns=split.nouns(text)
        #text 에서 명사만 추출하는 코드입니다
        #ex) ['아이디어', '오늘', '년', '월', '일', '오늘', '비', '피자', '마우스', '컴퓨터'] 
        counts=Counter(nouns)
        #ex) ({'오늘': 2, '아이디어': 1, '년': 1, '월': 1, '일': 1, '비': 1, '피자': 1, '마우스': 1, '컴퓨터': 1})
        count_noun=[]
        #Wordcloud 객체에서 list of tuple 형태를 원하고 있어서, counts 를 재가공하는 코드입니다.
        for noun, count in counts.most_common(20): 
            temp=(noun , count)
            count_noun.append(temp)
        return count_noun

def change_todo_data(request):   
    todo_id = request.POST['todo_id'] 
    target_id = request.POST['target_id'] 
    target_todo_obj = Todo.objects.get(id=todo_id)
    if target_id == "TODO":
        target_todo_obj.make_status_todo()
    elif target_id == "DOING":
        target_todo_obj.make_status_do()
    elif target_id == "DONE":
        target_todo_obj.make_status_done()
    
    target_todo_obj.save()
    return HttpResponse("You're looking at question")

def make_wordcloud(text,image_name,width,height):
    list_of_tuple=return_list_of_tuples(text)
    tuple_countnoun=tuple(list_of_tuple)
    taglist=pytagcloud.make_tags(tuple_countnoun)
    pytagcloud.create_tag_image(taglist,image_name,size=(width,height),fontname='Nanum Gothic',rectangular=False)
    
    