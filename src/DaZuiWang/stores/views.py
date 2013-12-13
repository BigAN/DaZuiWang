# -*- coding:utf-8 -*- 
import json
from datetime import datetime

from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.forms.util import ErrorList
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.shortcuts import render_to_response

from django.utils import simplejson
from stores import forms, models
from stores.models import Product,Store

def registerHtml(request):
    is_store=request.user.groups.filter(name='store')
    d={}
    d['is_store']=is_store
    return render(request,'member/login.html',d)

def all_products(request):
    products=Product.objects.all();
    return render(request,'all_products.html',{'products':products})

def getStoreNameFromUrl(url):
        start=url.find( '/stores/')
        storeNmae=url[start+8:-1]
        return storeNmae
def index_all(request):
    print "hello"
    products=Product.objects.all()
    return render(request,'index.html',{'products':products})

def index_stores_all(request):

    stores=Store.objects.all()
    return render(request,'index of stores.html',{'stores':stores})

def index_store_products(request):
    
    storename=request.POST['name']
    store=Store.objects.get(name=storename)
    #print storename
    return render(request,'products.html',{'store':store})    
def get_product(request):
    productname=request.POST['name']
    product=get_object_or_404(models.Product,name=productname)
    
    return render(request,'product.html',{'product':product})
    

def index(request):
    print request.get_full_path()
    print request.path
    store=getStoreNameFromUrl(request.path)
    '''
    print "hello"
    print request.subdomain
    print request.user
    '''
    store=get_object_or_404(models.Store,name=store)
    cart=models.Order.get_cart(store=store,user=request.user)
    return render(request,'index.html',{'store':store,'cart':cart})

def searchTag(request):
    #print request.POST
    cuisine=request.POST['name']
    products=models.Product.objects.filter(cuisine=cuisine)
    #print products
    return render(request,'search_tag_result.html',{'products':products})

def search(request):
    search_para=request.POST['para']
    products=models.Product.objects.filter(name__contains=search_para)
    stores=models.Store.objects.filter(name__contains=search_para)
    return render(request,'search_result.html',{'products':products,'stores':stores})

def searchMain(request):
    return render_to_response('search.html')
def order(request):

    # orders=models.Order.objects.get(user=request.user)
    if request.method=="POST":
        para=request.POST['name']
        id=request.POST['id']
        if para=="agree":
            order=models.Order.objects.get(id=id)
            order.agree_order()
            orders=request.user.order_set.all()

            orders=orders.order_by("-ordered_on")
            print orders
            # return render(request,'single_order.html',{'order':order})
            return render(request,'storeorder.html',{'orders':orders})
        elif para=="cancel":
            order=models.Order.objects.get(id=id)
            order.cancel_order()
            orders=request.user.order_set.all()
            orders=orders.order_by("-ordered_on")
            # return render(request,'single_order.html',{'order':order})
            return render(request,'storeorder.html',{'orders':orders})
        elif para=="finish":
            order=models.Order.objects.get(id=id)
            order.cancel_order()
            orders=request.user.order_set.all()
            orders=orders.order_by("-ordered_on")
            # return render(request,'single_order.html',{'order':order})
            return render(request,'storeorder.html',{'orders':orders})
    else:
        orders=request.user.order_set.all()
        print orders
        orders=orders.order_by("-ordered_on")
        print orders
        return render(request,'order.html',{'orders':orders})
def storeorder(request):

    # orders=models.Order.objects.get(user=request.user)
    orders=request.user.order_set.all()
    orders=orders.order_by("-ordered_on")
    return render(request,'storeorder.html',{'orders':orders})
def intro(request):
    storename=request.POST['name']
    #print storename
    
    store=Store.objects.get(name=storename)
    return render(request,'intro.html',{'store':store})
    #return render_to_response('intro.html')
