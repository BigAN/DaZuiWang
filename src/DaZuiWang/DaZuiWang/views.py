'''
Created on 2013-8-18

@author: samsung
'''
import datetime
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login,logout
from django.shortcuts import render_to_response
from django.contrib.auth.models import User
from django.contrib import auth
from django.http import HttpResponse
from django.utils import simplejson
import json
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse,HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.forms.util import ErrorList
from Myadmin.models import UserProfile
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
        info={}
        info["info"]="error"
        print request.POST
        username=request.POST['username']
        password=request.POST['password']
        email=request.POST['email']
        entire_name=request.POST['entire_name']
        phone=request.POST['phone']
        birthday=request.POST['birthday']
        address=request.POST['address']
        
        u_name = User.objects.filter(username=username).all()
        u_email = User.objects.filter(email=email).all()
        
       
        if u_name|u_email:
            return HttpResponse(simplejson.dumps(info))
        else:
            user = User.objects.create_user(username,
                                            email,
                                            password)
            user.save()
            profile = UserProfile(user=user)
            
            profile.birthday=datetime.datetime(int(birthday[0:4]),int(birthday[5:7]),int(birthday[8:]))
            profile.cellphone=phone
            profile.address=address
            profile.save()
            print profile.cellphone
            profile=user.get_profile()
         
            user = auth.authenticate(username=username, 
                                     password=password)
            login(request,user)

            info["info"]="success"
            return HttpResponse(simplejson.dumps(info))
     
        '''
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
    '''
    
def login_view(request):
    login_errors=None
    info={}
    info["info"]="error"
    
    if request.method== 'POST':
        username=request.POST['username']
        password=request.POST['password']
        user=auth.authenticate(username=username,
                               password=password)
        if user.is_authenticated() :
            print "nimaa "
        if user is not None and user.is_active:
            login(request,user)

            info["info"]="success"
    
            return HttpResponse(simplejson.dumps(info))
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
        
      #  i=json.dumps(info)
       # print i
        return HttpResponse(simplejson.dumps(info))
    #return render(request,'bootstrap/login.html',{'form':forms.LoginForm()})

def logout_view(request):
    auth.logout(request)
    return redirect('main')

def address(request):
    
    address_info={}
    user=request.user
    profile = user.get_profile()
    func_addr={'address':profile.address,
    'address1':profile.address1,
    'address2':profile.address2,
    'address3':profile.address3,
    }
    if request.method=='POST':
        name=request.POST['name']
        data=request.POST['data']
        func_addr[name]=data
        profile.save()
        return "success"

    else:
        if len(profile.address)>1:
            address_info['address']=profile.address
        if len(profile.address)>1:
            address_info['address1']=profile.address1
        if len(profile.address)>1:
            address_info['address2']=profile.address2
        if len(profile.address)>1:
            address_info['address3']=profile.address3

        return HttpResponse(json.dumps(address_info), content_type="application/json")
    return None

def new_address(request):

   
    address_info={}
    user=request.user
    data=request.POST['data']
    profile = user.get_profile()
    func_addr={'address':profile.address,
    'address1':profile.address1,
    'address2':profile.address2,
    'address3':profile.address3,
    }
    flag=0
    for i in func_addr.items():
        if len(i)<1:
            i=data
            flag=1
            return "success"
    if flag==0:
        return "full"