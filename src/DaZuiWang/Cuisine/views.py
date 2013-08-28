# Create your views here.
from django.shortcuts import render_to_response
from Cuisine import models 
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response

def getAllRestaurant(request):
    all_res=models.Restaurant.objects.all()
    return render_to_response('restaurants.html',{'all_res':all_res})
    
def getCuisineForOneRestaurant(request):
    
    return HttpResponseRedirect('/main/')
    