# Create your views here.

from django.shortcuts import render_to_response

def main(request):
    print "dassdf"
    
    return render_to_response('bootstrap/test.html')
    #return render_to_response('store/introduction.html')
  

