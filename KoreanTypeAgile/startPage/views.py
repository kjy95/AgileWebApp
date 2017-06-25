from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return render(request, 'startPages/index.html')
def loginPage(request):
    return render(request, 'startPages/loginPage.html')
def siginUpPage(request):
    return render(request, 'startPages/signUpPage.html')
def planMainPage(request):
    return render(request, 'startPages/planMainPage.html')