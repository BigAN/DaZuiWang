from django.conf.urls import patterns, include, url
from django.contrib import admin
from DaZuiWang.views import login_view,logout_view,main_view,register_view
from Cuisine import views as Cuisine_view
admin.autodiscover()

'''
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/login/$',login_view),
    url(r'^accounts/logout/$',logout_view),
    url(r'^accounts/register/$',register_view),
    url(r'^main/$', main_view),
    '''
    
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    #login view
    #main page
    #get all resturants for main page
    
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/login/$',login_view),
    url(r'^accounts/logout/$',logout_view),
    url(r'^accounts/register/$',register_view),
    url(r'^main/$', main_view), 
    url(r'^main/RestaurantAll',Cuisine_view.getAllRestaurant, name="getAllRestaurant"),
    
    #get cuisines for resturant
    #url(r'cuisine/$',Cuisine_view.getCuisineForOneRestaurant,name="getCuisine")
#  DaZuiWang.Cuisine.views.getCuisineForOneRestaurant
    # Examples:s
    # url(r'^$', 'DaZuiWang.views.home', name='home'),
    # url(r'^DaZuiWang/', include('DaZuiWang.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)

