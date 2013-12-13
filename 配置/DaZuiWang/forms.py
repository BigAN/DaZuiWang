'''
Created on 2013-8-19

@author: samsung
'''
from django.contrib.auth.models import User
from django import forms

class ChangeForm(object):
    """design for change personal information"""
    username = forms.CharField()
    oldpassword = forms.CharField(widget=forms.PasswordInput())
    newpassword= forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())
    email = forms.EmailField()
    birthday=forms.DateField()
    cellphone=forms.CharField(max_length=30)
    address= forms.CharField(max_length=200)
    address1= forms.CharField(max_length=200)
    address2= forms.CharField(max_length=200)
    address3= forms.CharField(max_length=200)
   
        
class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())

class RegisterForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())
    email = forms.EmailField()
                
    def clean_username(self):
        username = self.cleaned_data.get('username')
        users = User.objects.filter(username=username).all()
        if users:
            raise forms.ValidationError("Username exists")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        users = User.objects.filter(email=email).all()
        if users:
            raise forms.ValidationError("Email exists")
        return email



    def clean_confirm_password(self):
        if self.cleaned_data.get('password') != self.cleaned_data.get('confirm_password'):
            raise forms.ValidationError("Passwords don't match!")
        return self.cleaned_data.get('confirm_password')



'''
class RegisterForm(forms.Form):
    email=forms.EmailField(label=_(u"email"),max_length=30,widget=forms.TextInput(attrs={'size':30,}))
    password=forms.CharField(label=_(u"password"),max_length=30,widget=forms.PasswordInput(attrs={'size':20}))
    username=forms.CharField(label=_(u"name"),max_length=40,widget=forms.TextInput(attrs={'size':30,}))
    
    def clean_username(self):
        users=User.objects.filter(username__iexact=self.cleaned_data["username"])
        if not users:
            return self.cleaned_data["username"]
        raise forms.ValidationError(_(u"the name has been occupied"))
    def clean_email(self):
        users=User.objects.filter(username__iexact=self.cleaned_data["email"])
        if not users:
            return self.cleaned_data["email"]
        raise forms.ValidationError(_(u"the email has been occupied"))
'''    
    