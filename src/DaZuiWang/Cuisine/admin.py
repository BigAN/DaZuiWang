'''
Created on 2013-8-20
@author: samsung

'''
from django.contrib import admin
from Cuisine import models
admin.site.register(models.Restaurant)
admin.site.register(models.Cuisine)
