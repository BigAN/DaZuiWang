'''
Created on 2013-8-18

@author: samsung
'''
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login,logout
from django.shortcuts import render_to_response
from django.contrib.auth.models import User
from django.contrib import auth

from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse,HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.forms.util import ErrorList
import forms


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
    if request.method == 'POST':
        form = forms.RegisterForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(form.cleaned_data['username'],
                                            form.cleaned_data['email'],
                                            form.cleaned_data['password'])
            user.save()
            user = auth.authenticate(username=form.cleaned_data['username'], 
                                     password=form.cleaned_data['password'])

            auth.login(request, user)
            return redirect('index')
        else:
            return render_to_response('register.html',{'form':form})
            #return render(request, 'users/register.html', {'form': form})

    return render(request, 'register.html', {'form': forms.RegisterForm()})

    
def login_view(request):
    login_errors=None
    if request.method== 'POST':
        username=request.POST['username']
        password=request.POST['password']
        user=auth.authenticate(username=username,
                               password=password)
        if user is not None and user.is_active:
            login(request,user)
            return redirect('index')
        '''
        form=forms.LoginForm(request.POST)
        if form.is_valid():
            username=form.cleaned_data['username']
            password=form.cleaned_data['password']
            print username
            print password
            user=auth.authenticate(username=username,
                                   password=password) 
            print user     
            if user is not None and user.is_active:
                login(request,user)
                return redirect('index')
        '''
        '''
        errorlist
        use if method to implement this function in html
        '''
        #errors=form._errors.setdefault("__all__",ErrorList())
        #errors.append(u'Account not found Or Password is wrong')
        #return render(request,'bootstrap/login.html',{'form':form}) 
        return render_to_response('bootstrap/login.html')
    return render(request,'bootstrap/login.html',{'form':forms.LoginForm()})
def logout_view(request):
    auth.logout(request)
    return redirect('login')