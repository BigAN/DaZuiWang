'''
Created on 2013-8-18

@author: samsung
'''
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login,logout
from django.shortcuts import render_to_response
from django.contrib.auth.models import User

def main_view(request):
    return  render_to_response('base.html')

def register_view(request):
    '''
    register view
    '''
    '''
    template_var={}
    form=RegisterForm()
    if request.method=="POST":
        form=RegisterForm(request.POST.copy())
        if form.is_valid():
            username=form.cleaned_data["username"]
            email=form.cleaned_data["email"]
            password=form.cleaned_data["password"]
            user=User.objects.create_user(username.email.password)
            user.save()
            login_view(request,username,password)
     '''
    if request.method=='POST':
        form=UserCreationForm(request.POST.copy())
        if form.is_valid():
            username=form.cleaned_data["username"]
            print username
            email=form.cleaned_data["email"]
            password=form.cleaned_data["password"]
            new_user=form.save()
            return render_to_response('success.html')
        else:
            form= UserCreationForm()
        return render_to_response("register.html",{'form':form,})
    
def login_view(request):
    user=authenticate(username=request.POST['username'],password=request.POST['password'])
    print user
    if user is not None:
        login(request,user)
        print request.user
        return render_to_response('success.html')
    else:
        print "hello baby"
        return render_to_response('failure.html')
    
def logout_view(request):
    logout(request)