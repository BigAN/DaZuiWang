'''
Created on 2013-8-19

@author: samsung
'''
from django import forms
from django.contrib.auth.models import User

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
    