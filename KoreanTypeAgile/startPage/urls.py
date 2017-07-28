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
    url(r'^Signup',views.Signup)
]
