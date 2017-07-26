from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index), 
    url(r'^loginPage', views.loginPage), 
    url(r'^signUpPage', views.siginUpPage), 
    url(r'^planMainPage', views.planMainPage), 
    url(r'^todoPopUp', views.todoPopUp), 
    url(r'^sendTodoSubmit', views.sendTodoSubmit),
    url(r'^main_page', views.main_page),
    url(r'^profile', views.profile),
    url(r'^search', views.search),
]
