from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from views import login_view,logout_view,main_view,register_view,address,change_info
from stores import views as stores_view
from bootstrap import views as test_view
import django_braintree
admin.autodiscover()

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
#admin.autodiscover()

urlpatterns = patterns('',
    
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/login/$',login_view,name='login'),
    url(r'^accounts/address$',address,name='address'),
    url(r'^accounts/logout/$',logout_view,name='logout'),
    url(r'^accounts/register/$',register_view,name='register'),
    url(r'^accounts/change/$',change_info,name='change'),
    url(r'^stores/', include('stores.urls')),
    url(r'', include('django_braintree.urls')),
    url(r'^$',test_view.main,name='main'),


    # url(r'^test/gmap3/$',test_view.gmap3,name='gmap3'),
    # url(r'^test/gmap3/$',test_view.o,name='gmap3'),
    #url(r'^test/search/$',test_view.search,name='search'),
    
    #url(r'^test/intro/$',test_view.intro,name='intro')
    
    )

#url(r'^main/$', main_view), 
    #url(r'^main/RestaurantAll',Cuisine_view.getAllRestaurant, name="getAllRestaurant"),
#url(r'^stores/', stores_view.index,name='index'),
    #url(r'^stores/cart/$',stores_view.cart,name='cart'),
    #url(r'^add_to_cart/(?P<product_id>\d+)/$', stores_view.cart, name='add_to_cart'),
    #get cuisines for resturant
    #url(r'cuisine/$',Cuisine_view.getCuisineForOneRestaurant,name="getCuisine")
#  DaZuiWang.Cuisine.views.getCuisineForOneRestaurant
    # Examples:s
    # url(r'^$', 'DaZuiWang.views.home', name='home'),
    # url(r'^DaZuiWang/', include('DaZuiWang.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    #url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)