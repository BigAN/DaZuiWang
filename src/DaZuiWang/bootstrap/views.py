# -*- coding:utf-8 -*- 

from django.shortcuts import render_to_response
from stores import models
from django.shortcuts import render

def search(request):
	return render(request,'store/search.html')
def main(request):
    
    #return render_to_response('bootstrap/main.html')
    return render(request,'bootstrap/main.html')
   
    #return render_to_response('store/introduction.html')
    #return render_to_response('test/Copy of test.html')
    #return render_to_response('test/page.html')
def  gmap3(request):

    return render(request,'bootstrap/gmap3.html')
   
def intro(request):
    store=models.Store.objects.get(name="东来顺")
    return render(request,'store/intro.html',{'store':store})