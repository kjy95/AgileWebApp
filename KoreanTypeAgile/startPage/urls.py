from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index), 
    url(r'^loginPage', views.loginPage), 
    url(r'^signUpPage', views.signUpPage), 
    url(r'^Signin', views.Signin),
    url(r'^planMainPage', views.planMainPage),
    url(r'^todoPopUp', views.todoPopUp),
    url(r'^sendTodoSubmit', views.sendTodoSubmit),
    url(r'^send_project_submit', views.send_project_submit),
    url(r'^profile', views.profile),
    url(r'^search', views.search),
    url(r'^timeline', views.timeline),
    url(r'^backlog', views.backlog),
    url(r'^kanban', views.kanban),
    url(r'^issues', views.issues),
    url(r'^wiki', views.wiki),
    url(r'^team', views.team),
    url(r'^homepage', views.homepage),
    url(r'^create_project', views.create_project),
    url(r'^Signup',views.Signup),
    url(r'^brain_storming',views.brain_storming),
    url(r'^change_todo_data',views.change_todo_data)
]