def cart(request, product_id=None, checkout_form=None):
    info={"info":u"请先付款再进入其它餐厅"}
    storename=""
    storeid=0
    l_storename=request.POST.getlist('store_name')
    l_storeid=request.POST.getlist('store_id')
    if 'storename' in request.session and 'storeid' in request.session and len(request.session['storename'])>0 and request.session['storeid']>0:
        storename=request.session['storename']
        storeid=int(request.session['storeid'])
    else:
        #list=request.POST.getlist('store_name')

        print "step1"
        if len(l_storename)>0:
            storename=l_storename[0]
            storeid=l_storeid[0]
            request.session['storename']=storename
            request.session['storeid']=int(storeid)
            
    print "step2"    
    if len(l_storename)>0:
        if storename!=l_storename[0]:
            return HttpResponse(json.dumps(info), content_type="application/json")
     
    
    print "step3"
   # if request.session['storename']:
    if request.user is not None and storeid>0:
        store = get_object_or_404(models.Store, id=storeid)
        print "store"
        cart = models.Order.get_cart(store=store, user=request.user)
        # print len(cart.pro.all())
       
        l_product=request.POST.getlist('product_id')
    else:
        info={"info":u"您的购物车为空，请吃点东西吧！"}
        return render(request, 'cart.html', {'info': info["info"]})
    print "step4"
    if request.method == 'POST' and len(l_product)>0:
      #  print "adf"

        print "step5"
        product = get_object_or_404(models.Product, name=l_product[0])
        
        #request.session['storename'] = storename\
        cart.add_product(product)
       # print cart.total()
        return HttpResponse(json.dumps({'new_total': str(cart.total())}), content_type="application/json")
    if len(cart.products.all())==0:
        info={"info":u"您的购物车为空，请吃点东西吧！"}
        return render(request, 'cart.html', {'info': info["info"]}) 
    return render(request, 'cart.html', {'store': store, 'cart': cart, 'checkout_form': checkout_form or forms.CheckoutForm()})



@login_required
def remove_from_cart(request,checkout_form=None):
    product_id=request.POST['product_id']
    storeid=request.session["storeid"]
    store = get_object_or_404(models.Store, id=storeid)
    cart = models.Order.get_cart(store=store, user=request.user)
    product = get_object_or_404(models.Product, id=product_id)
    cart.remove_product(product)
    return render(request, 'cart.html', {'store': store, 'cart': cart, 'checkout_form': checkout_form or forms.CheckoutForm()})



@login_required
def checkout_cart(request):
    print "start"
    if request.method == 'POST':
        storeid=request.session["storeid"]
        address=request.POST["address"]
        send_time=request.POST['send_time']
        pay_way=request.POST['pay_way']
        store = get_object_or_404(models.Store, id=storeid)
        order = models.Order.get_cart(store=store, user=request.user)
        order.status="ing"
        if len(order.productquantities_set.all())==0:
            info={"info":"product_0"}
            request.session['storeid']=''
            request.session['storename']=''
            return  HttpResponse(json.dumps(info))
        order.address=address
        order.send_time=send_time
        order.pay_way=pay_way
        if pay_way == 'pay_online':
            #online code
            pass
        order.ordered_on = datetime.now()
        order.save()
        request.session['storeid']=''
        request.session['storename']=''
        
        #print request.POST
        info={"info":"success"}
        return  HttpResponse(json.dumps(info))
    #     form = forms.CheckoutForm(request.POST, instance=order)
    #     if form.is_valid():
    #         form.save()
    #         return render(request, 'confirm_order.html', {'store': store, 'order': order, 'checkout_form': forms.CheckoutForm()})
    #     else:
    #         return cart(request, checkout_form=form)
    # raise Http404

@login_required
def confirm_order(request, order_id):
    if request.method == 'POST':
        order = get_object_or_404(models.Order, id=order_id, user=request.user)
        order.ordered_on = datetime.now()
        order.save()
        for pq in order.productquantities_set.all():
            if pq.quantity > pq.product.quantity:
                messages.error(request, 
                               '%s %ss were available for purchase, please try again when items are back in stock.' % (pq.product.quantity, pq.product.name))
                pq.quantity = pq.product.quantity
                pq.product.quantity = 0
            else:
                pq.product.quantity -= pq.quantity
            pq.product.save()
        messages.success(request, 'Thank you for your order!')
        return redirect('index')
    raise Http404

@login_required
def delete_order(request, order_id):
    order = get_object_or_404(models.Order, id=order_id, user=request.user)
    order.delete()
    messages.success(request, 'Your order has been deleted')
    return redirect('index')


@login_required
def past_orders(request):
    store = get_object_or_404(models.Store, name=request.subdomain)
    cart = models.Order.get_cart(store=store, user=request.user)
    orders = models.Order.objects.filter(user=request.user, store=store, ordered_on__isnull=False)
    return render(request, 'past_orders.html', {'store': store, 'cart': cart, 'orders': orders, 'checkout_form': forms.CheckoutForm()})

def person(request):
    return render(request,'person.html',{})

def store(request):
    return render(request,'store.html',{})
