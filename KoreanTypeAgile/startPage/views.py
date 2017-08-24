from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from .models import User, Todo, Project, Brainstorm, Issue
from konlpy.tag import Twitter
from collections import Counter
from os import path
import datetime,csv,pytagcloud,os
import matplotlib.pyplot as plt
import xlwt
import plotly.plotly as py #그래프 만들때 
from plotly.graph_objs import * #
import plotly.offline as offline # 
import plotly.graph_objs as go #
def index(request): 
    return render(request, 'startPages/index.html')  
def loginPage(request):
    return render(request, 'startPages/loginPage.html')
def signUpPage(request):
    return render(request, 'startPages/signUpPage.html')
def planMainPage_project(request,project_name):
    request.session['project_name']=project_name
    todos = Todo.objects.filter(project_name=project_name)
    context = {'todos' : todos}
    return render(request, 'startPages/left_navi/planMainPage.html', context)
def planMainPage(request):
    project_name=request.session['project_name']
    todos = Todo.objects.filter(project_name=project_name)
    context = {'todos' : todos}
    return render(request, 'startPages/left_navi/planMainPage.html', context)
def todoPopUp(request):
    return render(request, 'startPages/todoPopUp.html')
def todoSaveForm(todoName, person_created, todoContents, startDate, endDate,project_name):
    todo = Todo(todoName = todoName,  
                 person_created = person_created,
                todoContents = todoContents,
                startDate = startDate,
                endDate = endDate,
                project_name=project_name
                )
                        
    todo.save()
    
def send_project_submit(request):
    project_leader=request.session['userid']
    project_member=[]
    project_member.append(request.POST.get('member1', None))
    project_member.append(request.POST.get('member2', None))
    project_member.append(request.POST.get('member3', None))
    project_member.append(request.POST.get('member4', None))
    project_cycle=request.POST.get('cycle',7)
    big_project_name = request.POST.get('big_project_name', False)
    project_contents = request.POST.get('project_contents',None)
    project = Project(
                    project_name = big_project_name,
                    project_contents = project_contents,
                    project_leader = project_leader,
                    project_member = project_leader,
                    project_Cycle=project_cycle )
    project.save()
                    
    for i in range(4):
        project = Project(
                    project_name = big_project_name,
                    project_contents = project_contents,
                    project_leader = project_leader,
                    project_member = project_member[i],
                    project_Cycle=project_cycle )
        project.save()
                        
    projects = Project.objects.filter(project_member=project_leader).values('project_name','project_contents')
    context = {'projects' : projects}
    request.session['member_count'] = 0
    return render(request, 'startPages/top_navi/homepage.html', context)


