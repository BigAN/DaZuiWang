# Create your views here.
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


from stores import forms, models
from stores.models import Product,Store
def registerHtml(request):
    return render_to_response('member/login.html')

def all_products(request):
    products=Product.objects.all();
    return render(request,'store/all_products.html',{'products':products})

def getStoreNameFromUrl(url):
        start=url.find( '/stores/')
        storeNmae=url[start+8:-1]
        return storeNmae
def index_all(request):
    print "hello"
    products=Product.objects.all()
    return render(request,'store/index.html',{'products':products})

def index_stores_all(request):

    stores=Store.objects.all()
    return render(request,'store/index of stores.html',{'stores':stores})
def index_store_products(request):
    
    storename=request.POST['name']
    store=Store.objects.get(name=storename)
    return render(request,'store/products.html',{'store':store})    
def get_product(request):
    productname=request.POST['name']
    product=get_object_or_404(models.Product,name=productname)
    
    return render(request,'store/product.html',{'product':product})
    

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
    return render(request,'store/index.html',{'store':store,'cart':cart})

def search(request):
    return render_to_response('store/search.html')


def intro(request):
    return render_to_response('store/intro.html')
def cart(request, product_id=None, checkout_form=None):
    print "hello:"
    store = get_object_or_404(models.Store, name=request.subdomain)
    cart = models.Order.get_cart(store=store, user=request.user)
    if request.method == 'POST' and product_id:
        product = get_object_or_404(models.Product, name=product_id)
        cart.add_product(product)
        print cart.total()
        return HttpResponse(json.dumps({'new_total': str(cart.total())}), content_type="application/json")
    return render(request, 'store/cart.html', {'store': store, 'cart': cart, 'checkout_form': checkout_form or forms.CheckoutForm()})



@login_required
def remove_from_cart(request, product_id):
    store = get_object_or_404(models.Store, name=request.subdomain)
    cart = models.Order.get_cart(store=store, user=request.user)
    product = get_object_or_404(models.Product, id=product_id)
    cart.remove_product(product)
    return redirect('cart')


@login_required
def checkout_cart(request):
    if request.method == 'POST':
        
        store = get_object_or_404(models.Store, name=request.subdomain)
        order = models.Order.get_cart(store=store, user=request.user)
        form = forms.CheckoutForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return render(request, 'store/confirm_order.html', {'store': store, 'order': order, 'checkout_form': forms.CheckoutForm()})
        else:
            return cart(request, checkout_form=form)
    raise Http404

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
    return render(request, 'store/past_orders.html', {'store': store, 'cart': cart, 'orders': orders, 'checkout_form': forms.CheckoutForm()})


