from django.conf.urls import *
from django_braintree import views 

urlpatterns = patterns('django_braintree.views',
    url(r'^payments-billing/$', views.payments_billing, name='payments_billing'),
    url(r'^pay/$', views.pay_bill, name='pay'),
    url(r'^pay/webhooks/$',views.webhooks,name='webhooks'),
    
)