def sendTodoSubmit(request):
    projectName = request.POST['projectName']
    contents = request.POST['contents']
    startDate = request.POST['startDate']
    endDate = request.POST['endDate']
    project_name=request.session['project_name']
    #create_user
    userid=request.session['userid']
    userinfo=User.objects.filter(email=userid).values('name')
    userinfo_list = [entry for entry in userinfo]  
    userinfo_dict={}
    for user in userinfo_list:#list를 dict로 바꿔주는 for문 입니다. 
        for items in user :
           value=user[items]
           userinfo_dict[items]=value
    create_user = userinfo_dict["name"]

    print(create_user)
    
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
            todoSaveForm( 
                todoName = projectNameArray[tempCount],
                        person_created = create_user,
                        todoContents = contentsArray[tempCount],
                        startDate = datetime.datetime(int(startDateArray[0]),int(startDateArray[1]),int(startDateArray[2]), int(startTimeArray[0]), int(startTimeArray[1])),
                        endDate = datetime.datetime(int(endDateArray[0]),int(endDateArray[1]),int(endDateArray[2]),int(endTimeArray[0]),int(endTimeArray[1])),
                        project_name=project_name)
        #todo - error
        elif projectNameCount >= tempCount and contentsCount < tempCount :
            if contentsCount == -1 :
                todoSaveForm(
                     todoName = projectNameArray[tempCount],
                        person_created = create_user,
                        todoContents = "",
                        startDate = datetime.datetime(int(startDateArray[0]),int(startDateArray[1]),int(startDateArray[2]), int(startTimeArray[0]), int(startTimeArray[1])),
                        endDate = datetime.datetime(int(endDateArray[0]),int(endDateArray[1]),int(endDateArray[2]),int(endTimeArray[0]),int(endTimeArray[1])),
                        project_name=project_name)
                        
            else:

                todoSaveForm(
                    todoName = projectNameArray[tempCount],
                            person_created = create_user,
                            todoContents = contentsArray[contentsCount],
                            startDate = datetime.datetime(int(startDateArray[0]),int(startDateArray[1]),int(startDateArray[2]), int(startTimeArray[0]), int(startTimeArray[1])),
                            endDate = datetime.datetime(int(endDateArray[0]),int(endDateArray[1]),int(endDateArray[2]),int(endTimeArray[0]),int(endTimeArray[1])),
                            project_name=project_name)

        elif projectNameCount < tempCount and contentsCount >= tempCount :
            if projectNameCount == -1 :
                todoSaveForm(
                    todoName = "",
                             person_created = create_user,
                            todoContents = contentsArray[tempCount],
                            startDate = datetime.datetime(int(startDateArray[0]),int(startDateArray[1]),int(startDateArray[2]), int(startTimeArray[0]), int(startTimeArray[1])),
                            endDate = datetime.datetime(int(endDateArray[0]),int(endDateArray[1]),int(endDateArray[2]),int(endTimeArray[0]),int(endTimeArray[1])),
                            project_name=project_name)
            else:
                todoSaveForm(
                    todoName = projectNameArray[projectNameCount],
                        person_created = create_user,
                        todoContents = contentsArray[tempCount],
                        startDate = datetime.datetime(int(startDateArray[0]),int(startDateArray[1]),int(startDateArray[2]), int(startTimeArray[0]), int(startTimeArray[1])),
                        endDate = datetime.datetime(int(endDateArray[0]),int(endDateArray[1]),int(endDateArray[2]),int(endTimeArray[0]),int(endTimeArray[1])),
                        project_name=project_name)


        tempCount = tempCount + 1
        
    todoSaveForm(
        todoName = projectNameArray[tempCount],
                         person_created = create_user,
                        todoContents = contentsArray[tempCount],
                        startDate = datetime.datetime(int(startDateArray[0]),int(startDateArray[1]),int(startDateArray[2]), int(startTimeArray[0]), int(startTimeArray[1])),
                        endDate = datetime.datetime(int(endDateArray[0]),int(endDateArray[1]),int(endDateArray[2]),int(endTimeArray[0]),int(endTimeArray[1])),
                        project_name=project_name)
    content_todo=Todo.objects.values('todoContents')
 
    todos = Todo.objects.filter(project_name=project_name).values()
    project_name=request.session['project_name']
    excel_output()#excel에 반영
    context = {'todos' : todos}
    return render(request, 'startPages/left_navi/planMainPage.html', context)

def homepage(request):
    wordcloud_flag=request.session['flag']
    userid=request.session['userid']
    if wordcloud_flag is 1 :
        output_csv('Brainstorming_idea.csv','ideas') #csv 파일로 아이디어들을 추출합니다.
        try:
            os.remove('..//KoreanTypeAgile/startPage/static/image/wordcloud.jpg')
            make_wordcloud('Brainstorming_idea.csv','wordcloud.jpg',1200,300)
            os.rename('wordcloud.jpg','..//KoreanTypeAgile/startPage/static/image/wordcloud.jpg')
        except:#삭제할 파일이 없는경우 == 처음으로 brainstorming 을 입력했을 경우    
            make_wordcloud('Brainstorming_idea.csv','wordcloud.jpg',1200,300)
            os.rename('wordcloud.jpg','..//KoreanTypeAgile/startPage/static/image/wordcloud.jpg')
            
        request.session['flag'] = 0
    project_week=1
    for i in range(10):
        isvaild=Brainstorm.objects.filter(project_week=i+1).exists()
        if isvaild is True : pass
        else : 
            project_week=i
            break
    week_list=[]
    for i in range(project_week):
        week_list.append(i+1)       
    projects = Project.objects.filter(project_member=userid).values('project_name','project_contents')
    context = {'projects' : projects, 'week_list' : week_list}
    return render(request, 'startPages/top_navi/homepage.html', context)


