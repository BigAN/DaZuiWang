from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from django.db.models.signals import post_save 

class UserProfile(models.Model):
    user =models.OneToOneField(User)
    birthday=models.DateField()
    cellphone=models.CharField(max_length=30,default='',blank=True)
    address= models.CharField(max_length=200,default='',blank=True)
    address1= models.CharField(max_length=200,default='',blank=True)
    address2= models.CharField(max_length=200,default='',blank=True)
    address3= models.CharField(max_length=200,default='',blank=True)
    test=models.CharField(max_length=200,default=   '',blank=True)
    
    def __unicode__(self):
        return self.user.username
    
def create_user_profile(sender,instance,created,**kwargs):
        if created:
            profile=UserProfile()
            profile.user=instance
            profile.save()
            
#post_save.connect(create_user_profile, sender=User,instance=User)