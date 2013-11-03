'''
Created on 2013-9-20

@author: samsung
'''
from django.contrib.auth.models import User

user = User.objects.filter(username="ddongjian0000").all()
profile=user.get_profile()

print profile.birthday