def homepage_project(request,project_name):
    userid=request.session['userid']
    member_cnt=0
    context=Project.objects.filter(project_name=project_name).values('project_member','project_name')
    context_list = [entry for entry in context] # userinfo를 list로 바꿔주는 코드    
    context_dict={}
    for user in context_list:#list를 dict로 바꿔주는 for문 입니다. 
        for items in user :
           value=user[items]
           context_dict[items]=value


    project_week=1
    for i in range(10):
        isvaild=Brainstorm.objects.filter(project_name=project_name,project_week=i+1).exists()
        if isvaild is True : pass
        else : 
            project_week=i
            break
    week_list=[]
    for i in range(project_week):
        week_list.append(i+1)    

    project_emails=Project.objects.filter(project_name=project_name).values('project_member')
    members_name=[]
    for email in project_emails:
        for name in email :
            temp=User.objects.filter(email=email[name]).values('name')
            member_cnt+=1
            temp_list= [entry for entry in temp]
            temp_dict= {}
            for temp in temp_list:#list를 dict로 바꿔주는 for문 입니다. 
                for name in temp :
                    value=temp[name]
                    temp_dict[name]=value
                    members_name.append(temp_dict)
    project_names=Project.objects.filter(project_member=userid).values('project_name')
    context_dict['projects']=project_names
    context_dict['week_list']=week_list
    context_dict['members_name']=members_name
    context_dict['member_cnt']=member_cnt
    return render(request, 'startPages/top_navi/homepage.html', context_dict)
def profile(request):
    userid=request.session['userid']
    #로그인 할때 저장한 session 을 불러서 userid 에 저장 해줍니다. userid 에는 로그인한 email이 저장 됩니다.
    userinfo=User.objects.filter(email=userid).values('name','email')
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

    todos = Todo.objects.all()
    brains = Brainstorm.objects.all()
    issues = Issue.objects.all()
    context = {'todos' : todos, "brains":brains, "issues":issues}

    return render(request, 'startPages/left_navi/timeline.html', context) 
 
def backlog(request):
    return render(request, 'startPages/left_navi/backlog.html')    
def kanban(request):
    project_name=request.session['project_name']
    todos = Todo.objects.filter(project_name=project_name).values()
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
    userid=request.session['userid']
    
    if member is None :#처음 켰을떄, None 임으로 그에 대한 처리
        context={}
        return render(request,'startPages/popup_invite_team.html',context)
    elif member == userid :# 본인을 멤버로 추가할 경우
        messages.info(request,"본인은 멤버로 추가할 수 없습니다")
        return render(request,'startPages/popup_invite_team.html')
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
            request.session['flag'] = 0
            request.session.set_expiry(0)
            #로그인한 유저를 저장하기 위해 session 에 저장을 해줍니다. 
            # ex ) {'userid' : input_email } 
            projects = Project.objects.filter(project_member=input_email).values('project_name','project_contents');
            context = {'projects' : projects}
            return render(request,'startPages/top_navi/homepage.html',context)
        
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
        content=Brainstorm.objects.filter(project_name=project_name).values();
        return render(request,'startPages/left_navi/brain_storming.html',{'content':content})
    else :# 입력하지 않은 경우 or 처음 실행시킨 경우
        content=Brainstorm.objects.filter(project_name=project_name).values();
        return render(request,'startPages/left_navi/brain_storming.html',{'content':content})


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
    excel_output()#excel에 반영
    return HttpResponse("You're looking at question")

