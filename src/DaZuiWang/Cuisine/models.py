from django.db import models

# Create your models here.

class Restaurant(models.Model):
    '''
    resturant: R_name,Region,Place,Taste,Location,Email,Phone,fixedPhone,
    '''
    R_name=models.CharField(max_length=50)
    City=models.CharField(max_length=60)
    Region=models.CharField(max_length=50)
    Place=models.CharField(max_length=50)
    Taste=models.CharField(max_length=50)
    Location=models.CharField(max_length=50)
    Email=models.EmailField()
    Phone=models.CharField(max_length=20)
    fixedPhone=models.CharField(max_length=20)
    
    def __unicode__(self):
        return self.R_name
class Cuisine(models.Model):# 
    '''
    Cuisine: name,cuisine,price, resturant
    '''
    
    name=models.CharField(max_length=50)
    cuisine=models.CharField(max_length=50)
    restaurant=models.ForeignKey(Restaurant)
    price=models.IntegerField()
    
    def __unicode__(self):
        return self.name
    