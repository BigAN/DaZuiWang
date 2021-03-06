'''
Created on 2013-8-31

@author: samsung
'''
'''
Created on 2013-8-22

@author: samsung
'''
from django.conf.urls import patterns, url

from stores import views


urlpatterns = patterns('',
    url(r'^$', views.index_stores_all, name='index'),
    url(r'^person/$',views.person,name='person'),
    url(r'^store/$',views.store,name='store'),
    url(r'^intro/$',views.intro,name='intro'),
    url(r'^order/$',views.order,name='order'),
    url(r'^order/$',views.order,name='agree_order'),
    url(r'^order/$',views.order,name='cancel_order'),
    url(r'^order/$',views.order,name='finish_order'),
    
    url(r'^storeorder/$',views.storeorder,name='storeorder'),
    
    url(r'^searchTag/$',views.searchTag,name='searchTag'),
    url(r'^search/$',views.search,name='search'),
    
    url(r'^searchMain/$',views.searchMain,name='searchMain'), 

    url(r'all_products/$',views.all_products,name='all_products'),
    url(r'^registrhtml/$',views.registerHtml,name='registerHtml'),
    url(r'(?P<store_id>\d+)/$',views.index_all,name='store_index'),
    url(r'products/',views.index_store_products,name='products'),
    url(r'get_product/',views.get_product,name='get_product'),
    url(r'^add_to_cart/$', views.cart, name='add_to_cart'),
    url(r'^remove_from_cart/$', views.remove_from_cart, name='remove_from_cart'),
    url(r'^cart/$', views.cart, name='cart'),
    url(r'^checkout_cart/$', views.checkout_cart, name='checkout_cart'),
    url(r'^confirm_order/(?P<order_id>\d+)/$', views.confirm_order, name='confirm_order'),
    url(r'^delete_order/(?P<order_id>\d+)/$', views.delete_order, name='delete_order'),
    url(r'^past_orders/$', views.past_orders, name='past_orders'),

    )
#url(r'^add_to_cart/(?P<product_id>\d+)/$', views.cart, name='add_to_cart'),
#url(r'^remove_from_cart/(?P<product_id>\d+)/$', views.remove_from_cart, name='remove_from_cart'),