def make_wordcloud(text,image_name,width,height):
    list_of_tuple=return_list_of_tuples(text)
    tuple_countnoun=tuple(list_of_tuple)
    taglist=pytagcloud.make_tags(tuple_countnoun)
    pytagcloud.create_tag_image(taglist,image_name,size=(width,height),fontname='Nanum Gothic',rectangular=False)
    
def excel_output():
    wbk = xlwt.Workbook()
    sheet = wbk.add_sheet('project')
    
    sheet.col(0).width = int(13*260) 
    sheet.col(1).width = int(13*590) 
    sheet.col(2).width = int(13*590) 
    sheet.col(3).width = int(13*1060) 
    
    sheet.row(1).height_mismatch = True
    sheet.row(1).height = 36*20
    #excel sytle지정
    top_style_string = "font: bold on, color white;\
                    alignment: horiz centre; \
                     borders: top_color white, bottom_color white, right_color white, left_color white,\
                     left double, right double, top double, bottom double;\
                     pattern: pattern solid, fore_color black;"
    name_style_string = "font: bold on;\
                    alignment: horiz centre; \
                    borders: left double, right double, top double, bottom double;\
                     pattern: pattern solid, fore_color white;"
    contents_style_string = "alignment: horiz centre;\
                     pattern: pattern solid, fore_color white;"
    title_style_string = "alignment: horiz centre;\
                            font: bold 1,height 380;"
    top_style = xlwt.easyxf(top_style_string)
    name_style = xlwt.easyxf(name_style_string)
    contents_style = xlwt.easyxf(contents_style_string)
    title_style = xlwt.easyxf(title_style_string)
    sheet.insert_bitmap('..//KoreanTypeAgile/startPage/static/image/logo.bmp', 0, 0)
    sheet.write(1, 2, 'project name', style=title_style)
    sheet.write(7, 0, '이름', style=top_style )
    sheet.write(7, 1, '시작 일', style=top_style)
    sheet.write(7, 2, '마감 예상일', style=top_style)
    sheet.write(7, 3, '할일', style=top_style)
    sheet.write(7, 4, '상태', style=top_style)
    sheet_2 = wbk.add_sheet('burndown chart')
    sheet_2.write(0, 0, '이름')
    sheet_2.write(0, 4, '기간 내 할일 수행률') 
    
    
    
    i = 8
    todos = Todo.objects.all()
    for todo in todos:
        sheet.write(i, 0, todo.person_created, name_style)
        sheet.write(i, 1, todo.startDate.strftime("%Y-%m-%d %H:%M:%S"),contents_style)
        sheet.write(i, 2, todo.endDate.strftime("%Y-%m-%d %H:%M:%S"), contents_style)
        sheet.write(i, 3, todo.todoName, contents_style)
        sheet.write(i, 4, todo.get_status(), contents_style)
        i += 1
    wbk.save('..//KoreanTypeAgile/startPage/static/document/excel_output.xls') 
    

def chart(project_name, create_user):

    #현재프로젝트 주기, 생성 시간 가져옴
    project=Project.objects.filter(project_name=project_name).values()
    project_Cycle = project[0]["project_Cycle"] 
    project_start_time = project[0]["project_start_time"]  
    project_start_date = project_start_time.strftime('%Y-%m-%d') 
    #todo 가져옴
    todos = Todo.objects.filter(project_name=project_name, person_created = create_user).values()
    todo_count = 0
    do_count = 0
    done_count = 0
    all_count = 0
    for todo in todos:
        all_count += 1
        if todo["todo"]:
            todo_count += 1
        elif todo["do"]:
            do_count += 1    
        elif todo["done"]:
            done_count += 1 
    #id/pw in plolt 2@2.com/asdfsadf ### username: chart_image API Key: nvV3Kfu4M2by2Agab3TX
    py.sign_in('chart_image', 'nvV3Kfu4M2by2Agab3TX') # Replace the username, and API key with your credentials.
    # Add data
    month = [project_start_date, 
    (project_start_time + datetime.timedelta(days=1)).strftime('%Y-%m-%d'), 
    (project_start_time + datetime.timedelta(days=2)).strftime('%Y-%m-%d'), 
    (project_start_time + datetime.timedelta(days=3)).strftime('%Y-%m-%d'),
    (project_start_time + datetime.timedelta(days=4)).strftime('%Y-%m-%d'),
    (project_start_time + datetime.timedelta(days=5)).strftime('%Y-%m-%d'),
    (project_start_time + datetime.timedelta(days=6)).strftime('%Y-%m-%d')
    ]
    high_2000 = [32.5, 37.6, 49.9, 53.0, 69.1, 75.4, 76.5]
    low_2000 = [13.8, 22.3, 32.5, 37.2, 49.9, 56.1, 57.7]

    # Create and style traces
    trace0 = go.Scatter(
        x = month,
        y = high_2000,
        name = 'High 2014',
        line = dict(
            color = ('rgb(205, 12, 24)'),
            width = 4)
    )
    trace1 = go.Scatter(
        x = month,
        y = low_2000,
        name = 'Low 2014',
        line = dict(
            color = ('rgb(22, 96, 167)'),
            width = 4,)
    )

    data = [trace0, trace1]

    # Edit the layout
    layout = dict(title = 'Burndown Chart',
                xaxis = dict(title = 'Date'),
                yaxis = dict(title = '성취율'),
                )

    fig = dict(data=data, layout=layout)
    py.iplot(fig, filename='styled-line')
    try:
        os.remove('..//KoreanTypeAgile/startPage/static/image/plot_image.png')
        py.image.save_as(fig,'..//KoreanTypeAgile/startPage/static/image/plot_image.png')
    except: 
        py.image.save_as(fig,'..//KoreanTypeAgile/startPage/static/image/plot_image.png')
    # Image('..//KoreanTypeAgile/startPage/static/image/plot_image.png') # Display a static image
    
    # offline.plot(fig,
    #          auto_open=True, image = 'png', image_filename='..\\KoreanTypeAgile\startPage\\static\image\plot_image' ,
    #          output_type='file', image_width=800, image_height=600, filename='..//KoreanTypeAgile/startPage/static/document/plot_chart.html', validate=False)
    # py.plot(fig, filename= 'shaded_lines')
    
def weekend_report(request): 
    project_name=request.session['project_name']  
    #create_user
    userid=request.session['userid']
    userinfo=User.objects.filter(email=userid).values('name')
    userinfo_list = [entry for entry in userinfo]  
    userinfo_dict={}
    for user in userinfo_list:#list를 dict로 바꿔주는 for문 입니다. 
        for items in user :
           value=user[items]
           userinfo_dict[items]=value
    create_user = userinfo_dict["name"]
    #chart함수
    chart(project_name=project_name, create_user = create_user)
    return render(request, 'startPages/left_navi/weekend_report.html')  

def chart_in_plotly(request):  
    return render(request, 'startPages/left_navi/weekend_report.html')   


def add_issue_submit(request):

    userid=request.session['userid']
    userinfo=User.objects.filter(email=userid).values('name')
    userinfo_list = [entry for entry in userinfo]  
    userinfo_dict={}
    for user in userinfo_list:#list를 dict로 바꿔주는 for문 입니다. 
        for items in user :
           value=user[items]
           userinfo_dict[items]=value
    create_user = userinfo_dict["name"]

    issue_name = request.POST.get('issue_name', '')
    issue_contents = request.POST.get('issue_contents', '')
    issue_type = request.POST.get('issue_type', '')
    issue_severity = request.POST.get('issue_severity', '')
    issue_priority = request.POST.get('issue_priority', '')
    issue_status = request.POST.get('issue_status', '')
    issue_create = request.POST.get('issue_create', '')

    issue = Issue(
                issue_name = issue_name,
                issue_contents = issue_contents,
                issue_type = issue_type,
                issue_severity = issue_severity,
                issue_priority = issue_priority,
                issue_status = issue_status,)
                
                        
    issue.save()
    issues = Issue.objects.all()

    context = {'issues' : issues}
    return render(request, 'startPages/left_navi/issues.html', context)


def add_issues(request):
    return render(request, 'startPages/add_issues.html')